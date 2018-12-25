Transfers a file from/to a tftp server

Options:
        -l FILE Local FILE.
        -r FILE Remote FILE.
        -g      Get file.
        -p      Put file.


Send to TFTP server
tftp -l /tmp/dump -r dump -p 192.168.1.100

Receive from TFTF server
tftp -g -r dump 192.168.1.100

Attach gdbserver to a PID
gdbserver localhost:23947 --attach <PID>
