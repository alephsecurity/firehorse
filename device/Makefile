#
# firehorse
# by Roee Hay & Noam Hadad, Aleph Research
#

.DEFAULT_GOAL := all

DEVICE = nokia6
BUILD_DIR = ./build
LD_SCRIPT := ./fh.ld

TARGET := fh
TARGETBIN = $(BUILD_DIR)/$(TARGET)
TARGETPAYLOAD := $(TARGETBIN).payload

TARGET64 := fh64
TARGETBIN64 = $(BUILD_DIR)/$(TARGET64)
TARGETPAYLOAD64 := $(TARGETBIN64).payload

DBGENTRY64 := dbgentry64
DBGENTRYBIN64 = $(BUILD_DIR)/$(DBGENTRY64)
DBGENTRYPAYLOAD64 := $(DBGENTRYBIN64).payload

DLOAD := dload
DLOADBIN := $(BUILD_DIR)/$(DLOAD)
DLOADPAYLOAD := $(DLOADBIN).payload

DLOAD64 := dload64
DLOADBIN64 := $(BUILD_DIR)/$(DLOAD64)
DLOADPAYLOAD64 := $(DLOADBIN64).payload


XMLHUNT := xmlhunt
XMLHUNTBIN := $(BUILD_DIR)/$(XMLHUNT)
XMLHUNTPAYLOAD := $(XMLHUNTBIN).payload

INIT64 := init64
INITBIN64 := $(BUILD_DIR)/$(INIT64)
INITPAYLOAD64 := $(INITBIN64).payload



HAS_UART := 1
ARCH := 32

ifeq ($(DEVICE), nokia6)
	COMPILE_DLOAD := 1
	HAS_UART := 1
endif 
ifeq ($(DEVICE), ugglite)
	COMPILE_XMLHUNTER := 1
	XMLHUNTER_DACR := 1
	HAS_UART := 1
endif
ifeq ($(DEVICE), mido)
	COMPILE_XMLHUNTER := 1
	XMLHUNTER_DACR := 1
	HAS_UART := 1
endif
ifeq ($(DEVICE), cheeseburger)
	COMPILE_XMLHUNTER := 1
	XMLHUNTER_DACR := 0
	HAS_UART := 1
	ARCH := 64
endif
ifeq ($(DEVICE), angler)
	COMPILE_XMLHUNTER := 0
	XMLHUNTER_DACR :=1
	HAS_UART := 1
	ARCH := 64
endif


GCC_FLAGS_32 :=  -Os -march=armv7-a -fpic -fno-builtin  -I"./target/$(DEVICE)" -D XMLHUNTER_DACR=$(XMLHUNTER_DACR) -D ARCH=$(ARCH) -D TARGET="\"$(DEVICE)\"" #-DVALIDATE_PAGES 
GCC_FLAGS_64 := -Os -I"./target/$(DEVICE)"  -D TARGET="\"$(DEVICE)\"" -fpic -fno-builtin -D XMLHUNTER_DACR=$(XMLHUNTER_DACR) -D ARCH=$(ARCH) -DNEED_ALIGNMENT -mstrict-align -Wno-int-to-pointer-cast -Wno-pointer-to-int-cast -Wno-attributes


ifeq ($(HAS_UART),1)
	GCC_FLAGS_32 += -DUART_ON
	GCC_FLAGS_64 += -DUART_ON
endif


CROSS_COMPILE := $(CROSS_COMPILE_32)
GCC_FLAGS := $(GCC_FLAGS_32)
ASM := asm
ifeq ($(ARCH), 64)
	CROSS_COMPILE := $(CROSS_COMPILE_64)
	GCC_FLAGS := $(GCC_FLAGS_64)
	ASM := asm64
endif

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)/obj

fh.o: fh.c	
	$(CROSS_COMPILE)gcc $(GCC_FLAGS) -c $?

stdlib.o: stdlib.c	
	$(CROSS_COMPILE)gcc $(GCC_FLAGS) -c $?

stdlib32.o: stdlib32.c	
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

flushtlb.o: flushtlb.c
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

dacr.o: dacr.c
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

null.o: null.c
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?


dbg.o: dbg.c	
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

dbg64.o: dbg64.c	
	$(CROSS_COMPILE_64)gcc $(GCC_FLAGS_64) -c $?


init.o: init.c	
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

mini_printf.o: mini_printf.c	
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

aeabi_uidiv.o: aeabi_uidiv.S	
	$(CROSS_COMPILE_32)gcc  $(GCC_FLAGS_32) -c $?


constants.o: constants.c	
	$(CROSS_COMPILE)gcc $(GCC_FLAGS) -c $?

dbgasm.o: dbg.S	
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $? -o dbgasm.o

dbgentry64.o: dbg64.S	
	$(CROSS_COMPILE_64)gcc $(GCC_FLAGS_64) -c $? -o dbgentry64.o

pagecopy.o: pagecopy.c
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

entry.o: entry.S
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

$(ASM).o: $(ASM).S
	$(CROSS_COMPILE)gcc $(GCC_FLAGS) -c $?

glue.o: glue.c
	$(CROSS_COMPILE)gcc $(GCC_FLAGS) -c $?

pt.o: pt.c
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

patcher.o: target/$(DEVICE)/patcher.c
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

pageremap.o: pageremap.c
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

dloadentry.o: dload.S
	$(CROSS_COMPILE)gcc $(GCC_FLAGS) -c $? -o dloadentry.o

dload.o: dload.c
	$(CROSS_COMPILE_32)gcc $(GCC_FLAGS_32) -c $?

xmlhunt.o: xmlhunt.c
	$(CROSS_COMPILE)gcc $(GCC_FLAGS) -c $?

pt64.o: pt64.c
	$(CROSS_COMPILE_64)gcc $(GCC_FLAGS_64) -c $?

entry64.o: entry64.S
	$(CROSS_COMPILE_64)gcc $(GCC_FLAGS_64) -c $?

init64.o: init64.c
	$(CROSS_COMPILE_64)gcc $(GCC_FLAGS_64) -c $?

init64entry.o: init64.S
	$(CROSS_COMPILE_64)gcc $(GCC_FLAGS_64) -c $? -o init64entry.o


clean: 
	rm -fr build
	rm -fr *.o

ifeq ($(COMPILE_XMLHUNTER),1)
$(XMLHUNTPAYLOAD): $(XMLHUNT)
	$(CROSS_COMPILE)objcopy -O binary $(XMLHUNTBIN) $(XMLHUNTPAYLOAD)

$(XMLHUNT): $(BUILD_DIR) $(XMLHUNT).o dloadentry.o stdlib.o fh.o glue.o constants.o $(ASM).o  #constants.o
	$(CROSS_COMPILE)ld -T $(LD_SCRIPT) -o $(XMLHUNTBIN) dloadentry.o $(XMLHUNT).o stdlib.o $(ASM).o #glue.o constants.o

objdump-xmlhunt: $(XMLHUNTBIN)
	$(CROSS_COMPILE)objdump $(XMLHUNTBIN) -d

else
$(XMLHUNTPAYLOAD):
endif

ifeq ($(ARCH),32)

all: $(TARGETPAYLOAD) $(DLOADPAYLOAD) $(XMLHUNTPAYLOAD)
	mv *.o ./build/obj
		
$(TARGET): $(BUILD_DIR) entry.o glue.o dbg.o fh.o pagecopy.o $(ASM).o stdlib.o dbgasm.o constants.o init.o pt.o patcher.o pageremap.o 
	$(CROSS_COMPILE_32)ld -T $(LD_SCRIPT) -o $(TARGETBIN) ./entry.o glue.o fh.o dbg.o pagecopy.o $(ASM).o stdlib.o constants.o dbgasm.o init.o pt.o patcher.o pageremap.o 

$(TARGETPAYLOAD): $(TARGET)
	$(CROSS_COMPILE_32)objcopy -O binary $(TARGETBIN) $(TARGETPAYLOAD)

ifeq ($(COMPILE_DLOAD),1)
$(DLOADPAYLOAD): $(DLOAD)
	$(CROSS_COMPILE_32)objcopy -O binary $(DLOADBIN) $(DLOADPAYLOAD)

$(DLOAD): $(BUILD_DIR) $(DLOAD).o dloadentry.o stdlib.o $(ASM).o fh.o glue.o constants.o
	$(CROSS_COMPILE_32)ld -T $(LD_SCRIPT) -o $(DLOADBIN) dloadentry.o $(DLOAD).o stdlib.o $(ASM).o 
objdump-dload: dload
	$(CROSS_COMPILE_32)objdump $(DLOADBIN) -d
else
$(DLOADPAYLOAD):
endif
objdump: all 
	$(CROSS_COMPILE_32)objdump $(TARGETBIN) -d

endif


ifeq ($(ARCH),64)

all: $(TARGETPAYLOAD64) $(DBGENTRYPAYLOAD64) $(DLOADPAYLOAD64) $(XMLHUNTPAYLOAD) 
	mv *.o ./build/obj

$(TARGETPAYLOAD64): $(TARGET64)
	$(CROSS_COMPILE_64)objcopy -O binary $(TARGETBIN64) $(TARGETPAYLOAD64)

$(DBGENTRYPAYLOAD64): $(DBGENTRYBIN64)
	$(CROSS_COMPILE_64)objcopy -O binary $(DBGENTRYBIN64) $(DBGENTRYPAYLOAD64)

$(DBGENTRYBIN64): dbgentry64.o
	$(CROSS_COMPILE_64)ld -T $(LD_SCRIPT) -o $(DBGENTRYBIN64) dbgentry64.o

$(DBGENTRY64)-objdump: $(DBGENTRYBIN64) 
	$(CROSS_COMPILE_64)objdump $(DBGENTRYBIN64) -d


$(TARGET64): $(BUILD_DIR) $(DBGENTRYBIN64) entry64.o fh.o dbg64.o $(ASM).o constants.o glue.o init64.o stdlib.o
	$(CROSS_COMPILE_64)ld -T $(LD_SCRIPT) -o $(TARGETBIN64) ./entry64.o ./init64.o ./fh.o ./dbg64.o $(ASM).o ./constants.o  ./glue.o ./stdlib.o


$(INITPAYLOAD64): $(INITBIN64)
	$(CROSS_COMPILE_64)objcopy -O binary $(INITBIN64) $(INITPAYLOAD64)

$(INITBIN64): init64entry.o init64.o $(ASM).o constants.o glue.o pt64.o stdlib.o
	$(CROSS_COMPILE_64)ld -T $(LD_SCRIPT) -o $(INITBIN64) init64entry.o init64.o $(ASM).o constants.o glue.o pt64.o stdlib.o

$(INIT64)-objdump: $(INITBIN64) 
	$(CROSS_COMPILE_64)objdump $(INITBIN64) -d



ifeq ($(COMPILE_DLOAD64),1)
$(DLOADPAYLOAD64): $(DLOAD64)
	$(CROSS_COMPILE_64)objcopy -O binary $(DLOADBIN64) $(DLOADPAYLOAD64)

$(DLOAD64): $(BUILD_DIR) $(DLOAD64).o dloadentry.o stdlib.o $(ASM).o fh.o glue.o constants.o
	$(CROSS_COMPILE_64)ld -T $(LD_SCRIPT) -o $(DLOADBIN64) dloadentry.o $(DLOAD64).o stdlib.o $(ASM).o
objdump-dload64: dload64
	$(CROSS_COMPILE_64)objdump $(DLOADBIN64) -d
else
$(DLOADPAYLOAD64):
endif

objdump64: all 
	$(CROSS_COMPILE_64)objdump $(TARGETBIN64) -d

endif

