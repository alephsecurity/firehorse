//
// firehorse
// by Roee Hay & Noam Hadad, Aleph Research
//

.align 3
get_currentel:
    mrs x0, CurrentEL
    ret


.align 3
get_elr_el1:
    mrs x0, ELR_EL1
    ret


.align 3
get_elr_el2:
    mrs x0, ELR_EL2
    ret


.align 3
get_elr_el3:
    mrs x0, ELR_EL3
    ret


.align 3
get_ttbr0_el1:
    mrs x0, TTBR0_EL1
    ret


.align 3
get_ttbr0_el2:
    mrs x0, TTBR0_EL2
    ret


.align 3
get_ttbr0_el3:
    mrs x0, TTBR0_EL3
    ret


.align 3
get_ttbr1_el1:
    mrs x0, TTBR1_EL1
    ret


.align 3
get_tcr_el1:
    mrs x0, TCR_EL1
    ret


.align 3
get_tcr_el2:
    mrs x0, TCR_EL2
    ret


.align 3
get_tcr_el3:
    mrs x0, TCR_EL3
    ret


.align 3
get_vbar_el1:
    mrs x0, VBAR_EL1
    ret


.align 3
get_vbar_el2:
    mrs x0, VBAR_EL2
    ret


.align 3
get_vbar_el3:
    mrs x0, VBAR_EL3
    ret


.align 3
get_daif:
    mrs x0, DAIF
    ret


.align 3
get_nzcv:
    mrs x0, NZCV
    ret


.align 3
get_spsel:
    mrs x0, SPSel
    ret


.align 3
get_rvbar_el3:
    mrs x0, RVBAR_EL3
    ret


.align 3
get_rvbar_el2:
    mrs x0, RVBAR_EL2
    ret


.align 3
get_rvbar_el1:
    mrs x0, RVBAR_EL1
    ret


.align 3
get_scr_el3:
    mrs x0, SCR_EL3
    ret


.align 3
get_sctlr_el3:
    mrs x0, SCTLR_EL3
    ret


.align 3
get_sctlr_el2:
    mrs x0, SCTLR_EL2
    ret


.align 3
get_sctlr_el1:
    mrs x0, SCTLR_EL1
    ret


.align 3
get_far_el1:
    mrs x0, FAR_EL1
    ret


.align 3
get_far_el2:
    mrs x0, FAR_EL2
    ret


.align 3
get_esr_el1:
    mrs x0, ESR_EL1
    ret


.align 3
get_esr_el2:
    mrs x0, ESR_EL2
    ret


.align 3
get_esr_el3:
    mrs x0, ESR_EL3
    ret


.align 3
enable_mmu:
    stp x30, x0, [sp, #-0x10]!
    bl flush_caches_el1_try2;
    mrs x0, SCTLR_EL1
    orr x0, x0, #1
    msr SCTLR_EL1, x0
    bl flush_caches_el1_try2;
    ldp  X30, X0, [SP],#0x10
    isb;
    ret


.align 3
flush_caches_el1_try2:
    ic	iallu;
    tlbi vmalle1is;
    dsb ish;


.align 3
flush_caches_el1:
	dsb sy;
    isb sy;
    tlbi vmalle1;
    dsb sy;
    isb sy;
    ic iallu;
    dsb sy;
    isb sy;
    ret;


.align 3
dbg_exit64:
    LDP             X0, X1, [SP],#0x10
    LDP             X2, X3, [SP],#0x10
    LDP             X4, X5, [SP],#0x10
    LDP             X6, X7, [SP],#0x10
    LDP             X8, X9, [SP],#0x10
    LDP             X10, X11, [SP],#0x10
    LDP             X12, X13, [SP],#0x10
    LDP             X14, X15, [SP],#0x10
    LDP             X16, X17, [SP],#0x10
    LDP             X18, X19, [SP],#0x10
    LDP             X20, X21, [SP],#0x10
    LDP             X22, X23, [SP],#0x10
    LDP             X24, X25, [SP],#0x10
    LDP             X26, X27, [SP],#0x10
    LDP             X28, X29, [SP],#0x10
    LDP             X30, X0, [SP],#0x10
    ERET


.align 3
invalidate_caches:
    ret


.align 3
asm_lsl:
    LSL X0, X0, X1;
    RET


.align 3
asm_lsr:
    LSR X0, X0, X1;
    RET


.global get_currentel
.global get_elr_el1
.global get_elr_el2
.global get_elr_el3
.global get_ttbr0_el1
.global get_ttbr0_el2
.global get_ttbr0_el3
.global get_ttbr1_el1
.global get_tcr_el1
.global get_tcr_el2
.global get_tcr_el3
.global get_vbar_el1
.global get_vbar_el2
.global get_vbar_el3
.global get_daif
.global get_spsel
.global get_nzcv
.global dbg_exit64
.global get_rvbar_el1
.global get_rvbar_el2
.global get_rvbar_el3
.global get_scr_el3
.global get_sctlr_el3
.global get_sctlr_el2
.global get_sctlr_el1
.global get_far_el1
.global get_far_el2
.global get_esr_el1
.global get_esr_el2
.global get_esr_el3
.global invalidate_caches
.global enable_mmu
.global flush_caches_el1
.global asm_lsl
.global asm_lsr