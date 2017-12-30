/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "glue.h"

#ifndef _LOG_H_
#define _LOG_H_

#define LL(msg) fh_log_msg(msg)
#define LLL(msg, size) fh_log_data(msg, size)

#ifdef UART_ON
    #define DD(buf) \
    {\
            if (ADDR_DPRINTF_NULL == get_dprintf()) { \
            if (ADDR_UARTB_NULL != get_uartB()) { \
                uartB(buf); \
            } \
        } else { \
            dprintf(buf "\n"); \
        }\
    }
    #define D(fmt, ...) \
        if (ADDR_DPRINTF_NULL == get_dprintf()) {\
            if ((ADDR_UARTB_NULL != get_uartB()) && (ADDR_SNPRINTF_NULL != get_snprintf())) { \
                char ____buf[150]; \
                snprintf(____buf, sizeof(____buf)-1, fmt, __VA_ARGS__); \
                uartB(____buf); \
            } \
        } \
        else { \
            dprintf(fmt "\n", __VA_ARGS__); \
        }
#else
    #define DD(buf) 
    #define D(fmt, ...) 
#endif



#define ASSERT(cond, msg) if (!(cond)) { for (;;) { D("ASSERT (%s) FAILED at %s-%d! %s", #cond, __FILE__, __LINE__, msg); } }
#define ASSERT2(cond, fmt, ...) if (!(cond)) { for (;;) { D("ASSERT (%s) FAILED at %s-%d! " fmt, #cond, __FILE__, __LINE__, __VA_ARGS__); } }

#endif


