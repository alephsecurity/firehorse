# firehorse 
By Roee Hay ([@roeehay](https://twitter.com/roeehay)) & Noam Hadad, Aleph Reseserch, HCL Technologies 

Research & Exploitation framework for Qualcomm EDL Firehose programmers.

Blog posts:

1. [Exploiting Qualcomm EDL Programmers (1): Gaining Access & PBL Internals](https://alephsecurity.com/2018/01/22/qualcomm-edl-1/)
2. [Exploiting Qualcomm EDL Programmers (2): Storage-based Attacks & Rooting](https://alephsecurity.com/2018/01/22/qualcomm-edl-2/)
3. [Exploiting Qualcomm EDL Programmers (3): Memory-based Attacks & PBL Extraction](https://alephsecurity.com/2018/01/22/qualcomm-edl-3/)
4. [Exploiting Qualcomm EDL Programmers (4): Runtime Debugger](https://alephsecurity.com/2018/01/22/qualcomm-edl-4/)
5. [Exploiting Qualcomm EDL Programmers (5): Breaking Nokia 6's Secure Boot](https://alephsecurity.com/2018/01/22/qualcomm-edl-5/) 


## Usage 

### Prerequisites
To use this tool you'll need:
    1. Qualcomm Product Support Tools (QPST - we used version 2.7.437 running on a windows 10 machine)
    2. A Cross compiler to build the payload for the devices (we used [arm-eabi-4.6](https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/arm/arm-eabi-4.6/) toolchain for aarch32 and [aarch64-linux-android-4.8](https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.8/) toolchain for aarch64, both running on ubuntu 16.04 machine)


### Building the payloads
First, we need to edit the Makefile in the device directory - set the device variable to whatever device we want (nokia6, angler, ugglite, mido and cheeseburger are currently supported).

Next, we set the CROSS_COMPILE_32 and CROSS_COMPILE_64 enviroment vars as follows:
```
export CROSS_COMPILE_32=<path-to-arm-eabi-4.6-toolchain>/bin/arm-eabi-
export CROSS_COMPILE_64=<path-to-aarch64-linux-android-4.8-toolchain>/bin/aarch64-linux-android-
```

Then we can call make and the payload for our specific device will be built :)


### Configure the tool 
Before we start, we need to configure some stuff, edit the constants.py file in the host directory:
    1. set COM to whatever com port the device is connnected to
    2. set FH_LOADER with a path to the fh_loader.exe  in the QPST\bin directory
    3. set SAHARA_SERVER with a path to the QSaharaServer.exe  in the QPST\bin directory
```python
COM = "COM17"
FH_LOADER = r"C:\Program Files (x86)\Qualcomm\QPST437\bin\fh_loader.exe"
SAHARA_SERVER = r"C:\Program Files (x86)\Qualcomm\QPST437\bin\QSaharaServer.exe" 
```

### Using the tool
From command line:
```
python firehorse.py [options] target|fw cmd [cmd_args]
```

options:
    -t TARGET_NAME                  __required__, TARGET_NAME can be one of the following:  nokia6 | angler | ugglite | mido | cheeseburger
    -s, --hello                     send programmer to device - THIS IS __REQUIRED__ ON THE FIRST TIME YOU USE THIS TOOL AFTER THE DEVICE BOOTED INTO EDL 
    -h, --help                      show help message and exit
    -c COM#, --com COM#             specify COM port
    -v, --verbose                   Enable verbose logging
    -vv, --moreverbose              Even more logging

target commands:
    magic                           causes the magic function in the target_TargetName.py file to be called -
                                    on nokia6 this will activate the secure boot exploit and the device will boot with root adb access
    rop                             executes a rop payload (different for every device)
    uart                            dumps uart buffer
    dump_pt                         dumps the programmer page table
    dump_pt32 [skip]                dumps the programmer page table (32 bit table format), if 'skip' is passed,
                                    skipps the first 'skip' entries in fisrt level PT
    dump_pt64                       dumps the programmer page table (64 bit table format)
    extract_pbl                     dumps the device pbl (to a file in the cwd)
    extract_modem_pbl               dumps the device modem_pbl (to a file in the cwd)
    extract_rpm_pbl                 dumps the device rpm_pbl (to a file in the cwd)
    read_partition name             dumps the partition specified by name (to a file in the cwd)
    write_partition name srcpath    overwrites the partition specified by name with the file specified by srcpath


fw commands:
    hello                           send programmer to device
    firehosep xml_path              send the xml specified in xml_path to the programmer
    upload file_path addr           upload the binary file specified by file path to the address addr in 32 bit chunks
    upload64 file_path addr         upload the binary file specified by file path to the address addr in 64 bit chunks
    sendfile file_path addr         upload the binary file specified by file path to the address addr (faster then upload)
    exec addr                       executes the code located at address addr - for 32 bit code
    exec64 addr                     executes the code located at address addr - for 64 bit code
    run file_path addr              uploads the file located at file_path to address addr and executes it - for normal arm code
    runt file_path addr             uploads the file located at file_path to address addr and executes it - for thumb code
    peek addr size [output_file]    reads size bytes from address addr and prints them to screen,if output_file is passed
                                    the output is written to file
    copy dst src size               copies size bytes from address src to address dst
    poke addr val                   writes 4 bytes of data specified by the hex value val at address addr
    


### Examples
```
c:\firehorse\host>python firehorse.py -s -c COM17 -t nokia6 target magic
INFO: sending programmer...
INFO: Overwriting partition logdump with ../tmp\nokia6-ramdisk-modified.cpio.gz...
INFO: applying patches and breakpoints...
INFO: installing bp for 0010527c
INFO: installing bp for 00104130
[...]
INFO: creating pagecopy...
INFO: pages: set([272, 256, 259, 260, 261])
INFO: uploading firehorse data...
INFO: uploading egghunter to 080af000
INFO: 080af000
INFO: i = 0, dst = 080d0000, cksum = d1fe325f
INFO: i = 1, dst = 080d0320, cksum = 3c092224
INFO: got all parts in 1 tries
INFO: uploading firehorse...
INFO: i = 0, dst = 080b0000, cksum = f5234b61
INFO: i = 1, dst = 080b0320, cksum = 641cb436
[...]
INFO: got all parts in 2 tries
INFO: initializing firehorse...
INFO: calling pbl patcher...
```



```
c:\firehorse\host>python firehorse.py -c COM17 -t nokia6 fw hello

c:\firehorse\host>python firehorse.py -c COM17 -t nokia6 fw peek 0x100000 0x10
INFO: 00100000  22 00 00 ea 70 00 00 ea 74 00 00 ea 78 00 00 ea   "...p...t...x...
```
