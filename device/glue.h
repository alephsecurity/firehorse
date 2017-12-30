/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _GLUE_H_
#define _GLUE_H_

#include "gluemacros.h"

#include "constants.h"

#define GLUE_HEADER(name, ret, ...)  ret name(__VA_ARGS__); GLUE_PTR_GETTER_HEADER(name); GLUE_PTR_SETTER_HEADER(name);

GLUE_HEADER(uartB, void, char *msg)
GLUE_HEADER(snprintf, int, char *buf, int size, char *fmt, ...);
GLUE_HEADER(disablemmu, void);
GLUE_HEADER(dprintf, void, char *fmt, ...);
GLUE_HEADER(partition_get_index,  int, char *name);
GLUE_HEADER(partition_get_offset, unsigned long long, int index);
GLUE_HEADER(partition_get_lun, u_int8, int offset);
GLUE_HEADER(mmc_set_lun, unsigned long long, u_int8 lun);
GLUE_HEADER(mmc_read, void, u_int64 data_addr, u_int32 *out, u_int32 data_len);
GLUE_HEADER(mmc_get_device_blocksize, u_int32);
GLUE_HEADER(get_scratch_address, u_int32);

#endif