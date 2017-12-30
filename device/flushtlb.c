/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"

STACKHOOK(flushtlb)
{
    DD("Flushing tlb...");
   __asm("DSB SY; ISB SY; MOV R0, #0; MCR p15,0,R0,c8,c6,0; MCR p15,0,R0,c8,c5,0; MCR p15,0,R0,c8,c7,0; DSB SY; ISB SY;");
}



