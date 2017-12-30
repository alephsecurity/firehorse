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


#define ADDR_UARTB_NULL         ADDR_CALLBACK(10) 
#define ADDR_SNPRINTF_NULL      ADDR_CALLBACK(11) 
#define ADDR_DPRINTF_NULL       (INVALID_PTR)

#define ADDR_DBG_ENTRY (0x14690000)

/* programmer */
#define ADDR_SNPRINTF_PROGRAMMER (void *)(0x140252B4)
#define ADDR_UARTB_PROGRAMMER    (void *)(0x14031CC0)

#define XMLHUNT_ADDR_START       (void *)(0x86028A00)
#define XMLHUNT_WRITE_BUFFER     (void *)(0x146B2000)

#define NUM_ENTRIES_PER_TABLE (512)

#define ADDR_FH_LOG_SIZE        (10)


#define ADDR_REMOTE_INIT(dst) (ADDR_REMOTE_CALLBACK(21, dst))

#endif