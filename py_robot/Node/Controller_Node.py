#! /usr/bin/python

import rospy
import numpy
import py_robot.msg as PyRobot

controller_msg = PyRobot.Controller_Node()
global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar18, comando, switch, sonar, volt, eureca, qrcode, on_of_lidar, visione

angle16 = None
angle8 = None
pitch = None
roll = None
mag = [None for x in range(0, 6)]
acc = [None for x in range(0, 6)]
gyro = [None for x in range(0, 6)]
temp = None
lidar18 = [None for x in range(0, 180)]
comando = None
switch = [0 for x in range(0, 3)]
sonar = [None for x in range(0, 3)]
volt = None
eureca = None
qrcode = 0
on_of_lidar = False
visione = None


def callback_prolog(msg):
    global comando
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
    elif risposta_prolog == 'correzione_destra':  # da rivedere e aggiungere gli altri comandi
        comando = ""
    elif risposta_prolog == 'correzione_destra':
        comando = ""
    elif risposta_prolog == 'fine':
        comando = ""


def callback_switch(msg):
    global switch
    switch = msg.switch


def callback_sonar_volt(msg):
    global sonar, volt
    sonar = msg.sonar
    volt = msg.volt


def callback_lidar_compass(msg):
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar18
    lidar = msg.lidar
    lidar18 = dividilista(lidar, 18)
    angle16 = msg.angle16
    angle8 = msg.angle8
    pitch = msg.pitch
    roll = msg.roll
    mag = msg.mag
    acc = msg.acc
    gyro = msg.gyro
    temp = msg.temp


def dividilista(lista, num):
    meta = len(lista) / float(num)
    listadivisa = []
    ultimo = 0.0
    while ultimo < len(lista):
        listadivisa.append(lista[int(ultimo):int(ultimo + meta)])
        ultimo += meta
    listamedia = []
    for x in range(0, 18):
        listamedia.append(numpy.mean(listadivisa[x]))
    return listamedia


def callback_mvcamera(msg):
    global eureca
    eureca = msg.eureca


def callback_pi_camera(msg):
    global visione
    visione = msg.visione


def ifNotNone( angle16, angle8, pitch, roll, mag, acc, gyro, temp, comando, volt, sonar):
    return angle16 is not None and angle8 is not None and pitch is not None and roll is not None and mag is not None and acc is not None and gyro is not None and temp is not None and comando is not None and volt is not None and sonar is not None


def main():
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar18, comando, switch, sonar, volt, eureca, qrcode, on_of_lidar, visione
    # inizializzazione nodo Controller
    rospy.init_node("Controller_Node")
    # inizializzazioni Publisher e Subsciber
    controller_pub = rospy.Publisher("controller_pub", PyRobot.Controller_Node, queue_size=1)
    rospy.Subscriber("prolog_sub", PyRobot.Prolog_Node, callback_prolog)
    rospy.Subscriber("switch_sub", PyRobot.Motor_Switch_Node, callback_switch)
    rospy.Subscriber("sonar_volt_sub", PyRobot.Sonar_Volt_Node, callback_sonar_volt)
    rospy.Subscriber("mv_camera_sub", PyRobot.MV_Camera_Node, callback_mvcamera)
    rospy.Subscriber("lidar_compass_sub", PyRobot.Lidar_Compass_Node, callback_lidar_compass)
    rospy.Subscriber("pi_camera_sub", PyRobot.Pi_Camera_Node, callback_pi_camera)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        if ifNotNone(angle16, angle8, pitch, roll, mag, acc, gyro, temp, comando, volt, sonar):
            controller_msg.lidar = lidar18  # messaggio per il nodo Prolog per distanze lidar
            controller_msg.angle16 = angle16  # messaggio per il nodo Prolog per angle16
            controller_msg.angle8 = angle8  # messaggio per il nodo Prolog per angle8
            controller_msg.pitch = pitch  # messaggio per il nodo Prolog per pitch
            controller_msg.roll = roll  # messaggio per il nodo Prolog per roll
            controller_msg.mag = mag  # messaggio per il nodo Prolog per mag
            controller_msg.acc = acc  # messaggio per il nodo Prolog per acc
            controller_msg.gyro = gyro  # messaggio per il nodo Prolog per gyro
            controller_msg.temp = temp  # messaggio per il nodo Prolog per temp
            controller_msg.switch = switch  # messaggio per il nodo Prolog per switch
            controller_msg.velo = comando  # messaggio per il nodo Motor_Switch per Motor
            controller_msg.volt = volt  # messaggio per il nodo Prolog per volt
            controller_msg.sonar = sonar  # messaggio per il nodo Prolog per sonar
            controller_msg.on_off_lidar = on_of_lidar  # messaggio per il nodo Lidar_compass per Lidar  1 = parti
            controller_msg.visione = visione  # messaggio per il nodo Prolog per Py Camera

            if eureca == 'trovato':
                controller_msg.qrcode = 1           # messaggio per il nodo Prolog per qrcode

            if comando == 'stop':                   # qrcode dal nodo MVCamera
                controller_msg.on_off_lidar = True

            controller_pub.publish(controller_msg)
            rospy.loginfo(controller_msg)
            r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
