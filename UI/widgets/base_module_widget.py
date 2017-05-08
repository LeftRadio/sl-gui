
import os
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap

import widgets.res.wresources


class BaseModuleWidget(QPushButton):
    """docstring for BaseModuleWidget"""

    changed_signal = pyqtSignal(str, object)

    def __init__(self, ids, ui='', name='NAME', group ='', pixtitle='', parent=None):
        super(BaseModuleWidget, self).__init__(parent)
        #
        self.ids = ids
        self._name = name
        self._group = group
        self._pixtitle = QPixmap( pixtitle )
        try:
            self._pixtitle_xy = self._pixtitle.width() / self._pixtitle.height()
        except ZeroDivisionError:
            self._pixtitle_xy = 1
        #
        self.init_ui( ui )

    def init_ui(self, filename):
        selfdir = os.path.dirname(__file__)
        try:
            uipath = os.path.join(selfdir, filename)
            self.uic = uic.loadUi(uipath, self)
        except Exception:
            pass

    def mousePressEvent(self, event):
        self.changed_signal.emit( 'clicked', {} )
        super().mousePressEvent(event)

    @property
    def group(self):
        return self._group
    @group.setter
    def group(self, text):
        self._group = text
        self.changed_signal.emit( 'group', {'text': text} )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, text):
        old = self._name
        self._name = text
        self.changed_signal.emit( 'name', {'text': text, 'old': old} )

    @property
    def pixtitle(self):
        return self._pixtitle

    @pixtitle.setter
    def pixtitle(self, file):
        if file == '':
            file, _ = QFileDialog.getOpenFileName(
                self,
                "Image Files",
                "",
                "Image Files (*.gif, *.png *.jpg *.bmp)"
            )
        if file == '':
            return

        self._pixtitle = QPixmap(file)
        try:
            self._pixtitle_xy = self._pixtitle.width() / self._pixtitle.height()
        except ZeroDivisionError:
            pass

        self.changed_signal.emit( 'pixtitle', {'file': file} )
