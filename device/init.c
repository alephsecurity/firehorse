/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"

STACKHOOK(init)
{
   init_set_fh_entry(); 
    
   //DD("invalidating");
   invalidate_context();
   //DD("done");
   
   firehorse *fh = getcontext();
   fh->mode++;

   fh_log_init();
   fh_dacr();
   fh_apply_patches();
   fh_enable_breakpoints();

   invalidate_caches();
   fh_print_banner(fh);


}

