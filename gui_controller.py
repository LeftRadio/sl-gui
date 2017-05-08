
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from Core.mqttc import MQTT_GUIClient
from UI.mainui import GUI_MainWindow


class GUI_Controller(QObject):

    sub_topic = pyqtSignal(str)
    pub_message = pyqtSignal(str, str)

    """docstring for GUI_Controller"""
    def __init__(self, parent=None):
        super(GUI_Controller, self).__init__(parent)

    @pyqtSlot(str)
    def new_topic(self, topic):
        print('new_topic: ', topic)

    @pyqtSlot(str, str)
    def new_message(self, topic, msg):
        print('new_message: ', topic, msg)



if __name__ == '__main__':
    main()