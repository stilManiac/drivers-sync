from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *

from gui import mainwindow

import sys
import time
import usb.core
import usb.util

import tools

settings = QtCore.QSettings('Devyncer', 'Devyncer')

class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        
        self.devices = []
        self.vendorList = []
        self.productList = []
        self.pathList = []
        
        self.find_storage_devices()

        # Attach action to syncButton
        self.syncButton.clicked.connect(self.syncButtonAction)

    def syncButtonAction(self):
        if self.syncButton.text() == 'Delete':
            self.pathList.remove(self.vendorList.index(self.devices[self.comboBox.currentIndex()].idVendor))
            self.vendorList.remove(self.devices[self.comboBox.currentIndex()].idVendor)
            self.productList.remove(self.devices[self.comboBox.currentIndex()].idProduct)

            settings.setValue('idVendor', self.vendorList)
            settings.setValue('idProduct', self.productList)
        else:
            # Open file dialog to choose directory to sync
            fpath = QFileDialog.getExistingDirectory(self, 'Choose FLASH DRIVE directory')

            self.vendorList.append(self.devices[self.comboBox.currentIndex()].idVendor)
            self.productList.append(self.devices[self.comboBox.currentIndex()].idProduct)
            self.pathList.append(fpath)

            settings.setValue('idVendor', self.vendorList)
            settings.setValue('idProduct', self.productList)
            settings.setValue('pathList', self.pathList)

            print(self.vendorList)
            print(self.productList)
            print(self.pathList)

        self.find_storage_devices()

    def find_storage_devices(self):
        devs = usb.core.find(find_all=True)

        self.comboBox.clear()
        self.devices.clear()

        # Find out devices
        for dev in devs:
            for cfg in dev:
                for intf in cfg:

                    # If finded device has Mass Storage Type
                    if intf.bInterfaceClass == 8:
                        self.devices.append(dev)
                        self.comboBox.addItem(usb.util.get_string(dev, 1) + ' '+ usb.util.get_string(dev, 2))
                        
                        # Load idVendor and idProduct from settings
                        self.vendorList = settings.value('idVendor', [], int)
                        self.productList = settings.value('idProduct', [], int)

                        # Change syncButton text
                        if dev.idVendor in self.vendorList and dev.idProduct in self.productList:
                            self.status_label.setText('Status: Tracked')
                            self.syncButton.setText('Delete')
                        else:
                            self.status_label.setText('Status: Not tracked')
                            self.syncButton.setText('Sync')
                        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
