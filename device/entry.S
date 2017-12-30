//
// firehorse
// by Roee Hay & Noam Hadad, Aleph Research
//

start:
    B dbg
init_set_fh_entry:
    SUB r0, pc, #0xC
    B set_fh_entry;
    nop
scratch:
    nop
    nop
    nop
    nop

exports:
B dbg                       // CMD_DBG
B init                      // CMD_INIT_NO_SHOOK
B _shook_pagecopy           // CMD_PC
B 0                         // CMD_CB_TEST
B cb_sblpatcher             // CMD_CB_SBLPATCHER
B 0                         // CMD_CB_MEMDUMP
B 0                         // CMD_FLUSHTLB
B 0                         // CMD_DACR
B 0                         // CMD_DISABLEMMU
B dbg_undef_inst_entry      // CMD_DBG_INT
B fh_disable_uart           // CMD_DISABLE_UART
B cb_ablpatcher             // CMD_ABL_PATCHER
B dbg_data_abort_entry      // CMD_DBG_DATA_ABORT_ENTRY
B dbg_prefetch_abort_entry  // CMD_DBG_PREFETCH_ABORT_ENTRY
B dbg_software_entry        // CMD_DBG_SOFTWARE_ENTRY
B _shook_init               // CMD_INIT
B cb_before_linux           // CMD_BEFORE_LINUX
B 0                         // CMD_FORCE_FASTBOOT
B 0                         // CMD_INFINITE_LOOP
B _shook_pageremap          // CMD_PAGE_REMAP
B _shook_pblpatcher         // CMD_PBL_PATCHER
B 0                         // CMD_CB_READUSB
B cb_mmcread                // CMD_MMC_READ
B cb_bootlinux              // CMD_BOOTLINUX
B _shook_fhpatcher          // CMD_FH_PATCHER
B cb_disablejtag            // CMD_DISABLE_JTAG
B 0                         // CMD_DUMP_STRUCTS
B 0                         // CMD_MINI_SNPRINTF
B fh_log_msg                // CMD_FH_LOG

.global start
.global get_entry
.global init_set_fh_entry