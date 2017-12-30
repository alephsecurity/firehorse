/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "stdlib.h"
#include "glue.h"
#include "fh.h"
 
__attribute__((naked)) dbg64entry() {
    volatile u_int64 *regs;
    __asm__("MOV %[regs], SP" : [regs] "=r" (regs));
    dbg64(regs);
}
int dbg64(u_int64 x[])
{

    u_int64 currentel = get_currentel()>>2;
    u_int64 elr = -1, far = -1, esr = -1;
    switch (currentel)
    {
        case 1:
            elr = get_elr_el1();
            esr = get_esr_el1();
            far = get_far_el1();
            break;
        case 2:
            elr = get_elr_el2();
            esr = get_esr_el2();
            far = get_far_el2();
            break;
        case 3:
            elr = get_elr_el3();
            esr = get_esr_el3();
            break;
        default:
            break;
    }
    void *entry = get_fh_entry();
    firehorse *fh = getcontext();

    bp *b = fh_reproduce_breakpoints_and_recover_instruction((u_int32 *)elr);

    do
    {
        D("x%02d %016lx x%02d %016lx x%02d %016lx x%02d %016lx", 0,  x[0],  1,  x[1],  2,  x[2],  3,  x[3]);
        D("x%02d %016lx x%02d %016lx x%02d %016lx x%02d %016lx", 4,  x[4],  5,  x[5],  6,  x[6],  7,  x[7]);
        D("x%02d %016lx x%02d %016lx x%02d %016lx x%02d %016lx", 8,  x[8],  9,  x[9],  10, x[10], 11, x[11]);
        D("x%02d %016lx x%02d %016lx x%02d %016lx x%02d %016lx", 12, x[12], 13, x[13], 14, x[14], 15, x[15]);
        D("x%02d %016lx x%02d %016lx x%02d %016lx x%02d %016lx", 16, x[16], 17, x[17], 18, x[18], 19, x[19]);
        D("x%02d %016lx x%02d %016lx x%02d %016lx x%02d %016lx", 20, x[20], 21, x[21], 22, x[22], 23, x[23]);
        D("x%02d %016lx x%02d %016lx x%02d %016lx x%02d %016lx", 20, x[20], 21, x[21], 22, x[22], 23, x[23]);
        D("x%02d %016lx x%02d %016lx x%02d %016lx x%02d %016lx", 24, x[24], 25, x[25], 26, x[26], 27, x[27]);
        D("x%02d %016lx x%02d %016lx x%02d %016lx, sp %016lx",   28, x[28], 29, x[29], 30, x[30], x);
        D("CurrentEL %016lx", currentel);
        D("ELR_ELx %016lx", elr);
        D("ESR_ELx %016lx", esr);
        D("FAR_ELx %016lx", far);
        DD("");

    } while (b == NULL);


    __asm__("MOV SP, %[x]; B dbg_exit64" :: [x] "r" (x));
}