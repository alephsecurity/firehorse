/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _FH_H_
#define _FH_H_ 


#include "constants.h"
#include <shook_target.h>
#include "stdlib.h"
#include "glue.h"

#include "log.h"

#define INST_INFINITE_LOOP (0xEAFFFFFE)

// MUST BE 8-BYTE aligned (+1 for null terminator)
#define BP_MESSAGE_LENGTH (23)

//#define ADDR_UARTB (void *)(ADDR_ENTRY + 4*10)
//#define ADDR_SNPRINTF (void *)(ADDR_ENTRY + 4*11)

#define BP_FLAG_HALT (1)
#define BP_FLAG_ONCE (2)
#define BP_FLAG_DISABLEMMU (4)
#define BP_FLAG_MSGONLY (8)

#define BP_TYPE_PROGRAMMER (0)
#define BP_TYPE_PBL (1)
#define BP_TYPE_SBL (2)
#define BP_TYPE_ABL (3)

#define AAA (0x414141)
#define NULL ((void *)0)



#if ARCH==32
#include "fh32.h"
#else
#include "fh64.h"
#endif

firehorse *getcontext();

typedef void (*brkcb)(cbargs *args);

#define P(c) ((c >= 0x20 && c <= 0x84) ? c : '.')

void writel(u_int32 addr, u_int32 data);

void null_snprintf(char *buf, int size, char *fmt, ...);
void null_uartB(char *buf);

void fh_dacr();
void fh_memdump(u_int32 addr, u_int32 size);
void fh_enable_breakpoints();
void fh_apply_patches();
void fh_log_data(char *data, u_int32 size);
void fh_log_msg(char *msg);
void fh_dump_log();
void fh_disable_uart();

bp *fh_reproduce_breakpoints_and_recover_instruction(u_int32 *lr);
void fh_print_banner(firehorse *fh);
void fh_print_system_registers();

void set_fh_entry(void *x);

void *get_fh_entry();
void *get_fh_scratch();
void *get_fh_saved_regs();
void *get_fh_exception_sp();
void *get_fh_saved_regs8();
#endif