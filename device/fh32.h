/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _FH32_H_
#define _FH32_H_ 

#include "fh.h"


#pragma pack(1)
typedef struct 
{
    u_int8 type;
    u_int32 *va;
    u_int32 val;
} 
patch;

#pragma pack(1)
typedef struct 
{
    u_int8 type;
    u_int32 *va;
    u_int8 flag;
    u_int32 inst;
    u_int8 instsize;
    u_int8 callback;
    char msg[BP_MESSAGE_LENGTH+1];
} 
bp;

#pragma pack(1)
typedef struct
{
    u_int8 mode;
    u_int32 *src;
    u_int32 *dst;
    u_int32 cksum;
}
page;


#pragma pack(1)
typedef struct
{
    u_int32 npages;
    page pages[];
}
pcopy;

#pragma pack(1)
typedef struct
{
    int *regs;
    int cpsr, spsr, dacr;
    bp *brkp;
} cbargs;


#pragma pack(1)
typedef struct
{
    u_int8 mode;
    u_int32 bplen;
    u_int32 patchlen;
    bp *bps;
    patch *patches;
    pcopy *pc;
} firehorse;

#endif