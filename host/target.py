#
# firehrose
# By Roee Hay & Noam Hadad, Aleph Research
#

from log import *
import argparse
import fw

class Target:

    def __init__(self, name, arch, programmer_path, peekpoke_style, saved_lr=0, saved_lr_addr=0, 
                 pbl_base_addr=0, pbl_copy_addr=0, page_table_base=0, fh_base_programmer=0,
                 fh_base_aboot=0, fh_scratch_offset=0, fh_saved_regs_offset=0,
                 egghunter_found_parts=0, egghunter_base=0, egg_xml=None, 
                 basicblocks_db_pbl=None, magic=None, rop=None, uart=0, exe_addr=0, ttbr0_el1=0, pt_levels=1,
                 xmlhunter_part_size = 0, rawprogram_xml=None, ufs=False, modem_pbl_base_addr = 0,
                 rpm_pbl_base_addr = 0, tnsz = 0):

        self.name = name
        self.arch = arch
        self.programmer_name = programmer_path.split("\\")[-1]
        self.programmer_search_path = "\\".join(programmer_path.split("\\")[:-1])
        self.peekpoke_style = peekpoke_style
        self.saved_lr = saved_lr
        self.saved_lr_addr = saved_lr_addr
        self.pbl_base_addr = pbl_base_addr
        self.pbl_copy_addr = pbl_copy_addr
        self.fh_base_programmer = fh_base_programmer
        self.fh_base_aboot = fh_base_aboot
        self.fh_scratch_offset = fh_scratch_offset
        self.fh_saved_regs_offset = fh_saved_regs_offset
        self.basicblocks_db_pbl = basicblocks_db_pbl
        self.page_table_base = page_table_base
        self.tnsz = tnsz
        self.egghunter_found_parts = egghunter_found_parts
        self.egghunter_base = egghunter_base
        self.egg_xml = egg_xml
        self.magic = magic
        self.rop = rop
        self.uart = uart
        self.rawprogram_xml = rawprogram_xml
        self.ufs = ufs
        self.pt_levels = pt_levels
        self.com = None
        self.xmlhunter_part_size = xmlhunter_part_size

        self.modem_pbl_base_addr = modem_pbl_base_addr
        self.rpm_pbl_base_addr = rpm_pbl_base_addr

        self.exe_addr = exe_addr
        if 0 == exe_addr:
            self.exe_addr = saved_lr_addr
        
        

        if peekpoke_style == 0:
            self.peek_xml = 'peek0.xml' 
            self.poke_xml = 'poke0.xml' 
            self.xmlhunter_xml = 'xmlhunter0.xml'
        elif peekpoke_style == 1:
            self.peek_xml = 'peek1.xml' 
            self.poke_xml = 'poke1.xml' 
            self.xmlhunter_xml = 'xmlhunter1.xml'


    def do_cmd(self, args):

        if args[0] == 'magic':
            if None == self.magic:
                raise NotImplementedError()             
            self.magic()

        if args[0] == 'rop':
            if None == self.rop:
                raise NotImplementedError()    
            self.rop()

        if args[0] == "uart":
            self.read_uart()

        if args[0] == "dump_pt":
            self.dump_pt(self.arch)

        if args[0] == "dump_pt32":

            if len(args) > 1:
                skip = int(args[1])
            self.dump_pt(32, skip)

        if args[0] == "dump_pt64":
            self.dump_pt(64)

        if args[0] == "extract_pbl":
            self.extract_pbl()

        if args[0] == "extract_modem_pbl":
            self.extract_modem_pbl()

        if args[0] == "extract_rpm_pbl":
            self.extract_rpm_pbl()

        if args[0] == "read_partition":
            if None == self.rawprogram_xml:
                raise NotImplementedError()
            
            fw.Framework.read_partition(args[1])
        
        if args[0] == "write_partition":
            if None == self.rawprogram_xml:
                raise NotImplementedError()
            
            fw.Framework.write_partition(args[1], args[2])

    def extract_pbl(self):
        if 0 == self.pbl_base_addr:
            raise NotImplementedError()

        f = file("%s-pbl-%x.bin" % (self.name, self.pbl_base_addr) , "wb")
        f.write(fw.Framework.peek(self.pbl_base_addr,0x18000))
        f.close()

    def extract_modem_pbl(self):
        if 0 == self.modem_pbl_base_addr:
            raise NotImplementedError()

        f = file("%s-modempbl-%x.bin" % (self.name, self.modem_pbl_base_addr) , "wb")
        f.write(fw.Framework.peek(self.modem_pbl_base_addr,0xc000))
        f.close()
        
    def extract_rpm_pbl(self):
        if 0 == self.rpm_pbl_base_addr:
            raise NotImplementedError()

        f = file("%s-rpmpbl-%x.bin" % (self.name, self.rpm_pbl_base_addr) , "wb")
        f.write(fw.Framework.peek(self.rpm_pbl_base_addr,0x4000))
        f.close()
        

    def read_uart(self):
        if 0 == self.uart:
            raise NotImplementedError()
        
        I("Reading UART from %016lx", self.uart)
        for d in fw.Framework.gen_string(self.uart):
            sys.stdout.write(d)

    def dump_pt(self, arch, skip=0):
        if 0 == self.page_table_base:
            raise NotImplementedError()

        if arch == 32:
            fw.Framework.pt32_walk(self.page_table_base, skip)    
        else:
            fw.Framework.pt64_walk(self.page_table_base, self.tnsz, self.pt_levels)

    def addr_callback(self, n, base=None):

        if base == None:
            base = self.fh_base_programmer

        if self.arch == 32:
            return base+0x20+n*4
        
        return base+0x30+n*8

current_target = None
all_targets = {}

def add_target(**kwargs):
    t = Target(**kwargs)
    all_targets[t.name] = t

def set_target(name, com):
    global current_target
    current_target = all_targets[name]
    current_target.com = com


def get():
    return current_target

import target_mido
import target_angler
import target_nokia6
import target_ugglite
import target_cheeseburger
import target_oneplusx
import target_oneplus3t