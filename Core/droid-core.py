
# sys.path.insert( 0, os.path.dirname( __file__ ) )

import time
import sys

from logger import DLogger as logger

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyleFactory

from entities.manager import PeripheralManager as PManager


class DroidCore(logger, QMainWindow):
    """"""
    def __init__(self):
        """ """
        super(QMainWindow, self).__init__()
        super(DroidCore, self).__init__( __file__, self.__class__.__name__ )

        # create Peripheral Manager
        self.pmanager = PManager()

    def closeEvent(self, event):
        self.pmanager.stop()
        super().closeEvent(event)





# program start here
if __name__ == '__main__':

    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))

    # create core class
    droid_core = DroidCore()

    # --- logging
    droid_core.logging_on('DEBUG')
    # droid_core.pmanager.logging_on('DEBUG')
    # droid_core.pmanager.hal.logging_on()
    # droid_core.pmanager.nmmp.logging_on()

    # manual create peripherals mac/ip
    sb_mac = 0x00000010

    droid_core.pmanager.new( 'Sensor Block 0', 0x00, sb_mac )
    droid_core.pmanager.new( 'SB0 internal temp', 0x01, sb_mac )
    droid_core.pmanager.new( 'temp', 0x55, sb_mac )

    droid_core.show()
    # droid_core.logging_on('INFO')
    sys.exit(app.exec_())
