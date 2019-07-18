class Devices(self):
    def __init__(self):
        self.__usbPath = None
        pass


    def findUSBDevices(self): 
        import win32com.client

        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")

        # 1. Win32_DiskDrive
        colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_DiskDrive WHERE InterfaceType = \"USB\"")
        DiskDrive_DeviceID = colItems[0].DeviceID.replace('\\', '').replace('.', '')
        DiskDrive_Caption = colItems[0].Caption
