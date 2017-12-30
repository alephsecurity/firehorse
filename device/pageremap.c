/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"

STACKHOOK(pageremap)
{
   int i = 0;
   
   firehorse *fh = getcontext();
   pcopy *p = fh->pc;

 
   page *pages = (page *)(&(p->npages)+1);

    D("number of pages: %d", p->npages);
   
   for (i = 0; i < p->npages; i++)
   {
        D("src: %08x  dst:%08x", pages[i].src, pages[i].dst);
        pt_second_level_xsmallpage_remap(pages[i].src, pages[i].dst);       
        
   }
   invalidate_tlb();
   D("done with %d pages", p->npages);

}



