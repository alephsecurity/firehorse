/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"


// sets the Domain Access Control Register to 0xFFFFFFFF
STACKHOOK(dacr)
{
   DD("Elevating to manager");
   fh_dacr();
   DD("Done elevating");
}



