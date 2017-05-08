#!python3

from PyQt5.QtGui import QPainter, QColor, QPixmap
from widgets.base_module_widget import BaseModuleWidget
from widgets.res.pixfiles import pixfiles


class ModuleWidget(BaseModuleWidget):
    """docstring for ModuleWidget"""
    def __init__(self, ids, ui='module_widget.ui', name='NAME', group='', title='', model='', pixtitle='', parent=None):
        super(ModuleWidget, self).__init__(ids, ui, name, group, pixfiles.get(model, pixtitle), parent)
        #
        self.setCheckable(True)
        #
        self.lineEditGroup.setText(self._group)
        self.lineEditGroup.editingFinished.connect(self.edit_regroup)
        #
        self.lineEditName.setText(self.name)
        self.lineEditName.editingFinished.connect(self.edit_rename)
        #
        self.lbl_pix_title.setPixmap( self.pixtitle )
        self.lbl_pix_title.setMinimumSize(120, 10)
        self.lbl_pix_title.update()
        #
        self.lbl_title.setText(title)
        #
        self.lbl_model.setText(model)
        #
        self.setMinimumSize(140, 120)
        self.setMaximumSize(140, 250)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(192, 16, 0))
        for i in range(1, 3):
            painter.drawLine(40, 5*i, 100, 5*i)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.parent:
            self.parent().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.parent:
            self.parent().mouseMoveEvent(event)

    def edit_rename(self):
        self.name = self.lineEditName.text()

    def edit_regroup(self):
        self.group = self.lineEditGroup.text()

    @property
    def group(self):
        return self._group
    @group.setter
    def group(self, text):
        old = self._group
        self._group = text
        self.lineEditGroup.setText(text)
        self.changed_signal.emit( 'group', {'text': text, 'old': old} )
