#! /usr/bin/python

import random
import rospy
import py_robot.msg as PyRobot


pi_camera = PyRobot.Pi_Camera_Node()


def main():
    rospy.init_node('Pi_Camera_Node')
    pi_camera_pub = rospy.Publisher("pi_camera", PyRobot.Pi_Camera_Node, queue_size=1)
    r = rospy.Rate(5)
    while not rospy.is_shutdown():
        pi_camera.visione = random.choice(['dritto', 'destra', 'sinistra'])
        pi_camera_pub.publish(pi_camera)
        rospy.loginfo(pi_camera)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass