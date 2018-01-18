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
import textwrap
import log as lg
from log import *
from cmd import *
import fw
from fh import *

def main():

    adjustLevels()

    parser = argparse.ArgumentParser(\
        prog="firehorse",
        usage="python firehorse.py -t TARGET_NAME [options] cmd [cmd_args]",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''\
                                target commands:
                                    magic                           causes the magic function in the target_TargetName.py file to be called -
                                                                    on nokia6 this will activate the secure boot exploit and the device will 
                                                                    boot with root adb access and SELinux in permissive mode
                                    rop                             executes a rop payload (different for every device)
                                    uart                            dumps uart buffer
                                    dump_pt                         dumps the programmer page table
                                    dump_pt32 [skip]                dumps the programmer page table (32 bit table format), if 'skip' is passed,
                                                                    skipps the first 'skip' entries in fisrt level PT
                                    dump_pt64                       dumps the programmer page table (64 bit table format)
                                    extract_pbl                     dumps the device pbl (to a file in the cwd)
                                    extract_modem_pbl               dumps the device modem_pbl (to a file in the cwd)
                                    extract_rpm_pbl                 dumps the device rpm_pbl (to a file in the cwd)
                                    read_partition name             dumps the partition specified by name (to a file in the cwd)
                                    write_partition name srcpath    overwrites the partition specified by name with the file specified by srcpath

                                fw commands:
                                    hello                           send programmer to device
                                    firehosep xml_path              send the xml specified in xml_path to the programmer
                                    upload file_path addr           upload the binary file specified by file path to the address addr in 32 bit chunks
                                    upload64 file_path addr         upload the binary file specified by file path to the address addr in 64 bit chunks
                                    sendfile file_path addr         upload the binary file specified by file path to the address addr (faster then upload)
                                    exec addr                       executes the code located at address addr - for 32 bit code
                                    exec64 addr                     executes the code located at address addr - for 64 bit code
                                    run file_path addr              uploads the file located at file_path to address addr and executes it - for normal arm code
                                    runt file_path addr             uploads the file located at file_path to address addr and executes it - for thumb code
                                    peek addr size [output_file]    reads size bytes from address addr and prints them to screen,if output_file is passed
                                                                    the output is written to file
                                    copy dst src size               copies size bytes from address src to address dst
                                    poke addr val                   writes 4 bytes of data specified by the hex value val at address addr
                                    
                                    
                                Usage examples:
                                    python firehorse.py -s -c COM17 -t nokia6 target magic
                                    python firehorse.py -c COM17 -t nokia6 fw hello
                                    python firehorse.py -c COM17 -t nokia6 fw peek 0x100000 0x10
                                '''))
    parser.add_argument('-c', '--com', dest='com', help='Specify COM port', default=constants.COM)
    parser.add_argument('-t', '--target', dest='target_name',
                        help='Specify target, can be one of the following: nokia6 | angler | ugglite | mido | cheeseburger', required=True)
    parser.add_argument('-s', '--hello', dest='hello', action='store_true',
                        help='send programmer to device - REQUIRED on the first time you use this tool after the device booted into EDL', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='Enable verbose logging')
    parser.add_argument('-vv', '--moreverbose', action='store_true', dest='moreverbose', help='Even more logging')
    parser.add_argument('cmd', nargs='*', help='Conduct command: fw ... | target ...')

    args = parser.parse_args()

    if args.verbose:
        lg.setVerbose()

    if args.moreverbose:
        lg.setVerbose(True)

    if not os.path.exists("../tmp"):
        os.mkdir("../tmp")
    try:
        target.set_target(args.target_name, args.com)
    except KeyError:
        E("unknown target")
        sys.exit(1)

    if args.hello:
        i = 0
        I('sending programmer...')
        while True:
            try:
                i += 1
                Framework.send_programmer()
                break
            except FirehorseDeviceNotConnectedException:
                time.sleep(1)
                if (i % 10) == 0:
                    I("device not connected, waiting.")
        time.sleep(1)

    name = args.cmd[0]
    args = args.cmd[1:]

    cmds = {'target': target.get().do_cmd, 'fw': fw.do_cmd}
    cmds[name](args)

    # t = target.get()
    # t.magic()
    # return 0

main()
