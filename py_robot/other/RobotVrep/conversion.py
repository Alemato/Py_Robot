import paho.mqtt.client as mqtt

def on_message(client1, userdata, msg):
    print("message received ", str(msg.payload.decode("utf-8")))
    client.publish("topi/test", "Hello world!2")

client = mqtt.Client()
client.connect("localhost", 1883, 60)
while True:
    client.publish("topi/test", "Hello world!1")
    client1 = mqtt.Client()
    client1.connect("localhost", 1883, 60)
    client1.subscribe("topic/test1")
    client1.on_message = on_message
    client1.loop_forever()