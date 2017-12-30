/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"
#include "pt64.h"


STACKHOOK(init)
{
    
  init_set_fh_entry();

   invalidate_context();
   firehorse *fh = getcontext();

   fh->mode++;
   fh_log_init();
   fh_apply_patches();
   fh_enable_breakpoints();

   fh_print_banner(fh);

}


