//
// firehorse
// by Roee Hay & Noam Hadad, Aleph Research
//

#include "constants.h"

// All labels here will be used as the exception handlers 
// They all save the current registrs state to a known location,
// and then passes the control to the dbg function

dbg_data_abort_entry:
    MCR p15,0,R0,c13,c0,2;
    MCR p15,0,R1,c13,c0,4;
    MOV R1, LR
    BL get_fh_saved_regs8;
    MOV LR, R1
    STMIA R0!, {R2-R12};
    MOV R3, SP;
    STMIA R0!, {R3, LR};
    SUB R2, R0, #0x3C;
    MRC p15,0,R0,c13,c0,2;
    MRC p15,0,R1,c13,c0,4;
    STMIA R2, {R0, R1};
    BL get_fh_exception_sp;
    MOV SP, R0;
    MOV R0, #0;
    MOV R1, #0x5000;
    B dbg;

dbg_prefetch_abort_entry:
    MCR p15,0,R0,c13,c0,2;
    MCR p15,0,R1,c13,c0,4;
    MOV R1, LR
    BL get_fh_saved_regs8;
    MOV LR, R1
    STMIA R0!, {R2-R12};
    MOV R3, SP;
    STMIA R0!, {R3, LR};
    SUB R2, R0, #0x3C;
    MRC p15,0,R0,c13,c0,2;
    MRC p15,0,R1,c13,c0,4;
    STMIA R2, {R0, R1};
    BL get_fh_exception_sp;
    MOV SP, R0;
    MOV R0, #0;
    MOV R1, #0x6000;
    B dbg;

dbg_undef_inst_entry:
    MCR p15,0,R0,c13,c0,2;
    MCR p15,0,R1,c13,c0,4;
    MOV R1, LR
    BL get_fh_saved_regs8;
    MOV LR, R1
    STMIA R0!, {R2-R12};
    MOV R3, SP;
    STMIA R0!, {R3, LR};
    SUB R2, R0, #0x3C;
    MRC p15,0,R0,c13,c0,2;
    MRC p15,0,R1,c13,c0,4;
    STMIA R2, {R0, R1};
    BL get_fh_exception_sp;
    MOV SP, R0;
    MOV R0, #0;
    MOV R1, #0x3000;
    B dbg;

dbg_software_entry:
    MCR p15,0,R0,c13,c0,2;
    MCR p15,0,R1,c13,c0,4;
    MOV R1, LR
    BL get_fh_saved_regs8;
    MOV LR, R1
    STMIA R0!, {R2-R12};
    MOV R3, SP;
    STMIA R0!, {R3, LR};
    SUB R2, R0, #0x3C;
    MRC p15,0,R0,c13,c0,2;
    MRC p15,0,R1,c13,c0,4;
    STMIA R2, {R0, R1};
    BL get_fh_exception_sp;
    MOV SP, R0;
    MOV R0, #0;
    MOV R1, #0x4000;
    B dbg;

.global dbg_software_entry
.global dbg_undef_inst_entry
.global dbg_prefetch_abort_entry
.global dbg_data_abort_entry