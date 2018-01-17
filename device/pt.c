/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"


#define PT_GET_TYPE(x) (x & 3)

#define PT_FLD_GET_TYPE(x) (PT_GET_TYPE(x))
#define PT_SLD_GET_TYPE(x) (PT_GET_TYPE(x))

#define PT_FLD_TYPE_FAULT    (0)
#define PT_FLD_TYPE_PT       (1)
#define PT_FLD_TYPE_SECTION  (2)
#define PT_FLD_TYPE_RESERVED (3)


#define PT_SLD_TYPE_UNSUPPORTED   (0)
#define PT_SLD_TYPE_LP            (1)
#define PT_SLD_TYPE_XSP           (2)
#define PT_SLD_TYPE_XSP_WITH_NX   (3)

#define PT_FL_OFFSET(x) ((u_int32)x >> 20)
#define PT_SL_OFFSET(x) (((u_int32)x & 0xFF000)>>12)

/*
 * Returns the first level descriptor (page table entry) of the given virtual address
 */
u_int32 pt_get_first_level_descriptor(u_int32 *addr)
{
    u_int32 *base = (u_int32 *)get_ttbr0();
    return base[PT_FL_OFFSET(addr)];
}


/*
 * Returns the address of the second level descriptor (page table entry) for the given virtual address
 */
u_int32 *pt_get_second_level_descriptor_ptr(u_int32 *addr)
{
    u_int32 fl = pt_get_first_level_descriptor(addr);
    //assert PT_FLD_GET_TYPE(fl) == PT_FLD_TYPE_PT;
    u_int32 *base = (u_int32 *)((fl >> 10) << 10);
    return &base[PT_SL_OFFSET(addr)];
}


/*
 * Returns the second level descriptor (page table entry) of the given virtual address
 */
u_int32 pt_get_second_level_descriptor(u_int32 *addr)
{
    return *pt_get_second_level_descriptor_ptr(addr);
}


/*
 * Sets the second level descriptor (page table entry) of the given virtual address with the given value
 */
void pt_set_second_level_descriptor(u_int32 *addr, u_int32 val)
{
    u_int32 *sladdr = pt_get_second_level_descriptor_ptr(addr);
    *sladdr = val;
}


/*
 * Sets the second level descriptor (page table entry) of the given virtual address (va)
 * with the second level descriptor of another virtual address (new_va)
 */
void pt_second_level_xsmallpage_remap(u_int32 *va, u_int32 *new_va) 
{
    u_int32 new_sl = pt_get_second_level_descriptor(new_va);
    pt_set_second_level_descriptor(va, new_sl);
}
