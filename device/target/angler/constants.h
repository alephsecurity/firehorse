/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _TARGET_CONSTANTS_H_
#define _TARGET_CONSTANTS_H_

/* firehorse */

#define ADDR_SCRATCH_OFFSET      (0xc000)
#define ADDR_EXCEPTION_SP_OFFSET (0)
#define ADDR_SAVED_REGS_OFFSET   (0)

#define ADDR_SIZE (ADDR_SCRATCH_OFFSET + 0xA000)

#define ADDR_UARTB_NULL         ADDR_CALLBACK(10) 
#define ADDR_SNPRINTF_NULL      ADDR_CALLBACK(11) 
#define ADDR_DPRINTF_NULL       (INVALID_PTR)

#define ADDR_REMOTE_INIT(dst) (ADDR_REMOTE_CALLBACK(21, dst))

#define ADDR_FH_ABOOT_REBASE    (0)


/* pbl */

#define ADDR_PBL_BASE (void *)(0)
#define ADDR_DISABLE_MMU_PBL (void *)(0)


/* programmer */
#define ADDR_SNPRINTF_PROGRAMMER (void *)(0xF803CB20)
#define ADDR_UARTB_PROGRAMMER    (void *)(0xF800D840)

#define ADDR_DBG_ENTRY (0xfe824000)
#define ADDR_FH_LOG_SIZE        (10)


#endif