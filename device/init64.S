//
// firehorse
// by Roee Hay & Noam Hadad, Aleph Research
//

start:
B _shook_init
init_set_fh_entry:
    adr x0, .;
    sub x0, x0, #4;
    B set_fh_entry; 

scratch:
    nop
    nop
    nop
    nop

.global start
.global init_set_fh_entry