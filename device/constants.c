/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"

static void *addr_entry = (void *)0x66666666;

void set_fh_entry(void *x) { addr_entry = x; }

void *get_fh_entry()          { return addr_entry; }
void *get_fh_scratch()        { return addr_entry + ADDR_SCRATCH_OFFSET; } 
void *get_fh_saved_regs()     { return addr_entry + ADDR_SAVED_REGS_OFFSET; }
void *get_fh_exception_sp()   { return addr_entry + ADDR_EXCEPTION_SP_OFFSET; }
void *get_fh_saved_regs8()    { return addr_entry + ADDR_SAVED_REGS_OFFSET+8; }
