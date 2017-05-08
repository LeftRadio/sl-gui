#!/usr/bin/python


import sys
import paho.mqtt.client as mqtt
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class MQTT_GUIClient(QObject, mqtt.Client):

    new_topic = pyqtSignal(str)
    new_message = pyqtSignal(str, str)

    """docstring for MQTT_GUIClient"""
    def __init__(self, cid='', parent=None):
        super(QObject, self).__init__(parent)
        super(mqtt.Client, self).__init__()

        self._registered_topics = []

    def on_connect(self, client, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, client, obj, msg):
        print('on_message: ', msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        if msg.topic not in self._registered_topics:
            self._registered_topics.append(msg.topic)
            self.new_topic.emit( msg.topic )
        self.new_message.emit( msg.topic, msg.payload )

    def on_publish(self, client, obj, mid):
        print("on_publish mid: "+str(mid))

    def on_subscribe(self, client, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, client, obj, level, string):
        print('on_log: ', level, string)




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

    mqttc = MQTT_GUIClient("SL-GUI")
    mqttc.connect("iot.eclipse.org", 1883, 10)
    mqttc.subscribe("/SL/#", 0)
    mqttc.loop_forever()
