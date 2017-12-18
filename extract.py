import os
import struct

FIRMWARE = "TX-6610_V4_150922.bin"
st = os.stat(FIRMWARE)
mem = open(FIRMWARE, "rb")

magic_bytes, header_size, file_size, crc, version, customer_version, kernel_size, rootfs_size, ctrom_size, model = struct.unpack(">4sIII32s32sIII32s", mem.read(124))

print("Magic bytes: {0}".format(magic_bytes))
print("Header size: {0} bytes".format(header_size))
print("File size: {0} bytes".format(file_size))
print("CRC32: {:08X}".format(crc))
print("Version: {0}".format(version))
print("Customer version: {0}".format(customer_version))
print("Kernel size: {0} bytes".format(kernel_size))
print("Rootfs size: {0} bytes".format(rootfs_size))
print("ctrom size: {0} bytes".format(ctrom_size))
print("Model: {0}".format(model))

#dump lzma
mem.seek(0x100)
lzma = mem.read(kernel_size)
f = open("tclinux", "wb")
f.write(lzma)
f.close()

#dump squashfs
mem.seek(0x150000)
squashfs = mem.read(rootfs_size)
f = open("150000.squashfs", "wb")
f.write(squashfs)
f.close()
