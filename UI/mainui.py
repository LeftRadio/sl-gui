
import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication, QStyleFactory, QMainWindow

from translations import Translator
from widgets.central_widget import BlocksWidget


class GroupController(QObject):
    """docstring for GroupControllerme"""

    ids = 0

    gui_add_block_signal = pyqtSignal(str, object, int, dict)

    def __init__(self, view, parent=None):
        """ """
        super(GroupController, self).__init__(parent)

        self.view = view
        self.view.add_root_button( self.select_group )

        self._active_group = 'ROOT'
        self._modules_scenaries = 'MODULES'

    def change_module_scen(self, text):
        assert text == 'MODULES' or text == 'SCENARIES'
        self._modules_scenaries = text
        self.view.update_blocks_view( text, self._active_group )

    def gui_add_block_request_slot(self):
        print('gui_add_block_request_slot')
        if self._active_group == 'ROOT':
            self.add_group()
        else:
            if self._modules_scenaries == 'MODULES':
                self.add_module()
            else:
                pass

    # -------------------------------------------------------------------------

    def add_group(self, name='NEW GROUP'):
        ids = GroupController.ids
        self.view.add_block( 'group', self.select_group, ids, {'name': name, 'group': 'ROOT'} )
        GroupController.ids += 1

    def add_module(self, model='SL-ESP-UM-012'):
        ids = GroupController.ids
        self.view.add_block( 'modul', self.select_module, ids, {'title': 'ESP MODULE', 'model': model, 'group': self._active_group} )
        GroupController.ids += 1

    def add_scenaries(self):
        pass

    def select_group(self, event, data):
        sender = self.sender()
        print( 'select_group', sender.name, event, data )

        if event == 'clicked':
            self._active_group = sender.name
            self.view.update_blocks_view( self._modules_scenaries, self._active_group )
        elif event == 'name':
            for b in self.view.get_blocks( self._modules_scenaries, data['old'] ):
                b.group = data['text']

    def select_module(self, event, data):
        print( 'select_module', self.sender(), event, data )

    def select_scenaries(self, event, data):
        print( 'select_scenaries', self.sender(), event, data )


class GUI_MainWindow(QMainWindow):
    """docstring for GUI_MainWindow"""

    change_module_scen = pyqtSignal(str)

    def __init__(self, parent=None):
        super(GUI_MainWindow, self).__init__(parent)

        # --- load UI, create Translator
        self.uic = uic.loadUi("main.ui", self)
        self.translator = Translator()

        central_widget = BlocksWidget(hmax=4, translator=self.translator)
        self.setCentralWidget( central_widget )

        self.group_controller = GroupController(view=central_widget)

        central_widget.add_widget_req.connect( self.group_controller.gui_add_block_request_slot )
        self.change_module_scen.connect( self.group_controller.change_module_scen )

        #
        self.toolBar.actionTriggered.connect( self.tool_bar_action )
        #
        self.styles_init()
        #
        self.translations_init()

        self.setWindowFlags(Qt.SplashScreen)

    def styles_init(self):
        self.actionStyleLight.triggered.connect( self.view_style )
        self.actionStyleDark.triggered.connect( self.view_style )

    def translations_init(self):
        """  """
        tr = self.translator
        #
        for name, code in tr.languages:
            act = QAction(name, parent=self.menuLanguage)
            act.setObjectName(name)
            act.triggered.connect( tr.change_translation )
            self.menuLanguage.addAction( act )
        #
        tr.add_intent( self.menuFile.setTitle, 'File')
        tr.add_intent( self.actionCrete_new_config.setText, 'Crete new config')
        tr.add_intent( self.actionLoad_config.setText, 'Load config')
        tr.add_intent( self.actionSave_active_config.setText, 'Save active config')
        #
        tr.add_intent( self.menuView.setTitle, 'View')
        tr.add_intent( self.menuViewStyle.setTitle, 'Style')
        tr.add_intent( self.actionStyleLight.setText, 'Light')
        tr.add_intent( self.actionStyleDark.setText, 'Dark')
        #
        tr.add_intent( self.menuSettings.setTitle, 'Settings')
        tr.add_intent( self.menuLanguage.setTitle, 'Language')
        #
        tr.update()

    @pyqtSlot()
    def view_style(self):
        sendername = self.sender().objectName()
        print(sendername)
        if 'Light' in sendername:
            self.setStyleSheet("")
            self.menubar.setStyleSheet("")
        elif 'Dark' in sendername:
            self.setStyleSheet("background-color: rgb(76, 76, 76);\ncolor: rgb(255, 255, 255);")
            self.menubar.setStyleSheet("background-color: rgb(54, 64, 74);\ncolor: rgba(255, 255, 255, 224);")

    @pyqtSlot(QAction)
    def tool_bar_action(self, action):
        [ a.setChecked(False) for a in self.toolBar.actions() if a != action ]
        self.change_module_scen.emit( action.text() )


# ----
if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setApplicationName('SmartLogic Control Panel GUI')
    QApplication.setStyle( QStyleFactory.create('Fusion') )

    main = GUI_MainWindow()
    main.group_controller.add_group(name='ALL')

    main.show()
    sys.exit(app.exec_())
