/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"



int dbg(char *msg, int line, int flag)
{

   unsigned int unknown = AAA;
   //int *x = (flag != 0x6000) ? ADDR_SAVED_REGISTERS : ADDR_SAVED_REGISTERS2;
   int *x = get_fh_saved_regs();

   void *pc = (void *)x[14]; 
   char *bpmsg = (char *)&unknown;
  
   firehorse *fh = getcontext();
   bp *bps = (bp *)fh->bps;
   int i = 0;

   unsigned int spsr, cpsr, dfar, ifar,dacr, dfsr, ifsr;
    
   fh_dacr();

   __asm__("MRC p15,0, %[dacr], c3, c0, 0" : [dacr] "=r" (dacr));
   __asm__("MRC p15, 0, %[dfar], C6, C0, 0" : [dfar] "=r" (dfar));
   __asm__("MRC p15, 0, %[ifar], C6, C0, 2" : [ifar] "=r" (ifar));
   __asm__("MRC p15, 0, %[dfsr], C5, C0, 0" : [dfsr] "=r" (dfsr));
   __asm__("MRC p15, 0, %[ifsr], C5, C0, 1" : [ifsr] "=r" (ifsr));

   __asm__("MRS %[spsr], SPSR" : [spsr] "=r" (spsr));
   __asm__("MRS %[cpsr], CPSR" : [cpsr] "=r" (cpsr));

   u_int8 thumb = (spsr >> 5) & 1;
   u_int32 fixedlr = x[14];
   fixedlr -= thumb ? 2 : 4;

   D("SAVED SP = %08x",  x[13]);
//    DD("verifying pages");

#ifdef VALIDATE_PAGES
   fh_verify_pages();   
#endif

   D("fixedlr (entry): %08x thumb: %d", fixedlr, thumb);
   

   if (NULL == msg)
   {
       msg = (char *)&unknown;
   }
 //  D("Found %d breakpoints", fh->bplen);
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

       D("%s-%x-%s", msg, line, bpmsg);

#ifndef SHORT_DBG_LOG
       D("r%02d %08x r%02d %08x r%02d %08x r%02d %08x", 0, x[0], 1, x[1], 2, x[2], 3, x[3]);
       D("r%02d %08x r%02d %08x r%02d %08x r%02d %08x",4, x[4], 5, x[5], 6, x[6], 7, x[7]);
       D("r%02d %08x r%02d %08x r%02d %08x r%02d %08x", 8, x[8], 9, x[9], 10, x[10], 11, x[11]);
       D("r%02d %08x sp  %08x  lr %08x", 12, x[12],  x[13],  x[14]);
       D("spsr %08x cpsr %08x dfar %08x ifar %08x", spsr, cpsr, dfar, ifar);
       D("dfsr %08x ifsr %08x dacr %08x", dfsr, ifsr, dacr);
#endif
       if (NULL != b)
       {
           D("bkva: %08x bkinst: %08x", b->va, b->inst);
               
           if (0 != b->callback)
           {
               cbargs args = { .cpsr = cpsr, .spsr = spsr, .dacr = dacr, .brkp = b,.regs = x };
               brkcb cb = (brkcb)ADDR_CALLBACK(b->callback);
               D("Calling callback(%d) - %08x", b->callback, cb);
               cb(&args);   
           }

           if (1 != (b->flag & BP_FLAG_HALT))
               break;

       }
   }

   x[14] = fixedlr;

   invalidate_caches();
   D("fixed lr=%08x, reproduced instruction: %08x", fixedlr, *(u_int32 *)(fixedlr));
   DD("");

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