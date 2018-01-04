#
# firehrose
# By Roee Hay & Noam Hadad, Aleph Research
#

import target
        
target.add_target(name="oneplus3t", arch=64, 
             programmer_path=r"target/oneplus3t/prog_ufs_firehose_8996_ddr.elf", 
             peekpoke_style=1, 
             rawprogram_xml="target/oneplus3t/rawprogram.xml",
             ufs=True)