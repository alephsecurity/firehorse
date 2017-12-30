/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#ifndef _GLUEMACROS_H_
#define _GLUEMACROS_H_ 

#include "constants.h"
#include "stdlib.h"


#if ARCH==32
#include "glue32.h"
#elif ARCH==64
#include "glue64.h"
#endif


#define GLUE_FUNC(name, ret, ...) __attribute__((naked)) ret name() { GLUE_BODY(name); }
#define GLUE_PTR(name, ret, defaultval, ...) static ret (*name ## _ptr)(__VA_ARGS__) = (void *)defaultval
#define GLUE(name, defaultval, ret, ...) GLUE_PTR(name, ret, defaultval, __VA_ARGS__); GLUE_FUNC(name, ret, __VA_ARGS__); GLUE_PTR_SETTER(name); GLUE_PTR_GETTER(name)
//#define GLUE_HEADER(name, ret) ret name();


#define GLUE_PTR_SETTER(name)  \
    void set ## _ ## name(void *addr) { \
        name ## _ ## ptr = addr; \
    }
#define GLUE_PTR_GETTER(name)  \
    void * get ## _ ## name() { \
        return name ## _ ## ptr; \
    }

#define GLUE_PTR_GETTER_HEADER(name) void * get ## _ ## name();
#define GLUE_PTR_SETTER_HEADER(name) void set ## _ ## name(void *addr);
#define GLUE_HEADER(name, ret, ...)  ret name(__VA_ARGS__); GLUE_PTR_GETTER_HEADER(name); GLUE_PTR_SETTER_HEADER(name);

#endif
