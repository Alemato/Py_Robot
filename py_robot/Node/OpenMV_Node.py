#! /usr/bin/python

import py_robot.msg as PyRobot
import rospy
import serial

openmv_msg = PyRobot.MV_Camera_Node()


def mvcamera(ser):
    while True:
        ser_bytes = ser.readline()
        return ser_bytes


def main():
    rospy.init_node("OpenMV_Node")
    mv_camera = rospy.Publisher("mv_camera", PyRobot.MV_Camera_Node, queue_size=1)
    r = rospy.Rate(1)
    ser = serial.Serial("/dev/ttyACM0")
    ser.flushInput()
    while rospy.is_shutdown():
        openmv_msg.eureca = mvcamera(ser)
        mv_camera.publish(openmv_msg)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass