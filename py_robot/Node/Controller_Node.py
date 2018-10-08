#! /usr/bin/python

import rospy
import py_robot.msg as PyRobot

controller_msg = PyRobot.Controller_Node()


class lidar_compass:
    def __init__(self, pos_lidar, angle16, angle8, pitch, roll, mag, acc, gyro, temp):
        self.pos_lidar = pos_lidar
        self.angle16 = angle16
        self.angle8 = angle8
        self.pitch = pitch
        self.roll = roll
        self.mag = mag
        self.acc = acc
        self.gyro = gyro
        self.temp = temp


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
    appoggio = 0
    appoggio_media = 0
    pos_lidar = []
    t = 0
    for j in range(0, 18):
        #i = 0
        for i in range(0, 10):
        #while i < 10:
            appoggio = appoggio + msg.lidar[t]
            #i = i+1
            t = t+1
        appoggio_media = appoggio / 10
        pos_lidar[j] = appoggio_media

    angle16 = msg.angle16
    angle8 = msg.angle8
    pitch = msg.pitch
    roll = msg.roll
    mag = msg.mag
    acc = msg.acc
    gyro = msg.gyro
    temp = msg.temp

    rospy.loginfo(pos_lidar)

    lidar_compass_sub = lidar_compass(pos_lidar, angle16, angle8, pitch, roll, mag, acc, gyro, temp)

    return lidar_compass_sub


def callback_mvcamera(msg):
    eureca = msg.eureca


def main():
    rospy.init_node("Controller_Node")
    controller_pub = rospy.Publisher("motor_pub", PyRobot.Controller_Node, queue_size=1)
    # prolog_sub = rospy.Subscriber("prolog_sub", PyRobot.Prolog_Node, callback_prolog)
    # switch_sub = rospy.Subscriber("switch_sub", PyRobot.Motor_Switch_Node, callback_switch)
    # sonar_sub, volt_sub = rospy.Subscriber("sonar_volt", PyRobot.Sonar_Volt_Node, callback_sonar_volt)
    # mv_camera = rospy.Subscriber("mv_camera", PyRobot.MV_Camera_Node, callback_mvcamera)
    lidar_compass_sub = rospy.Subscriber("sonar_volt", PyRobot.Lidar_Compass_Node, callback_lidar_compass)

    #pos_lidar, angle16, angle8, pitch, roll, mag, acc, gyro, temp = rospy.Subscriber("sonar_volt", PyRobot.Lidar_Compass_Node, callback_lidar_compass)

    r = rospy.Rate(1)

    while not rospy.is_shutdown():
        # controller_msg.velo = prolog_sub  # messaggio per il nodo Motor_Switch
        # controller_msg.switch = switch_sub  # messaggio per il nodo Prolog per switch
        # controller_msg.sonar = sonar_sub  # messaggio per il nodo Prolog per sonar
        # controller_msg.volt = volt_sub  # messaggio per il nodo Prolog per voltometro
        controller_msg.lidar = lidar_compass_sub.lidar_pos # messaggio per il nodo Prolog per lidar
        # compass
        controller_msg.angle16 = angle16  # messaggio per il nodo Prolog per angle16
        controller_msg.angle8 = angle8  # messaggio per il nodo Prolog per angle8
        controller_msg.pitch = pitch  # messaggio per il nodo Prolog per pitch
        controller_msg.roll = roll  # messaggio per il nodo Prolog per roll
        controller_msg.mag = mag  # messaggio per il nodo Prolog per mag
        controller_msg.acc = acc  # messaggio per il nodo Prolog per acc
        controller_msg.gyro = gyro  # messaggio per il nodo Prolog per gyro
        controller_msg.temp = temp  # messaggio per il nodo Prolog per temp

        # if mv_camera == 'trovato':
        #     controller_msg.qrcode = 1
        #
        # if prolog_sub == 'stop' and mv_camera == 'trovato':  # qrcode dal nodo MVCamera
        #     controller_msg.on_off_lidar = True
        #
        #     controller_pub.publish(controller_msg)
        #     r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
