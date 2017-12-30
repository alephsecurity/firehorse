/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

typedef unsigned long long u_int64;
typedef unsigned int u_int32;
typedef unsigned short u_int16;
typedef unsigned char u_int8;
typedef u_int32 size_t;

void memcpy(void *dst, const void *src, size_t size);
void memcpya(void *dst, const void *src, size_t size);
void memset(void *dst, int c, size_t n);
void writel(u_int32 addr, u_int32 data);

u_int64 r64a(u_int8 *buf);
u_int32 r32a(u_int8 *buf);
u_int16 r16a(u_int8 *buf);
u_int8 r8a(u_int8 *buf);
void w64a(u_int8 *buf, u_int64 x);
void w32a(u_int8 *buf, u_int32 x);
void w16a(u_int8 *buf, u_int16 x);
void w8a(u_int8 *buf, u_int8 x);

#define R0 (0)
#define R1 (1)
#define R2 (2)
#define R3 (3)
#define R4 (4)
#define R5 (5)
#define R6 (6)
#define R7 (7)
#define R8 (8)
#define R9 (9)
#define R10 (10)
#define R11 (11)
#define R12 (12)
#define R13 (13)
#define R14 (14)

#ifdef NEED_ALIGNMENT

#define ra(s) \
(sizeof(s) == 1) ? r8a(&(s)) :\
((sizeof(s) == 2) ? r16a(&(s)) :\
((sizeof(s) == 4) ? r32a(&(s)) :\
(sizeof(s) == 8) ? r64a(&(s)) : -1))



#define wa(d, v) \
    switch (sizeof(d))\
     {\
      case 1:  w8a(&(d), v); break; \
      case 2:  w16a(&(d), v); break; \
      case 4:  w32a(&(d), v); break; \
      case 8:  w64a(&(d), v); break; \
     }

#else 
#define ra(s) s
#define wa(d,v) d = v
#endif