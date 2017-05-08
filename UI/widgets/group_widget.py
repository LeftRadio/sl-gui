#!python3

from PyQt5.QtCore import QRectF, QRect, QPropertyAnimation
from PyQt5.QtGui import QPixmap, QBrush, QColor, QPainter, QPen, QPolygon, QPixmap
from PyQt5.QtWidgets import QPushButton
from widgets.base_module_widget import BaseModuleWidget
from widgets.res.pixfiles import pixfiles


class NavigationButton(BaseModuleWidget):
    """docstring for NavigationButton"""
    def __init__(self, ids, name='', parent=None):
        super(NavigationButton, self).__init__(ids, name=name, parent=parent)
        self.setText( name )


class GroupWidget(BaseModuleWidget):
    """docstring for GroupWidget"""
    def __init__(self, ids, name='NEW GROUP', group='ROOT', pixtitle=pixfiles['GROUP'], parent=None):
        super(GroupWidget, self).__init__(ids, 'group.ui', name, group, pixtitle, parent)
        #
        self.lineEdit.setText(self.name)
        self.lineEdit.editingFinished.connect(self.edit_rename)
        #
        self.open_file_icon = QPixmap(':/icons/pixmap/add_photo_48.png')
        self.open_pixmap_file = False
        #
        self.lbl_pix_title.paintEvent = self.pixmapPaintEvent
        #
        self.navigation_button = NavigationButton(ids, name)
        self.navigation_button.changed_signal = self.changed_signal

    def pixmapPaintEvent(self, event):
        painter = QPainter()
        painter.begin(self.lbl_pix_title)
        #
        pix_height = self.lbl_pix_title.width() / self._pixtitle_xy
        pix_y0 = ( self.lbl_pix_title.height() - pix_height ) / 2
        painter.drawPixmap( QRect(0, pix_y0, self.lbl_pix_title.width(), pix_height), self.pixtitle )
        #
        openicon_width = self.lbl_pix_title.width() // 8
        painter.drawPixmap( QRect(12, self.height()-54-openicon_width, openicon_width, openicon_width), self.open_file_icon )
        #
        painter.end()

    def mousePressEvent(self, event):
        if self.targetSquare( event.pos() ):
            self.open_pixmap_file = True
            self.update()
        else:
            super().mousePressEvent(event)

    def update(self):
        super().update()
        if self.open_pixmap_file:
            self.open_pixmap_file = False
            self.open_file_icon = QPixmap(':/icons/pixmap/add_photo_48_act.png')
            self.lbl_pix_title.update()
            # --- set empty filename for auto open filedialog
            self.pixtitle = ''
        self.open_file_icon = QPixmap(':/icons/pixmap/add_photo_48.png')
        self.lbl_pix_title.update()

    def targetSquare(self, pos):
        x0 = self.lbl_pix_title.pos().x()
        y0 = self.lbl_pix_title.pos().y()
        openicon_width = self.lbl_pix_title.width() // 8
        if pos.x() >= x0 and pos.x() <= x0 + openicon_width:
            if pos.y() >= y0 + self.height()-54-openicon_width and pos.y() <= y0 + self.height()-54:
                return True
        return False

    def edit_rename(self):
        self.name = self.lineEdit.text()
        self.navigation_button.setText( self.name )
