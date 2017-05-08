
# import random
import threading
from queue import Queue

from logger import DLogger as logger

from PyQt5.QtCore import Qt, QObject, QTimer, QVariant, pyqtSignal, pyqtSlot

from nmmp.hal.vcom_usart import NUSARTInterface as NUSART
from nmmp.nmmp import NMMP_NET, NMMP_Entity

from entities.commands import app_command_code as app_cmd


class Peripheral(NMMP_Entity):
    """docstring for Peripheral"""
    def __init__(self, name, ip, mac32):
        super(Peripheral, self).__init__(name, ip, mac32)
        pass


class PeripheralPackedFormatter(object):
    """docstring for PeripheralPackedFormatter"""
    def format(self, name, data):
        """ """
        packed = bytearray()
        packed.append( app_cmd[name] )
        packed.extend( bytearray( list(data) ) )

        return packed


class PeripheralInterface(object):
    """docstring for PeripheralInterface"""
    def __init__(self):
        pass


class PeripheralManager(logger, QObject):
    """docstring for PeripheralManager"""

    _on_send_signal = pyqtSignal(QVariant, bytearray)

    device_connect_signal = pyqtSignal(QVariant, bytearray)
    device_disconnect_signal = pyqtSignal(QVariant, bytearray)
    device_deadtime_signal = pyqtSignal(QVariant, bytearray)

    task_done_signal = pyqtSignal()

    def __init__(self):
        #
        super(QObject, self).__init__()
        super(PeripheralManager, self).__init__(
            __file__,
            self.__class__.__name__ )
        #
        self._timer = None
        #
        self._autoscan = False
        #
        self._devices = []

        # --- queue, threads, worker
        # Create the queue for threads, threads
        self.nqueue = Queue()
        t = threading.Thread( target = self._worker )
        t.daemon = True  # thread dies when main thread exits.
        t.start()

        # create HAL object
        self.hal = NUSART( name='CP210x', baudrate=921600 )
        # create NMMP [ Network, Datalink ] layers
        self.nmmp = NMMP_NET( self.hal )
        #
        self._on_send_signal.connect( self._on_send )
        self.nmmp.read_complite.connect( self._on_recive )
        #
        self.packedformatter = PeripheralPackedFormatter()

    @property
    def autoscan(self):
        return self._autoscan

    @logger.wrap('INFO')
    def _init_timer(self, period):
        """  """
        self._timer = QTimer()
        self._timer.setInterval(period)
        self._timer.setTimerType(Qt.CoarseTimer) # PreciseTimer
        self._timer.timeout.connect(self._on_timer)
        self._timer.start()

    @logger.wrap('INFO')
    def _deinit_timer(self):
        self._timer.stop()
        self._timer.timeout.disconnect(self._on_timer)
        self._timer = None

    # --- Autoscanning
    def autoscan_on(self, **kwargs):
        """ """
        self._deinit_timer()
        #
        if self.hal.isOpen():
            period = kwargs.get( 'period', self._timer.interval() )
            self._init_timer(period)
        #
        self._autoscan = True

    def autoscan_off(self, **kwargs):
        """  """
        self._deinit_timer()
        self._autoscan = False

    # --- Connection
    @logger.wrap('DEBUG')
    def connect(self):

        hstate = self.hal.open()
        if hstate:
            if self._autoscan:
                self._init_timer()

        return (hstate, )

    @logger.wrap('DEBUG')
    def disconnect(self):
        if self._autoscan:
            self._deinit_timer()
        return self.hal.close()

    # --- Devices
    @logger.wrap('INFO')
    def add_device(self, name, ip, mac):
        entity = NMMP_Entity( name, ip, mac )
        self._devices.append( entity )
        return True

    def clear_devices(self):
        """ """
        pass

    def update_devices(self):
        """ """
        self.queue.put('scan all')

    # --- Recive
    def _get_dev_from_ip(self, ip):
        for dev in self._devices:
            if ip == dev.ip:
                return dev
        return None

    @pyqtSlot(int, bytearray)
    @logger.wrap('DEBUG')
    def _on_recive(self, ip, app_packed):
        dev = self._get_dev_from_ip( ip )
        if dev is not None:
            dev.on_recive( app_packed )
            return True

    # --- Send
    @pyqtSlot(QVariant, bytearray)
    @logger.wrap('DEBUG')
    def _on_send(self, dev, data):
        return self.nmmp.send(dev, data)

    # ---
    def _worker(self):
        """ Main worker in self thread """
        while True:
            item, data = self.nqueue.get()

            with threading.Lock():
                if item == 'scan all':
                    pass
                    # if scan ok add finded devices to self dev list
                if item == 'get-description':
                    for dev in self._devices:
                        # format app data
                        app_packed = self.packedformatter.format( item, data )
                        # send
                        self._on_send_signal.emit( dev, app_packed )
            #
            self.nqueue.task_done()
            #
            self.task_done_signal.emit()

    @pyqtSlot()
    @logger.wrap('DEBUG')
    def _on_timer(self):
        #
        test_request = ( 'get-description', [0xEE] )
        #
        self.nqueue.put( test_request )

        return True


