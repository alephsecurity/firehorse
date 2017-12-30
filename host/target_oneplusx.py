#
# firehrose
# By Roee Hay & Noam Hadad, Aleph Research
#

import target


target.add_target(name="oneplusx", arch=32, 
             programmer_path=r"target/oneplusx/prog_emmc_firehose_8974.mbn", 
             peekpoke_style=0, 
             saved_lr=0x0803f28f,  saved_lr_addr = 0x8057ee4,
             pbl_base_addr=0xFC010000,
             page_table_base = 0x200000,
             basicblocks_db_pbl="target/oneplusx/pbl-oneplusx-bbdb.txt")