# TPLink-TX6610-V4-firmware-RE
Information about the binary structure of [TPLink's TX6610 V4 firmware](http://static.tp-link.com/res/down/soft/TX-6610_V4_150922.zip)

I'm working on reverse engineering TPLink's TX6610 firmware. I have been able to successfully unpack the files from the firmware.
I also have been working on actually parsing the header of the firmware's blob and getting information from it.

The firmware consists of several parts:

* 256 bytes header
* Kernel blob (starting at `0x100`)
* RootFS blob (starting at `0x150000`)
* Some sort of data appended to the end (starting at `0x350000`)

## Header

![Header](https://github.com/alexandernst/TPLink-TX6610-V4-firmware-RE/blob/master/TX-6610_V4_150922_bin.png)

* Magic bytes (4 bytes): `HDR2`
* Header size (`uint32_t`)
* File size (`uint32_t`) Keep in mind this size doesn't include the "checksum ending data". Keep reading.
* CRC32 (4 bytes) with a custom table (check `compress.py`).
* Version (32 bytes)
* Customer version (32 bytes)
* Kernel size (`uint32_t`) The size that the LZMA blob takes (starting from `0x100`)
* RootFS size (`uint32_t`) The size that the SquashFS blob takes (starting from `0x150000`)
* ctrom size (`uint32_t`)
* Model (32 bytes)
* Unknown 4 bytes
* 128 empty bytes

## CRC32
A CRC32 is performed on the the data starting at `0x100` and ending at `0x350000`. The CRC32 uses a custom table (check `compress.py`)

## Kernel blob

Starts at `0x100`. It contains the kernel and it's compressed with LZMA.

## RootFS blob

Starts at `0x150000`. It contains the FS and configuration data. It also contains the web-admin, users/passwords, etc... You can mount it like any other squashFS file.

## Checksum data

At `0x350000` there are 232 bytes of checksum data. After some more debugging of the firmware, I found how the firmware is validated.

![MD5 validation](https://github.com/alexandernst/TPLink-TX6610-V4-firmware-RE/blob/master/MD5_checksum_-_libcmm.so.png)

Basically, the firmware blob is constructed the following way:

* write the header data
* write the kernel blob
* write `0x00` up to `0x150000`
* write rootfs blob
* write `0x00` up to `0x350000`
* write the first 212 bytes (starting from `0x350000`) of the original firmware
* write the magic bytes (check `md5_magic` in `compress.py`)
* write 4 `0x00`

Now run an MD5 against that entire blob and then use the result to replace the magic md5 bytes.

## Python dumping and compressing tools

I'm adding a simple python piece of code that extracts the different parts of the firmware and another one that joins them back together in a perfectly valid and working firmware.

## SynalyzeIt Pro grammar

I'm also adding a grammar file so you can easily analyze the firmware yourself.
