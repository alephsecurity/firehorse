/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _GLUE32_H_
#define _GLUE32_H_ 

#define GLUE_BODY(name) __asm__("\
        SUB SP, #0x14;\
        STM SP, {R0, R7, R8, LR};\
        BL get_fh_entry;\
        MOV R8, R0;\
        LDR R7, =" #name "_ptr;\
        LDR R7,[R8, R7];\
        STR  R7,[SP, #0x10];\
        LDM SP!, {R0, R7, R8, LR, PC}") 

#endif
