

#!python3

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame, QPushButton, QToolButton, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor
try:
    from res.wresources import wresources
except Exception:
    try:
        from widgets.res.wresources import wresources
    except Exception:
        pass


class SensorWidget(QWidget):
    """docstring for SensorWidget"""
    def __init__(self, ids, title='', model='', pixfile='', parent=None):
        super(SensorWidget, self).__init__(parent)
        # --- load ui
        selfdir = os.path.dirname(__file__)
        uipath = os.path.join( selfdir, "temp_sensor.ui" )
        self.uic = uic.loadUi(uipath, self)
