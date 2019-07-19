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


        self.__devices = Devices()
        self.__USBDevices = self.__devices.findUSBDevices()

        if len(self.__USBDevices) != 0:
            self.enableItems(True)
            for item in self.__USBDevices:
                self.comboBox.addItems([item['Path'] + ':/'])



        # Load settings
        self.loadSettings()

        self.pushButton_saveSettings.clicked.connect(self.saveSettings)

        # When user changes disk
        self.comboBox.currentIndexChanged.connect(self.loadSettings)


    def closeEvent(self, event):
        self.saveSettings()
        print(self.data[0])
        print(self.data[1])

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


    def enableItems(self, enable):
        self.pushButton_sync.setEnabled(enable)
        self.radioButton_deviceLeader.setEnabled(enable)
        self.radioButton_PcLeader.setEnabled(enable)
        self.checkBox_deleteOldFiles.setEnabled(enable)
        self.checkBox_copyNewFiles.setEnabled(enable)
        self.pushButton_selectPcPath.setEnabled(enable)
        self.pushButton_selectDevicePath.setEnabled(enable)
        self.pushButton_clearPcFolder.setEnabled(enable)
        self.pushButton_clearDeviceFolder.setEnabled(enable)



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
