from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

from gui import mainwindow
from devices import Devices

import sys

settings = QtCore.QSettings('Devyncer', 'Devyncer')

class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.enableItems(False)

        self.data = settings.value('data')
        # print(self.data)

        self.__fworker = FWorker()

        self.__devices = Devices()
        self.__USBDevices = self.__devices.findUSBDevices()

        if len(self.__USBDevices) != 0:
            self.enableItems(True)
            for item in self.__USBDevices:
                self.comboBox.addItems([item['Path'] + ':/'])

        # Load settings
        self.loadSettings()

        self.pushButton_saveSettings.clicked.connect(self.saveSettings)

        self.pushButton_sync.clicked.connect(lambda: self.__fworker.syncDevices(self.__USBDevices[self.comboBox.currentIndex()]))

        # 1 - PC, 2 - Device
        self.pushButton_selectPcPath.clicked.connect(lambda: self.selectPath(1))
        self.pushButton_selectDevicePath.clicked.connect(lambda: self.selectPath(2))

        self.pushButton_clearPcFolder.clicked.connect(lambda: self.clearPath(1))
        self.pushButton_clearDeviceFolder.clicked.connect(lambda: self.clearPath(2))

        # When user changes disk
        self.comboBox.currentIndexChanged.connect(self.loadSettings)


    def clearPath(self, dev):
        if dev == 1:
            self.__USBDevices[self.comboBox.currentIndex()]['PcFolder'] = None
            self.label_isComputerFolderSelected.setText('''<span style=" color:#aa0000;">Not selected!</span>''')
        elif dev == 2:
            self.__USBDevices[self.comboBox.currentIndex()]['DevFolder'] = None
            self.label_isDeviceFolderSelected.setText('''<span style=" color:#aa0000;">Not selected!</span>''')

        self.saveSettings()



    def selectPath(self, dev):

        # PC 
        if dev == 1: 
            path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if len(path) != 0: 
                if path[0] == self.__USBDevices[self.comboBox.currentIndex()]['Path']:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("You tried to select external device's directory. Please, select computer's one.")
                    msg.setWindowTitle("Failed!")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()

                else:
                    self.__USBDevices[self.comboBox.currentIndex()]['PcFolder'] = path
                    self.saveSettings()

                    self.label_isComputerFolderSelected.setText('''<span style=" color:#00aa00;">Selected!</span>''')
        # Extern. device
        elif dev == 2:
            devPath = self.__USBDevices[self.comboBox.currentIndex()]['Path'] + ':\\'
            path = str(QFileDialog.getExistingDirectory(self, "Select Directory", devPath))

            if len(path) != 0: 
                if path[0] != self.__USBDevices[self.comboBox.currentIndex()]['Path']:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("You didn't select your external device's directory (must be a same disk letter)")
                    msg.setWindowTitle("Failed!")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                else:
                    self.__USBDevices[self.comboBox.currentIndex()]['DevFolder'] = path
                    self.saveSettings()

                    self.label_isDeviceFolderSelected.setText('''<span style=" color:#00aa00;">Selected!</span>''')

        if self.__USBDevices[self.comboBox.currentIndex()]['DevFolder'] is not None and self.__USBDevices[self.comboBox.currentIndex()]['PcFolder'] is not None:
            self.allowSync(True)


    def closeEvent(self, event):
        self.saveSettings()
        print(self.data[0])
        print(self.data[1])

        # settings.setValue('data', None)

    def loadSettings(self):
        if self.data is not None and len(self.__USBDevices) != 0:
            for item in self.data:
                if item['SN'] == self.__USBDevices[self.comboBox.currentIndex()]['SN']:
                    self.checkBox_deleteOldFiles.setChecked(item['AllowDelete'])
                    self.checkBox_copyNewFiles.setChecked(item['AllowCopy'])

                    self.__USBDevices[self.comboBox.currentIndex()]['AllowDelete'] = item['AllowDelete'] 
                    self.__USBDevices[self.comboBox.currentIndex()]['AllowCopy'] = item['AllowCopy'] 
                    self.__USBDevices[self.comboBox.currentIndex()]['PcFolder'] = item['PcFolder'] 
                    self.__USBDevices[self.comboBox.currentIndex()]['DevFolder'] = item['DevFolder'] 

                    if item['PcFolder'] is None or item['DevFolder'] is None:
                        self.allowSync(False)

                    elif item['PcFolder'] is not None and item['DevFolder'] is not None:
                        self.allowSync(True)


                    if item['Leader'] == 'Computer':
                        self.radioButton_deviceLeader.setChecked(False)
                        self.radioButton_PcLeader.setChecked(True)
                        self.__USBDevices[self.comboBox.currentIndex()]['Leader'] = 'Computer'
                    else:
                        self.radioButton_PcLeader.setChecked(False)
                        self.radioButton_deviceLeader.setChecked(True)
                        self.__USBDevices[self.comboBox.currentIndex()]['Leader'] = 'Device'

                    if item['PcFolder'] == None:
                        self.label_isComputerFolderSelected.setText('''<span style=" color:#aa0000;">Not selected!</span>''')
                    else:
                        self.label_isComputerFolderSelected.setText('''<span style=" color:#00aa00;">Selected!</span>''')

                    if item['DevFolder'] == None:
                        self.label_isDeviceFolderSelected.setText('''<span style=" color:#aa0000;">Not selected!</span>''')
                    else:
                        self.label_isDeviceFolderSelected.setText('''<span style=" color:#00aa00;">Selected!</span>''')

                    break

    def saveSettings(self):
        if len(self.__USBDevices) != 0:
            if self.data is None:
                self.data = []

            # If driver is already stored in data
            for item in self.data:
                if item['SN'] == self.__USBDevices[self.comboBox.currentIndex()]['SN']:
                    if self.radioButton_PcLeader.isChecked():
                        item['Leader'] = 'Computer'
                    else:
                        item['Leader'] = 'Device'

                    if self.checkBox_deleteOldFiles.isChecked():
                        item['AllowDelete'] = True
                    else:
                        item['AllowDelete'] = False

                    if self.checkBox_copyNewFiles.isChecked():
                        item['AllowCopy'] = True
                    else:
                        item['AllowCopy'] = False

                    item['PcFolder'] = self.__USBDevices[self.comboBox.currentIndex()]['PcFolder']
                    item['DevFolder'] = self.__USBDevices[self.comboBox.currentIndex()]['DevFolder']

                    settings.setValue('data', None)
                    settings.setValue('data', self.data) 

                    if item['PcFolder'] is not None and item['DevFolder'] is not None:
                        self.allowSync(True)
                    else:
                        self.allowSync(False)


                    break

            # if device is not in saved data
            else:
                # Saving
                item = self.__USBDevices[self.comboBox.currentIndex()]
                
                if self.radioButton_PcLeader.isChecked():
                    item['Leader'] = 'Computer'
                else:
                    item['Leader'] = 'Device'

                if self.checkBox_deleteOldFiles.isChecked():
                    item['AllowDelete'] = True
                else:
                    item['AllowDelete'] = False

                if self.checkBox_copyNewFiles.isChecked():
                    item['AllowCopy'] = True
                else:
                    item['AllowCopy'] = False

                self.data.append(item)
                settings.setValue('data', None)
                settings.setValue('data', self.data) 


    def allowSync(self, enable):
        self.pushButton_sync.setEnabled(enable) 

    def enableItems(self, enable):
        self.pushButton_saveSettings.setEnabled(enable)
        self.pushButton_sync.setEnabled(enable)
        self.radioButton_deviceLeader.setEnabled(enable)
        self.radioButton_PcLeader.setEnabled(enable)
        self.checkBox_deleteOldFiles.setEnabled(enable)
        self.checkBox_copyNewFiles.setEnabled(enable)
        self.pushButton_selectPcPath.setEnabled(enable)
        self.pushButton_selectDevicePath.setEnabled(enable)
        self.pushButton_clearPcFolder.setEnabled(enable)
        self.pushButton_clearDeviceFolder.setEnabled(enable)


import os
from os import listdir
from os.path import isfile, join
import shutil

class FWorker():
    ''' Class is responsible for everything relates to file managment. '''

    def __init__(self):
        # self.__devices = Devices()
        pass

    def syncDevices(self, devInfo):
        flashpath = devInfo['DevFolder']
        pcpath = devInfo['PcFolder']
        leader = devInfo['Leader']
        allowCopy = devInfo['AllowCopy']
        allowDelete = devInfo['AllowDelete']

        pcfiles = list()
        for (dirpath, dirnames, filenames) in os.walk(pcpath):
            pcfiles += [os.path.join(dirpath, file) for file in filenames]

        flashfiles = list()
        for (dirpath, dirnames, filenames) in os.walk(flashpath):
            flashfiles += [os.path.join(dirpath, file) for file in filenames]

        if leader == 'Computer':
            self.copyFiles(pcfiles, flashfiles, pcpath, flashpath)

            # Delete files
            if allowDelete is True:
                self.deleteFiles(pcfiles, flashfiles)


        else:
            self.copyFiles(flashfiles, pcfiles, flashpath, pcpath)
            
            # Delete files
            if allowDelete is True:
                self.deleteFiles(flashfiles, pcfiles)


    def copyFiles(self, leaderFiles, submissionFiles, leaderPath, submissionPath):
        for leaderFile in leaderFiles: 
            synced = False

            # TODO: FIX HASH OF zero-length files!!!!!!!!
            for submissionFile in submissionFiles: 
                if self.get_hash(leaderFile) == self.get_hash(submissionFile):
                    # If even 1 file is matched, delete this element from list to avoid duplicates 
                    submissionFiles.remove(submissionFile)
                    synced = True
            
            # If noone file is matched, copying..
            if synced == False:
                fullfp = submissionPath + leaderFile.replace(leaderPath, '')
                fullfpnoname = '\\'.join(fullfp.split('\\')[0:-1])

                if not os.path.isdir(fullfpnoname):
                    os.mkdir(fullfpnoname)

                shutil.copy2(leaderFile, submissionPath + leaderFile.replace(leaderPath, ''))
                # print('FILE %s WAS COPIED' % os.path.join(pcpath, pcfile))


    def deleteFiles(self, leaderFiles, submissionFiles):
        todelete = (list(set(submissionFiles) - set(leaderFiles)))
        for submissionFile in todelete:
            os.remove(submissionFile)
            # print('FILE %s WAS DELETED' % submissionFile)


     # Get hash of file
    def get_hash(self, filepath):
        import hashlib

        buf_size = 65536
        # sha1 = hashlib.sha1()
        md5 = hashlib.md5()

        with open(filepath, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break

                md5.update(data)

        return md5.hexdigest().upper()

  
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
    # fworker = FWorker()
