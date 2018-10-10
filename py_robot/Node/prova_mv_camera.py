#! /usr/bin/python

import random
import rospy
import py_robot.msg as PyRobot

mv_camera = PyRobot.MV_Camera_Node()


def main():
    rospy.init_node('MV_Camera_Node')
    mv_camera_pub = rospy.Publisher("mv_camera_sub", PyRobot.MV_Camera_Node, queue_size=1)
    r = rospy.Rate(5)
    while not rospy.is_shutdown():
        mv_camera.eureca = 'trovato'
        mv_camera_pub.publish(mv_camera)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass