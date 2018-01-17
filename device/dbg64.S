//
// firehorse
// by Roee Hay & Noam Hadad, Aleph Research
//

#include "constants.h"

// This label will be used as the exception handler for aarch64 exceptions
// It saves the register state on the stack, and the passes the control to the dbg_entry function
dbg_entry64:
    STP             X30, X0, [SP,#-0x10]! 
    STP             X28, X29, [SP,#-0x10]! 
    STP             X26, X27, [SP,#-0x10]! 
    STP             X24, X25, [SP,#-0x10]! 
    STP             X22, X23, [SP,#-0x10]! 
    STP             X20, X21, [SP,#-0x10]! 
    STP             X18, X19, [SP,#-0x10]! 
    STP             X16, X17, [SP,#-0x10]! 
    STP             X14, X15, [SP,#-0x10]! 
    STP             X12, X13, [SP,#-0x10]! 
    STP             X10, X11, [SP,#-0x10]! 
    STP             X8, X9, [SP,#-0x10]! 
    STP             X6, X7, [SP,#-0x10]! 
    STP             X4, X5, [SP,#-0x10]! 
    STP             X2, X3, [SP,#-0x10]! 
    STP             X0, X1, [SP,#-0x10]! 
    LDR X0, =ADDR_DBG_ENTRY;
    BR X0



.global dbg_entry64
