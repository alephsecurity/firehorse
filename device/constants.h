/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _CONSTANTS_H_
#define _CONSTANTS_H_

#include <constants.h>

#define INVALID_PTR ((void *)0x66666666)

#if ARCH==32
#define ADDR_CALLBACK(n) (get_fh_entry() + 0x20 + n*4)
#else
#define ADDR_CALLBACK(n) (get_fh_entry() + 0x30 + n*8)
#endif

#define ADDR_REMOTE_CALLBACK(n, dst) (void *)((ADDR_CALLBACK(n)-get_fh_entry()+dst))





#endif