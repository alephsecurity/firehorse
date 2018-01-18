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


def apply_breakpoints(m):
    cmd = Commands()

    m.bp_programmer(0x0802D3E4, msg="poke")
    m.break_function(MODE_PBL, "pbl_sahara")


def apply_patches(m, target):
    cmd = Commands()

    m.patch32_programmer(0x080094DC, 0xE51FF004) # LDR	 PC, [PC, #-4]
    m.patch32_programmer(0x080094E0, target.addr_callback(cmd.DBG_INT))

    m.patch32_programmer(0x080094E4, 0xE51FF004) # LDR	PC, [PC, #-4]
    m.patch32_programmer(0x080094E8, target.addr_callback(cmd.DBG_SOFTWARE_ENTRY))

    m.patch32_programmer(0x080094EC, 0xE51FF004) # LDR	PC, [PC, #-4]
    m.patch32_programmer(0x080094F0, target.addr_callback(cmd.DBG_DATA_ABORT_ENTRY))

    m.patch32_programmer(0x080243A0, 0xE51FF004) # LDR	PC, [PC, #-4]
    m.patch32_programmer(0x080243A4, target.addr_callback(cmd.DBG_PREFETCH_ABORT_ENTRY))


def magic():
    target = t.get()
    cmd = Commands()
    bbdb = BasicBlocks(target.basicblocks_db_pbl)
    bpm = BreakpointManager(bbdb)
    pm = PatchManager()

    I('applying patches and breakpoints...')
    apply_patches(pm, target)
    apply_breakpoints(bpm)

    I('creating pagecopy...')
    pages = set()
    pages.update(pm.get_pbl_page_numbers())
    pages.update(bpm.get_pbl_page_numbers())

    I('pages: ' + str(pages))
    pc = PageCopy(MODE_PBL, target.pbl_base_addr, target.pbl_copy_addr, pages,
                  target_pages=
                  [0x807D000, 0x807E000, 0x807F000, 0x807C000, 0x8068000, 0x806e000, 0x807B000])

    I('uploading firehorse data...')
    fh = Firehorse(pm, bpm, pc)
    fhdata = fh.pack()
    fhbin = file("../tmp/fh.bin", "wb")
    fhbin.write(fhdata)
    fhbin.close()

    xml_hunter = XMLHunter(fhdata, target.fh_base_programmer+target.fh_scratch_offset, target)
    xml_hunter.send()

    I('uploading firehorse..')
    xml_hunter = XMLHunter(file("../device/build/fh.payload", "rb").read(),
                           target.fh_base_programmer, target)
    xml_hunter.send()

    I('initializing firehorse...')
    FH_FW.exe_cmd(target.fh_base_programmer, cmd.INIT)

    # I('calling pbl patcher...')
    # FH_FW.exe_cmd(target.fh_base_programmer, cmd.PBL_PATCHER)


t.add_target(name="mido", arch=32, 
             programmer_path=r"target/mido/prog_emmc_firehose_8953_ddr.mbn",
             peekpoke_style=0,
             saved_lr=0x0803e65b,
             saved_lr_addr=0x8057ee4,
             pbl_base_addr=0x100000,
             pbl_copy_addr=0x8068000,
             page_table_base=0x200000,
             fh_base_programmer=0x0210000,
             fh_base_aboot=0x8f900000,
             fh_scratch_offset=0x4100,
             fh_saved_regs_offset=0x4000,
             egghunter_base=0x807e000,
             basicblocks_db_pbl="target/mido/pbl-mido-bbdb.txt",
             magic=magic,
             rawprogram_xml="target/mido/rawprogram0.xml",
             uart=0x806f880)
