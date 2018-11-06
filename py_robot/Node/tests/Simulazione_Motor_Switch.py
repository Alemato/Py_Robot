#! /usr/bin/python

import random
import rospy
import py_robot.msg as PyRobot

switch = PyRobot.Motor_Switch_Node()


def callback(msg):
    velo = msg.velo
    rospy.loginfo(velo)


def main():
    rospy.init_node('Motor_Switch_Node')
    rospy.Subscriber("controller_To_Motor", PyRobot.Controller_To_Motor_Node, callback)
    switch_pub = rospy.Publisher("switches", PyRobot.Motor_Switch_Node, queue_size=1)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        switch.switches = [random.choice([True, False]), random.choice([True, False]),random.choice([True, False])]
        switch_pub.publish(switch)
        rospy.loginfo(switch)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass