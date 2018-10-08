#! /usr/bin/python

import rospy
import py_robot.msg as PyRobot

controller_msg = PyRobot.Controller_Node()
global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar

angle16 = None
angle8 = None
pitch = None
roll = None
mag = [None for x in range(0, 5)]
acc = [None for x in range(0, 5)]
gyro = [None for x in range(0, 5)]
temp = None
lidar = [None for x in range(0, 180)]

def callback_prolog(msg):
    comando = ""
    risposta_prolog = msg.risposta
    if risposta_prolog == 'dritto':
        comando = "e"
    elif risposta_prolog == 'destra':
        comando = "r"
    elif risposta_prolog == 'sinistra':
        comando = "q"
    elif risposta_prolog == 'indietro':
        comando = "i"
    elif risposta_prolog == 'stop':
        comando = "s"
    else:
        rospy.loginfo(risposta_prolog + 'message error')
    return comando


def callback_switch(msg):
    switch = msg.switch
    return switch


def callback_sonar_volt(msg):
    sonar = msg.sonar
    volt = msg.volt
    return sonar, volt


def callback_lidar_compass(msg):
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar
    lidar = msg.lidar
    angle16 = msg.angle16
    angle8 = msg.angle8
    pitch = msg.pitch
    roll = msg.roll
    mag = msg.mag
    acc = msg.acc
    gyro = msg.gyro
    temp = msg.temp
    print("riceve", lidar, angle16, angle16,pitch, roll, mag, acc, gyro, temp)





def callback_mvcamera(msg):
    eureca = msg.eureca


def main():
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar
    rospy.init_node("Controller_Node")
    controller_pub = rospy.Publisher("motor_pub", PyRobot.Controller_Node, queue_size=1)
    # prolog_sub = rospy.Subscriber("prolog_sub", PyRobot.Prolog_Node, callback_prolog)
    # switch_sub = rospy.Subscriber("switch_sub", PyRobot.Motor_Switch_Node, callback_switch)
    # sonar_sub, volt_sub = rospy.Subscriber("sonar_volt", PyRobot.Sonar_Volt_Node, callback_sonar_volt)
    # mv_camera = rospy.Subscriber("mv_camera", PyRobot.MV_Camera_Node, callback_mvcamera)
    #lidar_compass_sub = rospy.Subscriber("sonar_volt", PyRobot.Lidar_Compass_Node, callback_lidar_compass)

    r = rospy.Rate(1)
    rospy.Subscriber("lidar_compass", PyRobot.Lidar_Compass_Node, callback_lidar_compass)
    while not rospy.is_shutdown():
        if angle8 is not None:
            controller_msg.lidar = lidar
            controller_msg.angle16 = angle16  # messaggio per il nodo Prolog per angle16
            controller_msg.angle8 = angle8  # messaggio per il nodo Prolog per angle8
            controller_msg.pitch = pitch  # messaggio per il nodo Prolog per pitch
            controller_msg.roll = roll  # messaggio per il nodo Prolog per roll
            controller_msg.mag = mag  # messaggio per il nodo Prolog per mag
            controller_msg.acc = acc  # messaggio per il nodo Prolog per acc
            controller_msg.gyro = gyro  # messaggio per il nodo Prolog per gyro
            controller_msg.temp = temp  # messaggio per il nodo Prolog per temp
            print("___")
            print("invia ", lidar, angle16, angle16, pitch, roll, mag, acc, gyro, temp)
            print("___")
            controller_pub.publish(controller_msg)
            rospy.loginfo(controller_msg)
            r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
