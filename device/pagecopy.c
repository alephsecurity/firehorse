/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"


/*
 * Copies all pages in the FireHorse context struct to their specified destanation
 */
STACKHOOK(pagecopy)
{
   int i = 0;
   
   firehorse *fh = getcontext();
   pcopy *p = fh->pc;

 
   page *pages = (page *)(&(p->npages)+1);

    D("pagecopy: number of pages: %d", p->npages);
   
   for (i = 0; i < p->npages; i++)
   {
        int j,k;
        D("src: %08x  dst:%08x", pages[i].src, pages[i].dst);
        
        for (j = 0 ; j < 0x1000/4; j++)
        {
            u_int32 v = (pages[i].src)[j];
            (pages[i].dst)[j] = v;
        }
   }
#ifdef VALIDATE_PAGES
   fh_compute_page_checksums();
#endif
   D("pagecopy: done with %d pages", p->npages);
}



