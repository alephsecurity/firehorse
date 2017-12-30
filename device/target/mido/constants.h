/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _TARGET_CONSTANTS_H_
#define _TARGET_CONSTANTS_H_


/* firehorse */

#define ADDR_SCRATCH_OFFSET      (0x4100) //  0x20000)
#define ADDR_EXCEPTION_SP_OFFSET (0x3FF0) // (0x2FFF0)
#define ADDR_SAVED_REGS_OFFSET   (0x4000)

#define ADDR_SIZE (ADDR_SCRATCH_OFFSET + 0xA000)


#define ADDR_UARTB_NULL         (INVALID_PTR) 
#define ADDR_SNPRINTF_NULL      (INVALID_PTR)
#define ADDR_DPRINTF_NULL       (INVALID_PTR)

#define ADDR_FH_LOG_SIZE        (10)

#define ADDR_REMOTE_INIT(dst) (ADDR_REMOTE_CALLBACK(1, dst))


/* pbl */

#define ADDR_PBL_BASE (void *)(0x100000)

/* programmer */
#define ADDR_SNPRINTF_PROGRAMMER (void *)(0x08006489)
#define ADDR_UARTB_PROGRAMMER    (void *)(0x08021861)

#define XMLHUNT_ADDR_START       (void *)(0x8069A20)
#define XMLHUNT_WRITE_BUFFER     (0)


#endif