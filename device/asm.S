//
// firehorse
// by Roee Hay & Noam Hadad, Aleph Research
//

invalidate_data:
    DSB SY; ISB SY;
    MOV r0, #0;
_label1:
    MOV r1, #0;
_label2:
    ORR r2, r1, r0;
    //MCR p15, 0, r2, c7, c6, 2;
    MCR p15, 0, r2, c7, c14, 2;
    AND r1, r1, #0x40000000;
    CMP r1, #0;
    BNE _label2;
    ADD r0, r0, #0x20;
    CMP r0, #0x2000;
    BNE _label1;
    BX lr;


invalidate_inst:
    DSB SY; ISB SY;
    MOV r0, #0;
    MCR p15, 0, r0, c7, c5, 0;
    BX lr;


invalidate_tlb:
    DSB SY; ISB SY;
    MOV r0, #0;\
    MCR p15, 0, r0, c8, c6, 0;\
    MCR p15, 0, r0, c8, c5, 0;\
    MCR p15, 0, r0, c8, c7, 0;\
    DSB SY; ISB SY;
    BX lr;


invalidate_caches:
    MOV r3, lr;
    BL invalidate_data;
    BL invalidate_inst;
    BL invalidate_bp;
    BL invalidate_tlb;
    BX r3;


invalidate_bp:
    DSB SY; ISB SY;
    MOV r0, #0;
    MCR p15, 0, r0, c7, c5, 6;
    BX lr;

             
get_ttbr0:
    MRC p15,0,r0,c2,c0,0;
    BX lr;


get_ttbr1:
    MRC p15,0,r0,c2,c0,1;
    BX lr;


get_scr:
    MRC p15,0,r0,c1,c1,0
    BX lr;


get_nsacr:
    MRC p15,0,r0,c1,c1,2
    BX lr


get_vbar:
    MRC p15,0,r0,c12,c0,0
    BX lr


get_cpsr:
    MRS r0, CPSR
    BX lr


get_mvbar:
    MRC p15,0,r0,c12,c0,1
    BX lr


get_rmr:
    MRC p15,0,r0,c12,c0,2
    BX lr

    
disablemmu2:
    MRC             p15, 0, R0,c1,c0, 0;
    BIC             R0, R0, #1;
    MCR             p15, 0, R0,c1,c0, 0;
    MRC             p15, 0, R0,c1,c0, 0;
    BIC             R0, R0, #0x1000;
    BIC             R0, R0, #4;
    MCR             p15, 0, R0,c1,c0, 0;
    MOV             R0, #0;
    MCR             p15, 0, R0,c7,c5, 0;
    MOV             R0, #0;
    BX LR;

fh_dacr:
    MOV R0, #0xFFFFFFFF;
    MCR p15,0,R0,c3,c0,0;
    BX LR;

.global invalidate_data
.global invalidate_inst
.global invalidate_tlb
.global invalidate_bp
.global invalidate_caches
.global get_ttbr0
.global get_ttbr1
.global get_vbar
.global get_scr
.global get_mvbar
.global get_rmr
.global get_nsacr
.global get_cpsr
.global disablemmu2
.global fh_dacr
