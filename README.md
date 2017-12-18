# TPLink-TX6610-V4-firmware-RE
Information about the binary structure of [TP Link's TX6610 V4 firmware](http://static.tp-link.com/res/down/soft/TX-6610_V4_150922.zip)

I'm working on REing TP Link's TX6610 firmware. I have been able to successfully unpack the files from the firmware.
I also have been working on actually parsing the header of the firmware's blob and getting information from it.

The firmware consists of several parts:

* 256 bytes header
* LZMA blob (starting at `0x100`)
* SquashFS blob (starting at `0x150000`)
* Some sort of data appended to the end

## Header

![Header](https://github.com/alexandernst/TPLink-TX6610-V4-firmware-RE/blob/master/TX-6610_V4_150922_bin.png)

* Magic bytes (4 bytes): `HDR2`
* Header size (`uint32_t`)
* File size (`uint32_t`) Keep in mind this size doesn't include the "unknown ending data". Keep reading.
* CRC32 (4 bytes) with a custom table (check `compress.py`).
* Version (32 bytes)
* Customer version (32 bytes)
* Kernel size (`uint32_t`) The size that the LZMA blob takes (starting from `0x100`)
* RootFS size (`uint32_t`) The size that the SquashFS blob takes (starting from `0x150000`)
* ctrom size (`uint32_t`)
* Model (32 bytes)
* Unknown 4 bytes
* 128 empty bytes

## LZMA blob

Starts at `0x100`. It contains the kernel.

## SquashFS blob

Starts at `0x150000`. It contains the FS and configuration data. It also contains the web-admin, users/passwords, etc...

## Unknown data

At `0x350000` there are 232 bytes of unknown data. After some more debugging of the firmware, I'm quite sure that `0x350000` to `0x35000F` and `0x3500D4` to `0x3500E3` contain MD5 checksums, but I still don't know the data that is being checked against. The rest is unknown. 

## Python dumping and compressing tools

I'm adding a simple python piece of code that extracts the different parts of the firmware and another one that joins them back together.
Note that the output of the second piece of code still doesn't produce an usable firmware blob as I still don't know how to generate the last 232 bytes.
