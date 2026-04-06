# firehorse 
By Roee Hay ([@roeehay](https://twitter.com/roeehay)) & Noam Hadad, Aleph Reseserch, HCL Technologies 

Research & Exploitation framework for Qualcomm EDL Firehose programmers.

Blog posts:

1. [Exploiting Qualcomm EDL Programmers (1): Gaining Access & PBL Internals](https://alephsecurity.com/2018/01/22/qualcomm-edl-1/)
2. [Exploiting Qualcomm EDL Programmers (2): Storage-based Attacks & Rooting](https://alephsecurity.com/2018/01/22/qualcomm-edl-2/)
3. [Exploiting Qualcomm EDL Programmers (3): Memory-based Attacks & PBL Extraction](https://alephsecurity.com/2018/01/22/qualcomm-edl-3/)
4. [Exploiting Qualcomm EDL Programmers (4): Runtime Debugger](https://alephsecurity.com/2018/01/22/qualcomm-edl-4/)
5. [Exploiting Qualcomm EDL Programmers (5): Breaking Nokia 6's Secure Boot](https://alephsecurity.com/2018/01/22/qualcomm-edl-5/) 


## Installation

### Option 1: Install from PyPI (Recommended)
```bash
pip install firehorse
```

### Option 2: Install from Source
```bash
git clone https://github.com/alephsecurity/firehorse.git
cd firehorse
pip install -e .
```

## Usage 

### Prerequisites
To use this tool you'll need:
   1. Qualcomm Product Support Tools (QPST - we used version 2.7.437 running on a windows 10 machine)
   2. A Cross compiler to build the payload for the devices (we used [arm-eabi-4.6](https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/arm/arm-eabi-4.6/) toolchain for aarch32 and [aarch64-linux-android-4.8](https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.8/) toolchain for aarch64, both running on ubuntu 16.04 machine)
   3. Acquire the relevant programmers and copy them to the firehorse/target/device directory


### Building the payloads
First, edit the Makefile in the device directory - set the device variable to whatever device you want (nokia6, angler, ugglite, mido and cheeseburger are currently supported).
<br/>
<br/>
Next, set the CROSS_COMPILE_32 and CROSS_COMPILE_64 enviroment vars as follows:
```
export CROSS_COMPILE_32=<path-to-arm-eabi-4.6-toolchain>/bin/arm-eabi-
export CROSS_COMPILE_64=<path-to-aarch64-linux-android-4.8-toolchain>/bin/aarch64-linux-android-
```
Then call make and the payload for your specific device will be built

### Configure the tool 
Before we start, we need to configure some stuff. The tool now requires command line arguments for configuration:

**Required Arguments:**
  - `-c COM` : COM port where the device is connected
  - `--fh-loader PATH` : Path to fh_loader.exe in QPST\bin directory  
  - `--sahara-server PATH` : Path to QSaharaServer.exe in QPST\bin directory
  - `-t TARGET_NAME` : Target device name

**Example Configuration:**
```bash
firehorse -c COM17 \
  --fh-loader "C:\Program Files (x86)\Qualcomm\QPST437\bin\fh_loader.exe" \
  --sahara-server "C:\Program Files (x86)\Qualcomm\QPST437\bin\QSaharaServer.exe" \
  -t nokia6 target magic
```


### Usage examples
```bash
firehorse -s -c COM17 \
  --fh-loader "C:\Program Files (x86)\Qualcomm\QPST437\bin\fh_loader.exe" \
  --sahara-server "C:\Program Files (x86)\Qualcomm\QPST437\bin\QSaharaServer.exe" \
  -t nokia6 target magic
```

```bash
firehorse -c COM17 \
  --fh-loader "C:\Program Files (x86)\Qualcomm\QPST437\bin\fh_loader.exe" \
  --sahara-server "C:\Program Files (x86)\Qualcomm\QPST437\bin\QSaharaServer.exe" \
  -t nokia6 fw hello
```

```bash
firehorse -c COM17 \
  --fh-loader "C:\Program Files (x86)\Qualcomm\QPST437\bin\fh_loader.exe" \
  --sahara-server "C:\Program Files (x86)\Qualcomm\QPST437\bin\QSaharaServer.exe" \
  -t nokia6 fw peek 0x100000 0x10
```
