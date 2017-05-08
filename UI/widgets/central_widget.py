#!python3

import os
from PyQt5 import uic
from PyQt5.QtCore import ( Qt, QMimeData, QByteArray, QPropertyAnimation,
                           pyqtSignal, pyqtSlot, QEasingCurve )
from PyQt5.QtWidgets import ( QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                              QPushButton, QSpacerItem, QSizePolicy )
from PyQt5.QtGui import QDrag

from widgets.module_widget import ModuleWidget
from widgets.sensor_widget import SensorWidget
from widgets.group_widget import GroupWidget, NavigationButton
from widgets.sc_regul_widget import SC_Regul_Widget


class NavigationWidget(QWidget):

    widget_changed = pyqtSignal(str, dict)

    """docstring for NavigationWidget"""
    def __init__(self, parent=None):
        super(NavigationWidget, self).__init__(parent)
        #
        spacer_layout = QHBoxLayout()
        self.btn_layout = QHBoxLayout()
        spacer_layout.addLayout( self.btn_layout )
        spacer_layout.addSpacerItem( QSpacerItem(0, 20, QSizePolicy.Expanding) )
        self.setLayout(spacer_layout)
        #
        self.buttons = {}

    def add_button(self, btn):
        #
        btn.clicked.connect( self.button_clicked )
        #
        self.btn_layout.addWidget( btn )
        #
        self.buttons[btn.ids] = btn
        # return btn

    def remove_button(self, name):
        try:
            self.buttons[name].setParent(None)
            del( self.buttons[name] )
        except Exception as e:
            pass
            # print(e)

    def clear(self):
        [ b.setParent(None) for b in self.buttons.values() ]
        self.buttons.clear()

    def button_clicked(self, sender=None):
        if not sender:
            sender = self.sender()

        for b in self.buttons.values():
            b.setChecked(False)
            b.setStyleSheet('')

        sender.setChecked(True)
        sender.setStyleSheet('background-color: rgba(128, 24, 24, 168);\ncolor: rgb(255, 255, 255);')
        sender.update()

        # self.widget_changed.emit( 'clicked', {} )


class DragDropWidget(QWidget):
    """docstring for DragDropWidget"""
    def __init__(self, parent=None):
        super(DragDropWidget, self).__init__(parent)
        self.widgets = {}
        self.mousepressed = False
        self.mousemoved = False
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        child = self.childAt(event.pos())
        if not child or child not in self.widgets.values():
            return
        self.drop_widget = child
        # print('mousePressEvent: ', event.pos())
        self.mousepressed = True
        self.mousemoved = False

    def mouseMoveEvent(self, event):
        if not self.mousepressed or self.mousemoved:
            return
        itemData = QByteArray()
        mimeData = QMimeData()
        mimeData.setData('application/x-dnditemdata', itemData)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.drop_widget.pixtitle)
        drag.setHotSpot(event.pos() - self.drop_widget.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)
        self.mousemoved = True

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):

            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                self.mousepressed = False
                self.mousemoved = False
                # self.child_drop.emit( self.drop_widget, event.pos() )
                # print('dropEvent: ', self.drop_widget.ids, event.pos())
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()


class ScrollAreaWidget(DragDropWidget):
    """docstring for ScrollAreaWidget"""

    add_widget_req = pyqtSignal()

    def __init__(self, hmax=10, translator=None, parent=None):
        super(ScrollAreaWidget, self).__init__(parent)
        # --- load ui
        selfdir = os.path.dirname(__file__)
        uipath = os.path.join( selfdir, "central_widget.ui" )
        self.uic = uic.loadUi(uipath, self)
        #
        self.gridLayout = QGridLayout( self.scrollArea.widget() )
        #
        self.hmax = hmax
        #
        self.add_button = QPushButton('NEW')
        self.add_button.setMinimumSize(150, 250)
        self.add_button.X = 0
        self.add_button.Y = 0
        self.add_button.clicked.connect( self.widget_clicked_slot )
        #
        self.gridLayout.addWidget( self.add_button, self.add_button.Y, self.add_button.X )
        #
        if translator:
            self.translations_init(translator)
        #
        self.animations_init()

    def animations_init(self):
        self._anim_scrollAreaHScroll = QPropertyAnimation(
            self.scrollArea.horizontalScrollBar(),
            b'value'
        )
        self._anim_scrollAreaHScroll.setEasingCurve(QEasingCurve.OutExpo)
        self.pushButton.clicked.connect(self.start_hscroll_anim)
        self.pushButton_2.clicked.connect(self.start_hscroll_anim)

    def translations_init(self, translator):
        """  """
        self.translator = translator
        for m in self.widgets.values():
            self.translator.add_intent( m.lbl_title.setText, m.title)
        self.translator.update()

    def _set_widget_index(self, widget):
        if len(self.widgets):
            widget.Y  = max( [w.Y for w in self.widgets.values()])
            widget.X = max( [w.X for w in self.widgets.values() if w.Y == widget.Y]) + 1
            if widget.X >= self.hmax:
                widget.X = 0
                widget.Y += 1
        else:
            widget.X = 0
            widget.Y = 0

    def get_widget(self, ids):
        try:
            return self.widgets[ids]
        except Exception as e:
            pass

    def clear(self):
        [ w.setParent(None) for w in self.widgets.values() ]
        self.widgets.clear()

    def add_widget(self, ids, widget):
        """ """
        self.add_button.setParent(None)
        del(self.add_button)

        self._set_widget_index( widget )
        self.widgets[ids] = widget

        self.add_button = QPushButton('NEW')
        self.add_button.setMinimumSize(125, 200)
        self.add_button.setMaximumSize(125, 200)
        self.add_button.clicked.connect( self.widget_clicked_slot )

        self._set_widget_index( self.add_button )

        # print(widget.X, widget.Y)
        # print(self.add_button.X, self.add_button.Y)
        # if self.translator:
        #     self.translator.add_intent(widget.set_title, widget.title)
        #     self.translator.update()

        self.gridLayout.addWidget( widget, widget.Y, widget.X )
        self.gridLayout.addWidget( self.add_button, self.add_button.Y, self.add_button.X )

        widget.clicked.connect( self.widget_clicked_slot )

    @pyqtSlot()
    def widget_clicked_slot(self):
        sender = self.sender()
        if sender == self.add_button:
            self.add_widget_req.emit()
            return

        for m in self.widgets.values():
            m.setChecked(False)
            m.setStyleSheet('')

        sender.setChecked(True)
        sender.setStyleSheet('background-color: rgba(128, 24, 24, 168);\ncolor: rgb(255, 255, 255);')
        sender.update()

    @pyqtSlot()
    def start_hscroll_anim(self):
        sendername = self.sender().objectName()
        print('start_hscroll_anim: ', sendername)
        if 'pushButton' == sendername:
            sm = -250
        elif 'pushButton_2' == sendername:
            sm = +250
        else:
            return
        anim = self._anim_scrollAreaHScroll
        anim.stop()
        anim.setLoopCount(1)
        anim.setDuration(500)
        val = self.scrollArea.horizontalScrollBar().value()
        anim.setStartValue( val )
        anim.setEndValue( val + sm )
        anim.start()


class BlocksWidget(QWidget):
    """docstring for BlocksWidget"""

    block_types = { 'group': GroupWidget, 'modul': ModuleWidget, 'scen': SC_Regul_Widget }

    def __init__(self, hmax=10, translator=None, parent=None):
        super(BlocksWidget, self).__init__(parent)

        self.navigation = NavigationWidget()
        self.scroll_area = ScrollAreaWidget(hmax, translator)

        vlayout = QVBoxLayout(self)
        vlayout.addWidget(self.navigation)
        vlayout.addWidget(self.scroll_area)
        self.setLayout(vlayout)

        self.blocks = {}

        self.add_widget_req = self.scroll_area.add_widget_req

    def add_block(self, btype, slot, ids, kwargs):

        WidgetClass = BlocksWidget.block_types[btype]
        widget = WidgetClass( ids, **kwargs)

        self.scroll_area.add_widget( ids, widget )
        widget.changed_signal.connect(slot)

        if WidgetClass == GroupWidget:
            self.navigation.add_button(widget.navigation_button)

        self.blocks[ids] = widget

    def get_blocks(self, wtype, group):
        #
        if group == 'ALL':
            group_blocks = self.blocks.values()
        else:
            group_blocks = [b for b in self.blocks.values() if group in b.group]
        #
        return [b for b in group_blocks if type(b) == wtype]

    def update_blocks_view(self, wtype, group):
        #
        self.scroll_area.clear()
        #
        if group == 'ROOT':
            wtype = GroupWidget
        elif wtype == 'MODULES':
            wtype = ModuleWidget
        elif wtype == 'SCENARIES':
            wtype = SC_Regul_Widget

        root_blocks = self.get_blocks(GroupWidget, 'ROOT')
        for g in root_blocks:
            if group == g.name:
                self.navigation.button_clicked(
                    sender = g.navigation_button
                )

        for w in self.get_blocks( wtype, group ):
            self.scroll_area.add_widget( w.ids, w )

    def add_root_button(self, slot):
        root_button = NavigationButton(-1, 'ROOT')
        root_button.changed_signal.connect(slot)
        self.navigation.add_button( root_button )
