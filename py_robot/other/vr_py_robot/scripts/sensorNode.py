#! /usr/bin/env python
import rospy
from std_msgs.msg import String

import socket


def conn():
    host_server = "localhost"
    port_server = 50043
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host_server, port_server))
    return client


def talker():
    client = conn()

    pub = rospy.Publisher('read-sense', String)
    rospy.init_node('sense')
    while not rospy.is_shutdown():
        data = client.recv(1024).decode()
        client.send('ciao')
        rospy.loginfo(data)
        pub.publish(data)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
