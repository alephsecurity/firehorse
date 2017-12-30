/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _FH64_H_
#define _FH64_H_ 

#include "fh.h"

#pragma pack(1)
typedef struct 
{
    u_int64 type;
    u_int32 *va;
    u_int64 val;
} 
patch;

#pragma pack(1)
typedef struct 
{
    u_int64 type;
    u_int32 *va;
    u_int64 flag;
    u_int64 inst;
    u_int64 instsize;
    u_int64 callback;
   // u_int32 cbarg1;
   // u_int32 cbarg2;
    char msg[BP_MESSAGE_LENGTH+1];
} 
bp;

#pragma pack(1)
typedef struct
{
    u_int64 mode;
    u_int32 *src;
    u_int32 *dst;
    u_int64 cksum;
}
page;


#pragma pack(1)
typedef struct
{
    u_int64 npages;
    page pages[];
}
pcopy;

#pragma pack(1)
typedef struct
{
    int *regs;
    u_int64 cpsr, spsr, dacr;
    bp *brkp;
} cbargs;


#pragma pack(1)
typedef struct
{
    u_int64 mode;
    u_int64 bplen;
    u_int64 patchlen;
    bp *bps;
    patch *patches;
    pcopy *pc;
} firehorse;

#endif