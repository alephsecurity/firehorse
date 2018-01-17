/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/
#include "fh.h"


/*
 * 32 bit debugger, this will be hooked into the abort handler
 */
int dbg(char *msg, int line, int flag)
{
    unsigned int unknown = AAA;
    int *saved_regs = get_fh_saved_regs();
    void *pc = (void *)saved_regs[14]; 
    char *bpmsg = (char *)&unknown;
    unsigned int spsr, cpsr, dfar, ifar,dacr, dfsr, ifsr;

    // get firehorse context data struct
    firehorse *fh = getcontext();
    bp *bps = (bp *)fh->bps;
    
    // set Domain Access Control Register to 0xffffffff so we won't get memory access aborts
    fh_dacr();

    // read system registers to our local variables
    __asm__("MRC p15,0, %[dacr], c3, c0, 0" : [dacr] "=r" (dacr));
    __asm__("MRC p15, 0, %[dfar], C6, C0, 0" : [dfar] "=r" (dfar));
    __asm__("MRC p15, 0, %[ifar], C6, C0, 2" : [ifar] "=r" (ifar));
    __asm__("MRC p15, 0, %[dfsr], C5, C0, 0" : [dfsr] "=r" (dfsr));
    __asm__("MRC p15, 0, %[ifsr], C5, C0, 1" : [ifsr] "=r" (ifsr));
    __asm__("MRS %[spsr], SPSR" : [spsr] "=r" (spsr));
    __asm__("MRS %[cpsr], CPSR" : [cpsr] "=r" (cpsr));
    u_int8 thumb = (spsr >> 5) & 1;

    // calculate the return address for the exception
    u_int32 fixedlr = saved_regs[14];
    fixedlr -= thumb ? 2 : 4;
    D("fixedlr (entry): %08x thumb: %d", fixedlr, thumb);
#ifdef VALIDATE_PAGES
    fh_verify_pages();   
#endif
    
    if (NULL == msg)
    {
        msg = (char *)&unknown;
    }
    
    // reproduce all other breakpoints and recover the original instruction for the current breakpoint
    bp *b = fh_reproduce_breakpoints_and_recover_instruction((u_int32 *)fixedlr);

#ifdef VALIDATE_PAGES
    fh_compute_page_checksums();
#endif

    if (NULL != b)
    {
        bpmsg = (char *)&(b->msg);
        bpmsg[BP_MESSAGE_LENGTH-1] = '\0';
    }
    for (;;)
    {
        // uart print
        D("%s-%x-%s", msg, line, bpmsg);
#ifndef SHORT_DBG_LOG
        D("r%02d %08x r%02d %08x r%02d %08x r%02d %08x", 0, saved_regs[0], 1, saved_regs[1], 2, saved_regs[2], 3, saved_regs[3]);
        D("r%02d %08x r%02d %08x r%02d %08x r%02d %08x",4, saved_regs[4], 5, saved_regs[5], 6, saved_regs[6], 7, saved_regs[7]);
        D("r%02d %08x r%02d %08x r%02d %08x r%02d %08x", 8, saved_regs[8], 9, saved_regs[9], 10, saved_regs[10], 11, saved_regs[11]);
        D("r%02d %08x sp  %08x  lr %08x", 12, saved_regs[12],  saved_regs[13],  saved_regs[14]);
        D("spsr %08x cpsr %08x dfar %08x ifar %08x", spsr, cpsr, dfar, ifar);
        D("dfsr %08x ifsr %08x dacr %08x", dfsr, ifsr, dacr);
#endif
        if (NULL != b)
        {
            D("bkva: %08x bkinst: %08x instsize: %2d", b->va, b->inst, b->instsize);
                
            if (0 != b->callback)
            {
                cbargs args = { .cpsr = cpsr, .spsr = spsr, .dacr = dacr, .brkp = b,.regs = saved_regs };
                brkcb cb = (brkcb)ADDR_CALLBACK(b->callback);
                D("Calling callback(%d) - %08x", b->callback, cb);
                cb(&args);   
            }

            if (1 != (b->flag & BP_FLAG_HALT))
                break;
        }
    }

    saved_regs[14] = fixedlr;

    invalidate_caches();
    D("fixed lr=%08x, reproduced instruction: %08x", fixedlr, *(u_int32 *)(fixedlr));
    DD("");

    // restore registers and return to fixed instruction
    __asm__("\
            BL get_fh_saved_regs;\
            MOV R1, R0;\
            LDR R0, [R1, #4];\
            MOV SP, R0;\
            LDR R0, [R1];\
            ADD R1, R1, #8;\
            LDMIA R1!, {R2-R12};\
            LDR LR, [R1,#4];\
            MOV R1, SP;\
            SUBS PC, LR, #0");

}