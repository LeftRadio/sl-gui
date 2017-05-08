
from PyQt5.QtCore import QRectF, QRect, QPropertyAnimation
from PyQt5.QtGui import QPixmap, QBrush, QColor, QPainter, QPen, QPolygon, QImage
from widgets.base_module_widget import BaseModuleWidget


class SC_Regul_Widget(BaseModuleWidget):
    """docstring for SC_Regul_Widget"""
    def __init__(self, ids, name='NAME', pixfile=':/scenaries/pixmap/sc_reg.png', parent=None):
        super(SC_Regul_Widget, self).__init__(ids, ui='sc_timer_widget.ui', title='THERMO REGULATE', name=name, pixfile=pixfile, parent=parent)

