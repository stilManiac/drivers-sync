from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

from gui import mainwindow

import os
from os import listdir
from os.path import isfile, join

import sys
import time
import usb.core
import usb.util
import shutil

import tools

settings = QtCore.QSettings('Devyncer', 'Devyncer')

class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        
        self.devices = []
        self.vendorList = []
        self.productList = []
        self.FlashPathList = []
        self.PCPathList = []
        
        self.find_storage_devices()

        # Attach action to syncButton
        self.syncButton.clicked.connect(self.syncButtonAction)

        # Timer
        timer = QTimer()
        timer.timeout.connect(self.syncFiles)
        timer.start(1000)


    def syncButtonAction(self):
        if self.syncButton.text() == 'Delete':
            # Clear lists
            self.FlashPathList.remove(self.vendorList.index(self.devices[self.comboBox.currentIndex()].idVendor))
            self.PCPathList.remove(self.vendorList.index(self.devices[self.comboBox.currentIndex()].idVendor))
            self.vendorList.remove(self.devices[self.comboBox.currentIndex()].idVendor)
            self.productList.remove(self.devices[self.comboBox.currentIndex()].idProduct)

            # Save lists
            settings.setValue('idVendor', self.vendorList)
            settings.setValue('idProduct', self.productList)
            settings.setValue('flashPathList', self.FlashPathList)
            settings.setValue('PCPathList', self.PCPathList)
        else:
            # Open file dialog to choose directory to sync
            fpath = QFileDialog.getExistingDirectory(self, 'Choose FLASH DRIVE directory')

            pcpath = QFileDialog.getExistingDirectory(self, 'Choose PC directory')

            self.vendorList.append(self.devices[self.comboBox.currentIndex()].idVendor)
            self.productList.append(self.devices[self.comboBox.currentIndex()].idProduct)
            self.FlashPathList.append(fpath)
            self.PCPathList.append(pcpath)

            settings.setValue('idVendor', self.vendorList)
            settings.setValue('idProduct', self.productList)
            settings.setValue('flashPathList', self.FlashPathList)
            settings.setValue('PCPathList', self.PCPathList)

        # Update GUI
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
                        self.FlashPathList = settings.value('flashPathList', [], str)
                        self.PCPathList = settings.value('PCPathList', [], str)

                        # Change syncButton text
                        if dev.idVendor in self.vendorList and dev.idProduct in self.productList:
                            self.status_label.setText('Status: Tracked')
                            self.syncButton.setText('Delete')

                            # If app founded saved drivers - sync it!
                            self.syncFiles(self.vendorList.index(dev.idVendor))
                        else:
                            self.status_label.setText('Status: Not tracked')
                            self.syncButton.setText('Sync')


    def syncFiles(self, idx):
        flashpath = self.FlashPathList[idx] 
        pcpath = self.PCPathList[idx] 

        flashfiles = [f for f in listdir(flashpath) if isfile(join(flashpath, f))] 
        pcfiles = [f for f in listdir(pcpath) if isfile(join(pcpath, f))] 
        # print(flashfiles)
        # print(pcfiles)

        # PC is leader
        for pcfile in pcfiles: 
            synced = False

            for ffile in flashfiles: 
                if tools.get_hash(os.path.join(pcpath, pcfile)) == tools.get_hash(os.path.join(flashpath, ffile)):
                    # If even 1 file is matched, OK
                    synced = True
            
            # If noone file is matched, copying..
            if synced == False:
                shutil.copy2(os.path.join(pcpath, pcfile), flashpath)
                print('FILE %s WAS COPIED' % os.path.join(pcpath, pcfile))


        time.sleep(60)
        self.find_storage_devices()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()

    
