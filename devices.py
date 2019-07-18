import ctypes
import os
import win32file

DRIVE_REMOVABLE   = 2  # The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.

class Devices():
    def __init__(self):
        self.__usbPath = None
        pass


    def findUSBDevices(self): 
        result = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for i in range(26):
            bit = 2 ** i
            if bit & bitmask:
                drive_letter = '%s' % chr(65 + i)
                drive_type = win32file.GetDriveType(drive_letter + ':\\') 

                if drive_type == DRIVE_REMOVABLE:

                    # Format serial number as cool XXXX-XXXX number
                    vsn = os.stat(drive_letter + ':').st_dev
                    SN = '{:04X}-{:04X}'.format(vsn >> 16, vsn & 0xffff)

                    result.append({'Path': drive_letter, 'Type': drive_type, 'SN': SN})

        return result
