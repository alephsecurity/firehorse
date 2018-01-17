/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#define STACKHOOK_TARGET(name, target) \
__attribute__((naked))  void _shook_##name() \
{ \
    __asm__("STR x0, [SP, #-16]!;\
             ADR X1, .;\
             ADD X1, X1, #0x1C;\
             BLR X1;\
             LDR X0, [SP], #16;\
             LDR X2, =" #target ";\
             BR X2;"); \
} void name()
