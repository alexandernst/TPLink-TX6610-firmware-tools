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
* Header size (uint32_t)
* File size (uint32_t) Keep in mind this size doesn't include the "unknown ending data". Keep reading.
* CRC? (4 bytes) This is probably a CRC32, but I haven't successfully proven that.
* Fw version (64 bytes)
* LZMA size (uint32_t) The size that the LZMA blob takes (starting from `0x100`)
* SquashFS size (uint32_t) The size that the SquashFS blob takes (starting from `0x150000`)
* Fw build (16 bytes)
* 152 bytes of unknown data (`0x7C` and `0x7E` look interesting, but I haven't found what they are for)

## LZMA blob

Starts at `0x100`. It contains the kernel.

## SquashFS blob

Starts at `0x150000`. It contains the FS and configuration data. It also contains the web-admin, users/passwords, etc...

## Padding and ending data.

After the end of the SquashFS blob (remember, `0x150000` + the SquashFS blob size from the header) there are `55640` nulled bytes. I don't know if that is some sort of padding, some sort of required empty space, or ...

... And after those `55640` bytes, there are another `232` bytes. That last section actually holds data, but I haven't found what is it's purpose, how it's generated or what it is used for.

## Python dumping tool

I'm adding a simple python piece of code that extracts the different parts of the firmware.
