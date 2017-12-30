#
# firehrose
# By Roee Hay & Noam Hadad, Aleph Research
#

import time
import re
import sys
import binascii

import target
import argparse
import subprocess
import os
import struct
import pt
import pt64
from constants import *
from log import *
import target as trgt

pr = None

class FirehorseException(Exception): pass
class FirehorseCannotFindProgramException(FirehorseException): pass
class FirehorseDeviceNotConnectedException(FirehorseException): pass
class FirehorseSendProgrammerException(FirehorseException): pass

class Framework:
    
    poke_xml, peek_xml, xmlhunter_xml, rawprogram_xml_path = (None, None, None, None)

    @staticmethod 
    def get_peek_xml():
        if not Framework.peek_xml:
            Framework.peek_xml =  file(target.get().peek_xml).read()

        return Framework.peek_xml

    @staticmethod 
    def get_xmlhunter_xml():
        if not Framework.xmlhunter_xml:
            Framework.xmlhunter_xml =  file(target.get().xmlhunter_xml).read()

        return Framework.xmlhunter_xml

    @staticmethod 
    def get_poke_xml():
        if not Framework.poke_xml:
            Framework.poke_xml =  file(target.get().poke_xml).read()

        return Framework.poke_xml

    @staticmethod
    def get_rawprogram_xml_path():
        if not Framework.rawprogram_xml_path:
            Framework.rawprogram_xml_path = target.get().rawprogram_xml

        return Framework.rawprogram_xml_path

    @staticmethod
    def peek(addr, size):
        d = Framework.get_peek_xml().replace("ADDR",hex(addr).replace("L","")).replace("SIZE", hex(size).replace("L",""))
        data = Framework.firehose(d)
        output = ""
        for l in data:
            if not l.startswith("0x"):
                continue
            output += binascii.unhexlify(l.replace(" ","").replace("0x", ""))
        
        return output

    @staticmethod
    def poke(addr, size, value, print_data= False):
        T("Poking %08x = %08x", addr, value)
        d = Framework.get_poke_xml().replace("ADDR",hex(addr).replace("L","")).replace("SIZE", hex(size).replace("L","")).replace("VALUE", hex(value).replace("L",""))
        data = Framework.firehose(d)
        if print_data:
            for x in data:
                I("%s" % x)

    @staticmethod
    def poke_payload(addr, size, value, payload, print_data= False):

        d =  Framework.get_xmlhunter_xml().replace("ADDR",hex(addr).replace("L","")).replace("SIZE", hex(size).replace("L","")).replace("VALUE", hex(value).replace("L","")).replace("PAYLOAD", payload)
        data = Framework.firehose(d)
        if print_data:
            for x in data:
                I("%s" % x)

    @staticmethod
    def read_program_for_partition(name):
        from xml.dom import minidom
        xml = minidom.parse(Framework.get_rawprogram_xml_path())
        items = xml.getElementsByTagName("program")
        for i in items:
            if i.attributes["label"].value == name:
                return i
        
        return None
    

    @staticmethod
    def read_partition(name):
        program = Framework.read_program_for_partition(name)
        if None == program:
            raise FirehorseCannotFindProgramException()

        filename = "%s-%s-read.bin" % (target.get().name, name)
        program.attributes["filename"] = filename
        program.tagName = "read"

        D("read program = %s", program.toxml())

        I("Downloading partition %s to %s...", name, filename)
        
        f = file(filename, "wb")
        f.close()

        xml = "<?xml version=\"1.0\" ?>\n"
        xml += "<data>\n"
        if target.get().ufs:
            xml += "<configure MemoryName=\"ufs\" />"
        xml += program.toxml() + "\n"
        xml += "</data>\n"
        Framework.firehose(xml)

    @staticmethod
    def write_partition(name, srcpath):
        program = Framework.read_program_for_partition(name)
        if None == program:
            raise FirehorseCannotFindProgramException()

        from shutil import copyfile
        import os

        srcname = os.path.basename(srcpath)
        dstpath = os.path.join("../tmp", srcname)

        copyfile(srcpath, dstpath)

        program.attributes["filename"] = srcname

        D("write program = %s", program.toxml())

        I("Overwriting partition %s with %s...", name, dstpath)


        xml = "<?xml version=\"1.0\" ?>\n"
        xml += "<data>\n"
        if target.get().ufs:
            xml += "<configure MemoryName=\"ufs\" />"

        xml += program.toxml() + "\n"
        xml += "</data>\n"
        Framework.firehose(xml)


    @staticmethod
    def peek32(addr):
        return struct.unpack("<L", Framework.peek(addr, 4))[0]

    @staticmethod
    def gen_string(addr):
        out = ""        
        i = 0
        idx = -1
        while idx == -1:
            data = Framework.peek(addr+i*0x1000, 0x1000)
            idx = data.find('\x00')
            yield data[:idx]
            i+=1

    @staticmethod
    def poke32(addr, value, print_data = False):
        Framework.poke(addr, 4, value, print_data)

    @staticmethod
    def poke64(addr, value, print_data = False):
        Framework.poke(addr, 8, value, print_data)

    @staticmethod
    def poke_blob(addr, blob):
        i = 0
        
        blob += b"\x00"*(4-len(blob)%4)
        while i < len(blob):
            I(hex(addr+i))
            Framework.poke32(addr + i, struct.unpack("<L", blob[i:i+4])[0])
            i = i+4

    @staticmethod
    def poke_blob64(addr, blob):
        i = 0

        rm = len(blob) % 8
        if rm != 0:
            D('fetching %d remaining bytes from %x' % ((8 - rm), addr+len(blob)))
            d = Framework.peek(addr + len(blob), 8 - rm)
            blob += d
            T(Framework.hexdump(d))

        #blob += b"\x00"*(8-len(blob)%8)
        
        while i < len(blob):
            D("%08x %d %i" % (addr+i, len(blob)-i, i))
            Framework.poke64(addr + i, struct.unpack("<Q", blob[i:i+8])[0])
            i = i+8
    
    @staticmethod
    def copy(dst, src, size):
        data = Framework.peek(src, size)
        data += b"\x00"*(8-len(data)%8)
        i = 0
        while i < size:
            n = struct.unpack("<Q",data[i:i+8])[0]
            I("dst %x, n=%x" % (dst+i, n))
            Framework.poke(dst+i, 8, n)
            i+=8

    @staticmethod
    def copy_and_rebase(dst, src, size):
        data = Framework.peek(src, size)
        data += b"\x00"*(8-len(data)%8)
        i = 0
        while i < size:
            n = struct.unpack("<Q",data[i:i+8])[0]
            if n > src and n < (src + size):
                I("dst %x, n=%x" % (dst+i, n))
                Framework.poke(dst+i, 8, n + (dst-src))
            else:
                Framework.poke(dst+i, 8, n)
            i+=8
    
    @staticmethod
    def sendfile(path, addr, offset = 0, size = -1):
        Framework.senddata(file(path,"rb").read(), addr, offset, size)
        
    @staticmethod
    def senddata(blob, addr, offset = 0, size = -1):
            
        blob = blob[offset:]
        
        if size != -1:
            blob = blob[:size]
                
        
        blob += b"\x00"*(8-len(blob)%8)
        i = 0
        while i < len(blob):
            I("%08x" % (addr+i))
            xml = "<?xml version=\"1.0\" ?>\n<data>"
            
            for j in xrange(497):

                if target.get().peekpoke_style == 0:
                    xml +="<poke address64=\"0x%08x\" SizeInBytes=\"0x8\" value=\"0x%08x\"/>\n" % (addr+i, struct.unpack("<Q", blob[i:i+8])[0])
                else:
                    xml +="<poke address64=\"0x%08x\" size_in_bytes=\"0x8\" value64=\"0x%08x\"/>\n" % (addr+i, struct.unpack("<Q", blob[i:i+8])[0])
                i = i+8  
                
                if i >= len(blob):
                    break
                
            xml += "</data>"
            Framework.firehose(xml)               
        

    @staticmethod
    def firehose(xmldata):
        f = file("../tmp/temp.xml","wb")
        f.write(xmldata)
        f.close()
        target_out = []
        return Framework.firehosep("../tmp/temp.xml")        
    
    @staticmethod
    def exe(va):
        Framework.poke(target.get().exe_addr, 4, va)

    @staticmethod
    def exe_cmd(base, cmd):
       D('Executing %08x', base+0x20+cmd*4)
       Framework.poke(target.get().exe_addr, 4, base+0x20+cmd*4)

    @staticmethod
    def exe64(va):
        D("Executing %08x", va)
        Framework.poke64(target.get().exe_addr, va)
    
    @staticmethod
    def exe64_cmd(base, cmd):
        D('Executing %016lx', base+0x30+cmd*8)
        Framework.poke64(target.get().exe_addr, base+0x30+cmd*8)

    @staticmethod
    def send_programmer():
        t = target.get()
        out = subprocess.Popen([SAHARA_SERVER, "-p", r"\\.\%s" % t.com, "-s", "13:%s" % t.programmer_name, "-b", "%s\\" % t.programmer_search_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate("\n")
        if not "transferred successfully" in out[0]:
            if "Could not connect" in out[0]:
                raise FirehorseDeviceNotConnectedException()

            raise FirehorseSendProgrammerException()

    @staticmethod
    def firehosep(path):
        target_out = []
        search = "/".join(path.split("/")[:-1])
        filename = path.split("/")[-1]
        p = subprocess.Popen([FH_LOADER, r"--search_path=" + search, r"--port=\\.\%s" % target.get().com, "--sendxml=%s" % filename], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        out = p.communicate("\n")

        if "There is a chance your target is in SAHARA mode!!" in out[0]:
            p.kill()
            raise FirehorseSendProgrammerException()
            
        for l in out[0].split("\r\n"):
            T("FIREHOSE: %s", l)
            if None == l:
                continue
            if "ERROR: Failed to open com port" in l:
                raise FirehorseDeviceNotConnectedException()
            m = re.search(r".*TARGET SAID:\s*'(.*)'.*", l)
            if m:
                target_out.append(m.group(1))
        return target_out

    @staticmethod
    def upload(va, path):
        Framework.poke_blob(va, file(path, "rb").read())

    @staticmethod
    def upload64(va, path):
        Framework.poke_blob64(va, file(path, "rb").read())

    @staticmethod
    def pt_get_fl(base, va):
        return Framework.peek32(base+(va>>18))

    @staticmethod
    def pt_get_sl(base, va):
        fl = pt.get_fld(pt_get_fl(base, va & 0xFFF00000))
        sl_va = fl.coarse_base + ((va & 0xFF000)>>10)
        return (sl_va, Framework.peek32(sl_va))

    @staticmethod
    def pt_set_fl(base, va, x):
        Framework.poke32(base+(va>>18), x)

    @staticmethod
    def pt_set_fl_attr(base, va, attr):
        pt_set_fl(base, va, ((pt_get_fl(base, va) >> 10) << 10) | attr)

    @staticmethod
    def pt_set_fl_section_nx_off(base, va):
        pt_set_fl(base, va, pt_get_fl(base, va) & ~16)

    @staticmethod
    def pt_set_sl_xsmallpage_nx_off(base, va):
        addr, sl = pt_get_sl(base, va)
        newsl = sl & 0xFFFFFFFE
        Framework.poke32(addr, newsl)

    @staticmethod
    def pt_set_sl_xsmallpage_apx_off(base, va):
        addr, sl = pt_get_sl(base, va)
        newsl = sl & 0xFFFFFDFF
        newsl = newsl | 0x140
        newsl = newsl & 0xFFFFFFF7
        Framework.poke32(addr, newsl)

    @staticmethod
    def pt_set_sl_xsmallpage_attributes(base, va, attributes):
        addr, sl = pt_get_sl(base, va)
        newsl = sl & 0xFFFFF000
        newsl = newsl | attributes
        Framework.poke32(addr, newsl)

    @staticmethod
    def pt_set_sl_xsmallpage_remap(base, va, new_va):
        addr, sl = pt_get_sl(base, va)
        newaddr, newsl = pt_get_sl(base, new_va)
        Framework.poke32(addr, newsl)    
        
    @staticmethod
    def pt_set_fl_section_remap(base, va, new_va):
        fl = pt_get_fl(base, new_va)
        pt_set_fl(base, va, fl)
       
    @staticmethod
    def pt64_walk(ttbr, tnsz, levels = 3):
        I("Dumping page tables (levels=%d)", levels)
        I("First level (ptbase = %016x)", ttbr)
        I("---------------------------------------------")
        fl = Framework.peek(ttbr, 0x1000)

        if levels <= 1:
            return
            
        for (va,fle) in pt64.parse_pt(fl, 0, tnsz, 1):
            if "TABLE" in str(fle):
                I("Second level (ptbase = %016x)" % fle.output)
                I("---------------------------------------------")

                sl = Framework.peek(fle.output, 0x4000)
                sl = pt64.parse_pt(sl, va, tnsz, 2)

                if levels <=2:
                    continue

                for (va, sle) in sl:
                    if "TABLE" in str(sle):
                        I("Third level (ptbase = %016x)" % sle.output)
                        I("---------------------------------------------")
                        tl = Framework.peek(sle.output, 0x1000)
                        pt64.parse_pt(tl, va, tnsz, 3)

               
    @staticmethod
    def pt32_walk(ttbr, skip):
        I("First level (va = %08x)", ttbr)
        I("---------------------------------------------")
        fl = Framework.peek(ttbr, 0x4000)
            
        i = 0
        for (va, fl) in pt.parse_pt(fl):
            i+=1
            if i <= skip:
                continue
            if type(fl) == pt.pt_desc:
                I("")
                I("Second level (va = %08x)", va)
                I("---------------------------------------------")
                sldata = Framework.peek(fl.coarse_base, 0x400)
                pt.parse_spt(sldata, va)
               
                    
                                
            
            
    @staticmethod
    def hexdump(src, length=16, base=0):

        format = "%08x  %-*s  %s\n"
        if target.get().arch == 64:
            format = "%016lx  %-*s  %s\n"

        FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
        lines = []
        for c in xrange(0, len(src), length):
            chars = src[c:c+length]
            hex = ' '.join(["%02x" % ord(x) for x in chars])
            printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
            lines.append(format % (c+base, length*3, hex, printable))
        return ''.join(lines)


def do_cmd(args):


    argv1, argv0, argv1, argv2, argv3 = (None,None,None,None, None)


    if len(args) > 0:
        argv0 = args[0]

    if len(args) > 1:
        argv1 = args[1]

    if len(args) > 2:
        argv2 = args[2]

    if len(args) > 3:
        argv3 = args[3]

    if argv0 == "hello":
        Framework.send_programmer()
        return 
    if argv0 == "firehosep":
        Framework.firehosep(argv1)
        return 

    if argv0 == "upload":
        Framework.upload(int(argv2,16), argv1)
        return
        
    if argv0 == "upload64":
        Framework.upload64(int(argv2,16), argv1)
        return
        
    if argv0 == "exec":
        Framework.exe(int(argv1,16))
        return

    if argv0 == "run":
        print 'uploading...'
        Framework.upload(int(argv2,16), argv1)
        print 'executing...'
        Framework.exe(int(argv2,16))
        return

    if argv0 == "runt":
        print 'uploading...'
        Framework.upload(int(argv2,16), argv1)
        print 'executing...'
        Framework.exe(int(argv2,16)+1)
        return

    if argv0 == "peek":
        addr = int(argv1,16)
        size = int(argv2,16)
        data = Framework.peek(addr, size)
        if len(args) > 3:
            f = file(argv3, "wb")
            f.write(data)
            f.close()
            I("Wrote %s", argv3)
            return

        I(Framework.hexdump(data, base=addr))
        return


    if argv0 == "exe64":
        Framework.exe64(int(argv1,16))
        I("ok")
        return

    if argv0 == "copy":
        Framework.copy(int(argv1,16),int(argv2,16), int(argv3,16))
        return

    if argv0 == "poke":
        Framework.poke(int(argv1,16), 4, int(argv2,16))
        return

    if argv0 == "sendfile":    
        sendfile(argv1, int(argv2,16))
    


if __name__ == "__main__":
    main()
