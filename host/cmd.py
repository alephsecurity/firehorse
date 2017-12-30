#
# firehrose
# By Roee Hay & Noam Hadad, Aleph Research
#

import re
import constants
import target
from log import *

class Commands:

    def __init__(self):
        self.cmds = {}

        t = target.get()

        if t.arch == 32:
            data = file(constants.CMD_PATH32,"rb").read()
        else:
            data = file(constants.CMD_PATH64,"rb").read()
            
        i = 0
        found_export = False
        for line in data.split("\n"):
            if "exports:" in line:
                found_export = True
                continue
            if found_export == False:
                continue    

            cmdmatch = re.match(r"B\s+.*?// CMD_([a-zA-Z0-9_]+)", line)

            if not cmdmatch:
#                i+=1
                continue

 #           print (cmdmatch.group(1), i)
            self.cmds[cmdmatch.group(1)] = i
            i+=1

    def get_cmd(self, name):
        return self.cmds[name]

    def __getattr__(self, name):
        D("%s = %d", name, self.get_cmd(name))
        return self.get_cmd(name)
