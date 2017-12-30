/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"


void cb_disable_uart()
{
  //  D("Disabling UART output functions: fh_log_msg = %08x, mini_snprintf = %08x", ADDR_CALLBACK(28), ADDR_CALLBACK(27));
    set_uartB(ADDR_UARTB_NULL);
    //set_snprintf(ADDR_CALLBACK(27));
    set_snprintf(ADDR_SNPRINTF_NULL);
    set_dprintf(ADDR_DPRINTF_NULL);
}



