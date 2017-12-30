start:
B dbg64entry
.align 3
init_set_fh_entry:
    adr x0, .;
    sub x0, x0, #8;
    B set_fh_entry;
.align 4 // offset: 0x20
scratch:
    nop
    nop
    nop
    nop

.align 4
exports: // offset: 0x30
B dbg64                     // CMD_DBG
.align 3
B _shook_init               // CMD_INIT
.global start
.global init_set_fh_entry