import paho.mqtt.client as mqtt
import time

class Subscriber:
    def subscribeToQueue(self):
        self.client = mqtt.Client()
        self.url="inbound"
        self.client.connect("localhost", 1883, 10)
        self.client.loop_start()
        self.client.on_message = self.on_message
        self.client.on_disconnect=self.on_disconnect
        self.client.subscribe(self.url)


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        flags = True;

    def on_message(self, client, userdata, msg):
        print("Message --- "+str(msg.payload))
        self.flag = False;
        client.disconnect()

    def on_disconnect(self, client, userdata, msg):
        print('Disconnect')
        self.flag=False;

mqtt12= Subscriber()
mqtt12.subscribeToQueue()