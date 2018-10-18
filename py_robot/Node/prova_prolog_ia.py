#! /usr/bin/python

import random
import rospy
import py_robot.msg as PyRobot


comando = PyRobot.Prolog_IA_Node()


def callback(msg):
    controller = msg
    rospy.loginfo(controller)


def main():
    rospy.init_node('Prolog_IA_Node')
    rospy.Subscriber("controller", PyRobot.Controller_Node, callback)
    comando_pub = rospy.Publisher("prolog", PyRobot.Prolog_IA_Node, queue_size=1)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        comando.risposta = random.choice(['dritto', 'destra', 'sinistra', 'indietro','dritto', 'destra', 'sinistra', 'indietro', 'stop', 'fine'])
        comando_pub.publish(comando)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
