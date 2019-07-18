from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

from gui import mainwindow
from devices import Devices

import sys

class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.enableItems(False)

        self.__devices = Devices()
        self.__USBDevices = self.__devices.findUSBDevices()

        
    def enableItems(self, enable):
        self.pushButton_sync.setEnabled(enable)
        self.radioButton_deviceLeader.setEnabled(enable)
        self.radioButton_PcLeader.setEnabled(enable)
        self.checkBox_deleteOldFiles.setEnabled(enable)
        self.checkBox_copyNewFiles.setEnabled(enable)
        self.pushButton_selectPcPath.setEnabled(enable)
        self.pushButton_selectDevicePath.setEnabled(enable)
        self.checkBox_rememberDevice.setEnabled(enable)



class FWorker():

    ''' Class is responsible for everything relates to file managment. '''

    def __init__(self):
        # self.__devices = Devices()
        pass

    def copyFiles(self):
        pass

    def deleteFiles(self):
        pass

   
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
    # fworker = FWorker()
