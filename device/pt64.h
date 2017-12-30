/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"

#ifndef _PT64_H_
#define _PT64_H_

#define PT_GET_TYPE(x) (x & 3)

#define PT_TYPE_NONE   (0)
#define PT_TYPE_BLOCK  (1)
#define PT_TYPE_NONE2   (2)
#define PT_TYPE_TABLE  (3)

#define PT_GET_ATTR_OUTPUT(x) ((((u_int64)x & 0xFFFFFFFFFFFF) >> 12) << 12)
#define PT_GET_ATTR_AP(x) ((x >> 6) & 3)
#define PT_GET_ATTR_NS(x) ((x >> 5) & 1)
#define PT_GET_ATTR_SH(x) ((x >> 8) & 3)
#define PT_GET_ATTR_AF(x) ((x >> 10) & 1)
#define PT_GET_ATTR_NG(x) ((x >> 11) & 1)
#define PT_GET_ATTR_ATTRINDEX(x) ((x >> 2) & 7)
#define PT_GET_ATTR_PXN(x) ((x >> 59) & 1)
#define PT_GET_ATTR_XN(x) ((x >> 60) & 1)
#define PT_GET_ATTR_APH(x) ((x >> 61) & 3)
#define PT_GET_ATTR_NSH(x) (x >> 63)

#define PT_SET_ATTR_AP(pentry, x) *pentry = ((*pentry & 0xFFFFFFFFFFFFFF3F) | x << 6)
#define PT_SET_ATTR_OUTPUT(entry,x) ((entry & 0xF000000000000FFF) | ((x & 0xFFFFFFFFFFFF) << 12))

#define TCR_GET_T0SZ(x) (x & 0x3F)
#define TCR_GET_TG0(x) ((x>>14) & 0x3)
#define TCR_GET_TG1(x) ((x>>30) & 0x3)
#define TCR_GET_IPS(x) ((x>>32) & 0x7)

void pt64_dump(u_int64 e);
void pt64_set_attr_writable(u_int32 *va);
u_int64 *pt64_set_attr_writable_walk(u_int64 *base, u_int32 *va, u_int8 level);
void pt64_copy_attr(u_int32 *dst_va, u_int32 *src_va);
#endif