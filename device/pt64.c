/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "pt64.h"

u_int32 pt_get_index(u_int32 *va, u_int8 level);


/*
 * Sets entries in all levels of page table as writable for a given virtual address
 */
void pt64_set_attr_writable(u_int32 *va)
{
    u_int64 *next = get_ttbr0_el1();
    u_int8 level = 1;
    while (next != (u_int64 *)-1)
    {
        next = pt64_set_attr_writable_walk(next, va, level++);
    }
}


/*
 * Copy all attribuites in all levels of page table entries for one virtual address (dst_va) from the attributes of another virtual address (src_va)
 */
void pt64_copy_attr(u_int32 *dst_va, u_int32 *src_va)
{
    ASSERT(TCR_GET_T0SZ(get_tcr_el1())>=25 && TCR_GET_T0SZ(get_tcr_el1()))<=33, "unsupported tngz value");
    ASSERT(TCR_GET_TG0(get_tcr_el1())==0, "only supporting 4KB granule");
  
    u_int64 *src_ttbase, *dst_ttbase;
    u_int8 level = 1;
    u_int64 *src_entry, *dst_entry;
    u_int32 src_index, dst_index;    
    
    src_ttbase = get_ttbr0_el1();
    dst_ttbase = get_ttbr0_el1();

    for (level = 1; level <= 3; level++)
    {
        src_index = pt_get_index(src_va, level);
        dst_index = pt_get_index(dst_va, level);
        
        src_entry = &src_ttbase[src_index];
        dst_entry = &dst_ttbase[dst_index];

        *dst_entry = PT_SET_ATTR_OUTPUT(*src_entry, PT_GET_ATTR_OUTPUT(*dst_entry)>>12);

        src_ttbase = PT_GET_ATTR_OUTPUT(*src_entry);
        dst_ttbase = PT_GET_ATTR_OUTPUT(*dst_entry);
    }
}


/*
 * Returns the index of an entry in a certain level of the page table  
 */
u_int32 pt_get_index(u_int32 *va, u_int8 level)
{
    /* not tested */
    u_int32 maskbits = 37-TCR_GET_T0SZ(get_tcr_el1())+26-30+1;
    u_int32 mask = (2<<maskbits)-1;

    switch (level)
    {
        case 1:
            return ((u_int64)va >> 30) & mask;
        case 2:
            return ((u_int64)va >> 21) & 0x1FF;
        case 3:
            return ((u_int64)va >> 12) & 0x1FF;
    }

    /* shouldn't get here.. */
    return -1;
}


/*
 * Sets entry (in the specified level of the page table) of the given virtual address as writable 
 */
u_int64 *pt64_set_attr_writable_walk(u_int64 *base, u_int32 *va, u_int8 level)
{

    ASSERT(TCR_GET_T0SZ(get_tcr_el1())==28, "only supporting T0SZ==28");
    ASSERT(TCR_GET_TG0(get_tcr_el1())==0, "only supporting 4KB granule");
  

    u_int32 index = pt_get_index(va, level);


    D("pt64_handle_table base = %016x, level = %d, index = %08x", base, level, index);


    u_int64 e = base[index];


    u_int8 type = PT_GET_TYPE(e);

    pt64_dump(e);      
    PT_SET_ATTR_AP(&base[index], 0);

    e = base[index];
    pt64_dump(e);      

    if ((type == PT_TYPE_NONE) || (type == PT_TYPE_NONE2))
    {
        D("done with level %d (type is none)", level);
        return (u_int64 *)-1;
    }


    if ((type ==  PT_TYPE_TABLE) && (level < 3))
    {
        D("done with level %d (type is table)", level);
        return (u_int64 *)PT_GET_ATTR_OUTPUT(e);
    }
    
    D("done with level %d (type is none or level >= 3)", level);
    return (u_int64 *)-1;

 
}


void pt64_dump(u_int64 e)
{
        D("%016x TYPE=%d, OUTPUT=%016x AP=%x NS=%x SH=%x AF=%x NG=%x ATTRINDEX=%x PXN=%x XN=%x", e, PT_GET_TYPE(e),
            PT_GET_ATTR_OUTPUT(e),
            PT_GET_ATTR_AP(e),
            PT_GET_ATTR_NS(e),
            PT_GET_ATTR_SH(e),
            PT_GET_ATTR_AF(e),
            PT_GET_ATTR_NG(e),
            PT_GET_ATTR_ATTRINDEX(e),
            PT_GET_ATTR_PXN(e),
            PT_GET_ATTR_XN(e));   
}