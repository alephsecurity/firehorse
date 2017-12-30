/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "stdlib.h"
#include "fh.h"

#ifdef UART_ON
#define EE(buf) uartB(buf)
#define E(fmt, ...) { char buf[150]; snprintf(buf, sizeof(buf)-1, fmt, __VA_ARGS__); uartB(buf); }
#else
#define EE(buf)
#define E(fmt, ...)
#endif


u_int64 asm_lsl(u_int64, u_int64);
u_int64 asm_lsr(u_int64, u_int64);

u_int64 lsl(u_int64, u_int64);
u_int64 lsr(u_int64, u_int64);

void memcpy(void *dst, const void *src, size_t size)
{
    while (size-- > 0)
    {
        ((char *)dst)[size] = ((char *)src)[size];
    }
}

    
void memset(void *dst, int c, size_t n)
{
    while (n-- > 0)
    {
        ((char *)dst)[n] = (char)c;
    }
}

    
void codecpy(void *dst, const void *src, size_t size)
{
    memcpy(dst, src, size);
    invalidate_caches();
}


void writel(u_int32 addr, u_int32 data)
{
   *(u_int32 *)(addr) = data;
}

u_int32 mod(u_int32 n, u_int32 m)
{
    if (m == 0)
    {
        return 0;
    }
    while (n >= m)
    {
        n -= m;
    }
    return n;
}

u_int32 div(u_int32 n, u_int32 d)
{
    u_int32 i = 0;

    if (d == 0)
    {
        return 0;
    }
    while (n >= d)
    {
        n -= d;
        i++;
    }
    return i;
}

#ifdef NEED_ALIGNMENT

void memcpya(void *dst, const void *src, size_t size)
{
    while (size-- > 0)
    {
        w8a(&((char *)dst)[size], r8a(&((char *)src)[size]));
    }
}


u_int64 r64a(u_int8 *buf)
{
    u_int64 n1 = 8-(u_int64)(buf)%8;
    u_int64 n2 = 8-n1;

    u_int64 w1 =*(u_int64 *)(buf-n2);
    u_int64 w2 =*(u_int64 *)(buf+n1);

    u_int64 s1 = n1*8;
    u_int64 s2 = n2*8;

    u_int64 mask = lsl(1, s1)-1;
    u_int64 x1 = lsr(w1, s2);
    u_int64 x2 = lsl(w2, s1);
    u_int64 out = x1 | x2;

    return out;
}
u_int32 r32a(u_int8 *buf)
{
    u_int64 x = r64a(buf);
    u_int64 nx = lsr(lsl(x,32),32);

    return nx;
}
u_int16 r16a(u_int8 *buf)
{
    return lsr(lsl(r64a(buf),48),48);
}

u_int8 r8a(u_int8 *buf)
{
    return lsr(lsl(r64a(buf),56),56);
}
void w64a(u_int8 *buf, u_int64 x)
{
    u_int8 n1 = 8 - ((u_int8)(buf) % 8);
    u_int8 n2 = 8 - n1; 

    u_int8 s1 = 8*n1;
    u_int8 s2 = 8*n2;

    u_int64 x1 = lsl(x, s2);
    u_int64 x2 = lsr(x, s1);


    u_int64 orig1 = lsr(lsl((*(u_int64 *)(buf-n2)), s1), s1);
    u_int64 orig2 = lsl(lsr((*(u_int64 *)(buf-n2+8)), s2), s2);

    *(u_int64 *)(buf-n2) = orig1 | x1;
    *(u_int64 *)(buf-n2+8) = orig2  | x2;
}

void w32a(u_int8 *buf, u_int32 x)
{
    u_int64 orig = r64a(buf);

    u_int64 new = (lsl(lsr(orig,32),32))|(u_int64)x;

    w64a(buf, (lsl(lsr(orig,32),32))|(u_int64)x);
}

void w16a(u_int8 *buf, u_int16 x)
{
    u_int64 orig = r64a(buf);
    w64a(buf, (lsl(lsr(orig,16),16))|(u_int64)x);
}

void w8a(u_int8 *buf, u_int8 x)
{
    u_int64 orig = r64a(buf);
    w64a(buf, (lsl(lsr(orig,8),8))|(u_int64)x);
}


u_int64 lsl(u_int64 x, u_int64 y)
{
    if (y == 64)
    {
        return 0;
    }
    return asm_lsl(x, y);
}

u_int64 lsr(u_int64 x, u_int64 y)
{
    if (y == 64)
    {
        return 0;
    }
    return asm_lsr(x, y);
}
#else
u_int64 r64a(u_int8 *buf)  { return *(u_int64 *)buf; }
u_int32 r32a(u_int8 *buf) { return *(u_int32 *)buf; }
u_int16 r16a(u_int8 *buf) { return *(u_int16 *)buf; }
u_int8 r8a(u_int8 *buf) { return *(u_int8 *)buf; }
void w8a(u_int8 *buf, u_int8 x) { *buf = x; }
void memcpya(void *dst, const void *src, size_t size) { memcpy(dst, src, size); }
#endif