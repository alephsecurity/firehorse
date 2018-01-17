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
import log as lg
from log import *
from cmd import *
import fw
from fh import *

def main():


    adjustLevels()

    parser = argparse.ArgumentParser("firehorse")
    parser.add_argument('-c','--com', dest='com', help='Specify COM port', default=constants.COM)
    parser.add_argument('-t','--target', dest='target_name', help='Specify target', required=True)
    parser.add_argument('-s','--hello', dest='hello', action='store_true', help='', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='Enable verbose logging')
    parser.add_argument('-vv', '--moreverbose', action='store_true', dest='moreverbose', help='Even more logging')
    parser.add_argument('cmd', nargs='*',  help='Conduct command: fw ... | target ...')

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
        i=0
        I('sending programmer...')    
        while True:
            try:
                i+=1
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
