/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "gluemacros.h"
#include "constants.h"

GLUE(uartB,                    ADDR_UARTB_PROGRAMMER,    void,               char *msg);
GLUE(snprintf,                 ADDR_SNPRINTF_PROGRAMMER, int,                char *buf, int size, char *fmt, ...);
GLUE(disablemmu,               INVALID_PTR,              void);
GLUE(dprintf,                  ADDR_DPRINTF_NULL,        void,               char *fmt, ...);
GLUE(partition_get_index,      INVALID_PTR,              int,                char *name);
GLUE(partition_get_offset,     INVALID_PTR,              unsigned long long, int index);
GLUE(partition_get_lun,        INVALID_PTR,              u_int8,             int offset);
GLUE(mmc_set_lun,              INVALID_PTR,              unsigned long long, u_int8 lun);
GLUE(mmc_read,                 INVALID_PTR,              void,               u_int64 data_addr, u_int32 *out, u_int32 data_len);
GLUE(mmc_get_device_blocksize, INVALID_PTR,              u_int32);
GLUE(get_scratch_address,      INVALID_PTR,              u_int32);
