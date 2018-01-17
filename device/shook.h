/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#define STACKHOOK_TARGET(name, target) \
__attribute__((naked))  void _shook_##name()  \
{ \
   __asm__("PUSH {R0};\
            ADD R1, PC, #0xC;\
            BLX R1; POP {R0};\
            LDR R2, =" #target ";\
            BX R2;"); \
} void name() 
