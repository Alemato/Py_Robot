#! /usr/bin/python
import random

import rospy
import py_robot.msg as PyRobot

sonar_msg = PyRobot.Lidar_Compass_Node()


def talker():
    pub = rospy.Publisher('lidar_compass', PyRobot.Lidar_Compass_Node, queue_size=1)
    rospy.init_node('talker')
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        sonar_msg.lidar = [random.randint(0, 100) * 0.1 for x in range(0, 181)]
        sonar_msg.angle16 = random.randint(0, 16)
        sonar_msg.angle8 = random.randint(0, 10)
        sonar_msg.pitch = random.randint(0, 7)
        sonar_msg.roll = random.randint(0, 5)
        sonar_msg.mag = [random.randint(0, 6) for x in range(0, 6)]
        sonar_msg.acc = [random.randint(0, 6) for x in range(0, 6)]
        sonar_msg.gyro = [random.randint(0, 6) for x in range(0, 6)]
        sonar_msg.temp = random.randint(0, 24)
        pub.publish(sonar_msg)

        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
