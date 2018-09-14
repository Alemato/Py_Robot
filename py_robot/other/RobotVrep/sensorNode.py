#! /usr/bin/env python
import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt

global pub, rate

def on_message(client, userdata, msg):
    global pub, rate
    rospy.loginfo(str(msg.payload.decode("utf-8")))
    pub.publish(str(msg.payload.decode("utf-8")))
    rate.sleep()

def talker():
    global pub, rate
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.subscribe("topic/sense")
    pub = rospy.Publisher('read-sense', String)
    rospy.init_node('sense')
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        client.on_message = on_message
        client.loop_forever()



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
