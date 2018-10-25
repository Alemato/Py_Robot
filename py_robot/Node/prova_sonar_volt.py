#! /usr/bin/python

import random
import rospy
import py_robot.msg as PyRobot

sonar_volt = PyRobot.Sonar_Volt_Node()



def main():
    rospy.init_node('Sonar_Volt_Node')
    sonar_volt_pub = rospy.Publisher('sonar_volt', PyRobot.Sonar_Volt_Node, queue_size=1)
    r = rospy.Rate(5)
    while not rospy.is_shutdown():
        sonar_volt.sonar = [random.uniform(10, 50), random.uniform(10, 50), random.uniform(10, 50)]
        sonar_volt.volt = 13
        sonar_volt_pub.publish(sonar_volt)
        rospy.loginfo(sonar_volt)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
