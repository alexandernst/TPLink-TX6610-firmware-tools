import os
import struct

IMAGE = "TX-6610_V4_150922.bin"
st = os.stat(IMAGE)
mem = open(IMAGE, "rb")

magic_bytes, header_size, file_size, crc, fw_version, lzma_size, squashfs_size = struct.unpack(">4sII4s64sII", mem.read(88))

print("Magic bytes: {0}".format(magic_bytes))
print("Header size: {0} bytes".format(header_size))
print("File size (without data added at the end): {0} bytes".format(file_size))
print("CRC (?): {}".format(crc))
print("Fw version: {0}".format(fw_version))
print("LZMA size: {0} bytes".format(lzma_size))
print("SquashFS size: {0} bytes".format(squashfs_size))

#dump lzma
mem.seek(0x100)
lzma = mem.read(lzma_size)
f = open("100.lzma", "wb")
f.write(lzma)
f.close()

#dump squashfs
mem.seek(0x150000)
squashfs = mem.read(squashfs_size)
f = open("150000.squashfs", "wb")
f.write(squashfs)
f.close()

#dump data at the end
end_data_size = st.st_size - file_size
end_data = mem.read(end_data_size)
f = open("end.bin", "wb")
f.write(end_data)
f.close()
