#
# firehrose
# By Roee Hay & Noam Hadad, Aleph Research
#

# Default values - will be overridden by command line arguments
COM = None
FH_LOADER = None
SAHARA_SERVER = None

BP_MSG_LEN = 23
BP_FLAG_HALT = 1
BP_FLAG_ONCE = 2

MODE_PROGRAMMER = 0
MODE_PBL = 1
MODE_SBL = 2
MODE_ABL = 3

LOG_FILE_PATH = "firehorse.log"

CMD_PATH32 = "../device/entry.S"
CMD_PATH64 = "../device/entry64.S"
