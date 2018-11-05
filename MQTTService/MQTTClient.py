import paho.mqtt.client as mqtt

class MqttClientCall:
    def callmqttbroker(self, queue_name, message):
        client = mqtt.Client()
        client.connect("localhost", 1883)
        client.publish(queue_name, message);
        client.disconnect();

mqtt12= MqttClientCall()
mqtt12.callmqttbroker("inbound","hello")