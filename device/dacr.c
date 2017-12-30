/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"

STACKHOOK(dacr)
{
   DD("Elevating to manager");
   //__asm("MOV R0, #0xFFFFFFFF; MCR p15,0,R0,c3,c0,0;");
   fh_dacr();
   DD("Done elevating");
}



