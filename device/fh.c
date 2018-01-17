/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"


static firehorse *fh = INVALID_PTR;

#ifdef VALIDATE_PAGES
static u_int32 get_inst_for_va(firehorse *fh, u_int32 *va);
#endif

static void _mem2str(u_int8 *in, u_int32 size, u_int8 off, char *out);
static void _itoa(u_int8 in, char *out);
static char _n2c(u_int8 n);


void invalidate_context()
{
    fh = INVALID_PTR;
}


/*
 * Returns a pointer to the context (firehorse) data structure
 */
firehorse *getcontext()
{
    if (INVALID_PTR != fh)
    {
        return fh;
    }       

    fh = (firehorse *)get_fh_scratch();
    u_int32 bplen = fh->bplen;
    fh->bps = (bp *)((unsigned int)fh + sizeof(firehorse));
    bp *bps = (bp *) fh->bps;
    fh->patches = (patch *)(bps + bplen);
    fh->pc = (pcopy *)(fh->patches + fh->patchlen);

    return fh;
}


/*
 * Outputs a memory dump of the given address and size to uart
 */
void fh_memdump(u_int32 addr, u_int32 size)
{
    char *c = (char *)(addr & 0xFFFFFFFC);
    while (c <= (char *)(addr+size))
    {
        D("%08x: %02x%02x%02x%02x %02x%02x%02x%02x  %02x%02x%02x%02x %02x%02x%02x%02x   | %c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c |", 
            c,
            c[0],c[1], c[2],c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], c[11], c[12], c[13], c[14], c[15],
            P(c[0]),P(c[1]), P(c[2]),P(c[3]), P(c[4]), P(c[5]), P(c[6]), P(c[7]), P(c[8]), P(c[9]), P(c[10]), P(c[11]), P(c[12]), P(c[13]), P(c[14]), P(c[15]));
        
        c+=16;
    }

}


/*
 * Outputs a memory dump of the given address and size to uart
 */
void fh_memdump2(u_int32 addr, u_int32 size)
{
    char *c = (char *)(addr & 0xFFFFFFFC);
    char line[53];

    char *s = c;
    while (c <= (char *)(addr+size))
    {
        _mem2str(c, 16, c-s, line);
        uartB(line);
        c+=16;
    }
}


/*
 * Applies the patches relevant to given mode we're in (PROGRAMMER, PBL, SBL or ABOOT)
 */
void fh_apply_patches()
{
   firehorse *fh = getcontext();
   int i = 0;

   for (i = 0; i < fh->patchlen; i++)
   {
       patch *p = &fh->patches[i];
       if (fh->mode != p->type) continue;
       *(p->va) = p->val;
   }

#ifdef VALIDATE_PAGES
   fh_compute_page_checksums();
#endif
}


bp *fh_reproduce_breakpoints_and_recover_instruction(u_int32 *lr)
{
    firehorse *fh = getcontext();
    u_int64 i = 0;
    bp *b = NULL;
    bp *bps = (bp *)fh->bps;

    // find relevant breakpoint to restore
    for (i = 0; i < fh->bplen; i++)
    {
        if (bps[i].va == lr)
        {
            b = &bps[i];
            break;
        }
    }

    if (NULL == b) 
    {
        return NULL;       
    }

    // reproduce instruction
    switch (b->instsize)
    {
        case 4: *(u_int32 *)(b->va) = (u_int32)b->inst; break;
        case 2: *(u_int16 *)(b->va) = (u_int16)b->inst; break;
    }

    // reproduce all other breakpoints (only the ones relevant to current mode)
    for (i = 0; i < fh->bplen; i++)
    {
        if (0 == (bps[i].flag & BP_FLAG_ONCE) && (&bps[i] != b) && (bps[i].type == b->type))
        {
            switch (bps[i].instsize)
            {
                case 4: *(u_int32 *)(bps[i].va) = UNDEF_INST_32; break;
                case 2: *(u_int16 *)(bps[i].va) = UNDEF_INST_16; break;
            }
        }
    }

    return b;
}


void fh_enable_breakpoints()
{
    firehorse *fh = getcontext();
    int i = 0;

    for (i = 0; i < fh->bplen; i++)
    {
        bp *b = &fh->bps[i];
        if (fh->mode == b->type)
        {
            switch (b->instsize)
            {
                case 4:
                    b->inst = *(u_int32 *)(b->va);
                    break;
                case 2:
                    b->inst = (u_int32)*(u_int16 *)(b->va);
                    break;
            }
        }
    }

    for (i = 0; i < fh->bplen; i++)
    {
        bp *b = &fh->bps[i];
        if (fh->mode == b->type)
        {
            D("Installing bp for va 0x%08x, size=%0d", b->va, b->instsize);
            switch (b->instsize)
            {
                case 4:
                    *(u_int32 *)(b->va) = UNDEF_INST_32;
                    break;
                case 2:
                    *(u_int16 *)(b->va) = UNDEF_INST_16;
                    break;
            }
        
        }
    }
    #ifdef VALIDATE_PAGES
    fh_compute_page_checksums();
    #endif
}


/*
 * Copies the FireHorse code to a new location and updates relevant pointers
 */
void fh_rebase(u_int32 dst) 
{    
    codecpy(dst, get_fh_entry(), ADDR_SIZE);
    void (*rinit)() = ADDR_REMOTE_INIT(dst);
    D("Calling remote init: %08x", rinit);
    rinit();
}

static char log[ADDR_FH_LOG_SIZE+1] = {1};
static u_int32 logIndex = 0;


#define LOG_INDEX_GET(x) mod(x, ADDR_FH_LOG_SIZE)
#define LOG_INDEX       LOG_INDEX_GET(logIndex)
#define LOG_INDEX_INC   LOG_INDEX_GET(logIndex++)
#define LOG_WRITE(c)    log[LOG_INDEX_INC] = c; log[LOG_INDEX] = '\0'


void fh_log_init()
{
    log[sizeof(log)-1] = '\0';
}


void fh_log_msg(char *buf)
{
    while (*buf != 0)
    {
        LOG_WRITE(*buf);
        buf++;
    }
    LOG_WRITE('\r');
    LOG_WRITE('\n');
}


void fh_log_data(char *data, u_int32 size)
{
    while (size-- > 0)
    {
        LOG_WRITE(*data);
        data++;
    }
}


void fh_dump_log()
{   
    uartB("LOG DUMP");
    uartB(&log[LOG_INDEX_GET(logIndex+1)]);
    uartB(log);
}

/*
 * Invalidates uart and snprintf function pointers
 */
void fh_disable_uart()
{
    set_uartB(ADDR_UARTB_NULL);
    set_snprintf(ADDR_SNPRINTF_NULL);
    set_dprintf(ADDR_DPRINTF_NULL);
}


void fh_print_banner(firehorse *fh)
{
    D("Welcome to firehorse (%s, %d-bit arch)!", TARGET, ARCH);
    D("Loaded @ %016lx", get_fh_entry());
    D("mode=%d, #bps=%d, #patches=%d", fh->mode, fh->bplen, fh->patchlen);
    fh_print_system_registers();
}


void fh_print_system_registers()
{
#if ARCH==32
    D("CPSR = %08x", get_cpsr());
    D("SCR = %08x", get_scr());
    D("NSACR = %08x", get_nsacr());
    D("VBAR = %08x", get_vbar());
    D("MVBAR = %08x", get_mvbar());
    D("RMR = %08x", get_rmr());
    D("TTBR0 = %08x", get_ttbr0());
    D("TTBR1 = %08x", get_ttbr1());
#endif

#if ARCH==64
  u_int64 currentel = get_currentel()>>2;
  u_int64 ttbr0 = 0, ttbr1 = 0;
  D("Exception Level=%d", currentel);
  D("DAIF=%016lx, NZCV=%016lx, SPSel=%016lx", get_daif(), get_nzcv(), get_spsel());

  if (3 == currentel)
  {
      D("TTBR0_EL3  = %016lx", get_ttbr0_el3());
      D("VBAR_EL3   = %016lx", get_vbar_el3());    
      //D("RVBAR_EL3  = %016lx", get_rvbar_el3());    
      D("SCTLR_EL3  = %016lx", get_sctlr_el3());    
      D("TCR_EL3    = %016lx", get_tcr_el3()); 
      D("SCR_EL3    = %016lx", get_scr_el3());

  }
  if (2 == currentel)
  {
      D("TTBR0_EL2  = %016lx", get_ttbr0_el2());
      D("VBAR_EL2   = %016lx", get_vbar_el2());  
      D("RVBAR_EL2  = %016lx", get_rvbar_el2());
      D("SCTLR_EL2  = %016lx", get_sctlr_el2());    
      D("TCR_EL2    = %016lx", get_tcr_el2()); 
  }
  if (1 == currentel)
  {
      D("TTBR0_EL1  = %016lx", get_ttbr0_el1());
      D("TTBR1_EL1  = %016lx", get_ttbr1_el1());
      D("VBAR_EL1   = %016lx", get_vbar_el1());
    //   D("RVBAR_EL1  = %016lx", get_rvbar_el1());    
      D("SCTLR_EL1  = %016lx", get_sctlr_el1());    
      D("TCR_EL1    = %016lx", get_tcr_el1());
  }
#endif
   DD(" ");
}


/*
 * Convert a value in memory to its hex string representation
 */
static void _mem2str(u_int8 *in, u_int32 size, u_int8 offset, char *out)
{
    int i = 0;
    _itoa(offset, out);
    out[2] = ' ';
    out[3] = ' ';

    for (i = 0; i < size; i++)
    {
        _itoa(in[i], &out[4+3*i]);
         out[4+3*i+2] = ' ';
    }
    out[4+3*size] = '\0';
}

static void _itoa(u_int8 in, char *out)
{
    u_int8 n1 = in & 0xF;
    u_int8 n2 = in>>4 & 0xF;

    out[0] = _n2c(n2);
    out[1] = _n2c(n1);
}

static char _n2c(u_int8 n)
{
    if (n < 10)
    {
        return '0' + n;
    }
    return n-10 + 'a';
}


#ifdef VALIDATE_PAGES

/*
 * Verifies the pages in the pagecopy(pcopy) struct weren't corrupted
 */
void fh_verify_pages()
{
    firehorse *fh = getcontext();
    pcopy *p = fh->pc; 
    page *pages = &(p->npages)+1;
    u_int32 sum = 0;
    int i;

    for (i = 0; i < p->npages; i++)
    {
        int j;

        if (pages[i].mode != fh->mode) continue;
        if (!pages[i].cksum) continue;
        
        for (j = 0 ; j < 0x1000/4; j++)
        {
            u_int32 v = (pages[i].dst)[j];

            if (0xFFFFFFFF == v)
            {
                u_int32 *va = &(pages[i].dst)[j];
            }
            sum ^= v;
        }
        if (pages[i].cksum != sum)
        {
            for (;;)
            {
                D("verification for dst = 0x%08x failed (sum=%08x != cksum=%08x)", pages[i].dst, sum, pages[i].cksum);
            }
        }
        sum = 0;
    }
}


/*
 * Sets the checksum value for the pages in the pagecopy(pcopy) struct
 */
void fh_compute_page_checksums()
{
    firehorse *fh = getcontext();
    pcopy *p = fh->pc;
    page *pages = &(p->npages)+1;
    u_int32 sum = 0;
    int i = 0;

    for (i = 0; i < p->npages; i++)
    {
            int j,k;
            for (j = 0 ; j < 0x1000/4; j++)
            {
                u_int32 v = (pages[i].src)[j];
                sum ^= v;
            }
            pages[i].cksum = sum;
            sum = 0;
    }
}


/*
 * Returns the instruction to place in the given virual address
 */
static u_int32 get_inst_for_va(firehorse *fh, u_int32 *va)
{
   int i;
   for (i = 0; i < fh->bplen; i++)
   {
       bp *b = &fh->bps[i];

       if (b->va == va)
       {
            return b->inst;
       }
   }
   return *va;
}

#endif