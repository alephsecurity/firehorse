/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _TARGET_CONSTANTS_H_
#define _TARGET_CONSTANTS_H_


/* firehorse */

#define ADDR_SCRATCH_OFFSET      (0x20000)
#define ADDR_EXCEPTION_SP_OFFSET (0x1FFF0)
#define ADDR_SAVED_REGS_OFFSET   (0x21000)

#define ADDR_SIZE (ADDR_SCRATCH_OFFSET + 0xA000)


#define ADDR_UARTB_NULL         (INVALID_PTR) 
#define ADDR_SNPRINTF_NULL      (INVALID_PTR)
#define ADDR_DPRINTF_NULL       (INVALID_PTR)

#define ADDR_REMOTE_INIT(dst) (ADDR_REMOTE_CALLBACK(1, dst))

#define ADDR_FH_ABOOT_REBASE    (0x8F900000)

#define ADDR_FH_LOG_SIZE        (2048)

/* pbl */

#define ADDR_PBL_BASE (void *)(0x100000)
#define ADDR_DISABLE_MMU_PBL (void *)(0x110004)


/* programmer */
#define ADDR_SNPRINTF_PROGRAMMER (void *)(0x800644D)
#define ADDR_UARTB_PROGRAMMER    (void *)(0x80131B1)

#define EGGHUNT_ADDR_START       (0x205000)
#define EGGHUNT_ADDR_END         (0x20F000)
#define EGGHUNT_FOUND_PARTS      (void *)(0x8093000)


/* sbl */

#define ADDR_SNPRINTF_SBL       (void *)(0x8005451)
#define ADDR_UARTB_SBL          (void *)(0x801F159)

/* aboot */

#define ADDR_SCRATCH_ADDR       (void *)(0xa3000000)
#define ADDR_SCRATCH_RAMDISK    (ADDR_SCRATCH_ADDR + 40*0x1000*1000)
#define ADDR_RAMDISK            (void *)(0x13600000)
#define ADDR_DPRINT_ABOOT              (void *)(0x8F646C38)
#define ADDR_PARTITION_GET_INDEX       (void *)(0x8F608434)
#define ADDR_PARTITION_GET_OFFSET      (void *)(0x8F608560)
#define ADDR_PARTITION_GET_LUN         (void *)(0x8F6085D8)
#define ADDR_MMC_SET_LUN               (void *)(0x8F610214)
#define ADDR_MMC_READ                  (void *)(0x8F60FB60)
#define ADDR_MMC_GET_DEVICE_BLOCKSIZE  (void *)(0x8F60F8D0)
#define ADDR_GET_SCRATCH_ADDRESS       (void *)(0x8F601288)

#define RAMDISK_SIZE            (2016526)

#endif