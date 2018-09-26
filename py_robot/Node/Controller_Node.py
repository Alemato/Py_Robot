#! /usr/bin/python

import rospy
import py_robot.msg as PyRobot
import random


motor_pub = PyRobot.Controller_Node()
prolog_pub = PyRobot.Prolog_Node()
lidar_pub = PyRobot.Lidar_Compass_Node()



def callback(msg):
    appoggio = msg.switches

    rospy.loginfo(appoggio)

def main():
    rospy.init_node("nodo_sottoscrittore")
    motor_pub = rospy.Publisher("motor_pub", PyRobot.Controller_Node, queue_size=1)
    prolog_pub = rospy.Publisher("prolog_pub", PyRobot.Prolog_Node, queue_size=1)
    lidar_pub = rospy.Publisher("lidar_pub", PyRobot.Lidar_Compass_Node, queue_size=1)
    motor_sub = rospy.Subscriber("switches", PyRobot.Motor_Switch_Node, callback)
    lidar_sub = rospy.Subscriber("lidar_compass", PyRobot.Lidar_Compass_Node, callback)
    prolog_sub = rospy.Subscriber("prolog_sub", PyRobot.Prolog_Node, callback)
    sonar_sub = rospy.Subscriber("sonar", PyRobot.Sonar_Volt_Node, callback)

    r = rospy.Rate(1)

    while not rospy.is_shutdown():
        motor_pub.vel = random.choice('abc')
        motor_pub.on_off_lidar = True
        motor_pub.prolog = 'ciao1'
        lidar_pub.lidar = [2.12, 1.2]
        lidar_pub.angle16 = 200
        lidar_pub.angle8 = 18
        lidar_pub.pitch = 10
        lidar_pub.roll = 19
        lidar_pub.mag = [1, 2, 3, 4, 5, 6]
        lidar_pub.acc = [10, 20, 30, 40, 50, 60]
        lidar_pub.gyro = [100, 200, 300, 400, 500, 600]
        lidar_pub.temp = 29
        motor_pub.publish(motor_pub.on_off_lidar, motor_pub.vel, motor_pub.prolog)
        prolog_pub.publish('ciao')
        lidar_pub.publish(lidar_pub.lidar, lidar_pub.angle16, lidar_pub.angle8, lidar_pub.pitch, lidar_pub.roll, lidar_pub.mag, lidar_pub.acc, lidar_pub.gyro, lidar_pub.temp)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
