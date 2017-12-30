/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _GLUE64_H_
#define _GLUE64_H_ 

#include "stdlib.h"

static u_int64 saved_lr;


#define GLUE_BODY(name) __asm__("\
        STP X0, X7, [SP,#-0x10]!;\
        STP X8, X30, [SP,#-0x10]!;\
        BL get_fh_entry;\
        LDP X8, X30, [SP],#0x10;\
        STP X8, X9, [SP,#-0x10]!;\
        MOV X8, X0;\
        STR X30, [X8, #0x20];\
        LDR X7, =" #name "_ptr;\
        LDR X30,[X8, X7];\
        LDP X8, X9, [SP],#0x10;\
        LDP X0, X7, [SP],#0x10;\
        BLR X30;\
        STP X0, X7, [SP,#-0x10]!;\
        BL get_fh_entry;\
        LDR X30, [X0, #0x20];\
        LDP X0, X7, [SP],#0x10;\
        RET");
        
#endif

