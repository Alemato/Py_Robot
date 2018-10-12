#! /usr/bin/python

import rospy
import numpy
import py_robot.msg as PyRobot

controller_msg = PyRobot.Controller_Node()

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
switch = [None for x in range(0, 3)]
sonar = [None for x in range(0, 3)]
volt = None
eureca = None
visione = None

def resetvar():
    """
    funzione per il reset delle variabili
    :return:
    """
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar18, comando, switch, sonar, volt, eureca, visione

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
    switch = [None for x in range(0, 3)]
    sonar = [None for x in range(0, 3)]
    volt = None
    eureca = None
    visione = None


def callback_prolog(msg):
    """
    funzione di callback per i messaggi provenienti dal nodo Prolog_IA,
    modifica la variabile globale comando
    :param msg: messagio ricevuto
    :return: nulla
    """
    global comando
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
        endfunction()


def endfunction():
    """
    funzione per la fine e il blocco della simulazione
    :return: nulla
    """
    global comando
    comando = 'stop'                             # da rivedere
    rospy.signal_shutdown('Mission Complete')


def callback_switch(msg):
    """
    funzione di callback per i messaggi provenienti dal nodo Motor_Switch_Node
    :param msg: messagio ricevuto
    :return: nulla
    """
    global switch
    switch = msg.switch


def callback_sonar_volt(msg):
    """
    funzione di callback per i messaggi provenienti dal nodo Sonar_Volt_Node
    :param msg: messagio ricevuto
    :return:
    """
    global sonar, volt
    sonar = msg.sonar
    volt = msg.volt


def callback_lidar_compass(msg):
    """
    funzione di callback per i messaggi provenienti dal nodo Lidar_Compass_Node
    :param msg: messagio ricevuto
    :return:
    """
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar18
    lidar = msg.lidar
    lidar18 = dividilista(lidar)
    angle16 = msg.angle16
    angle8 = msg.angle8
    pitch = msg.pitch
    roll = msg.roll
    mag = msg.mag
    acc = msg.acc
    gyro = msg.gyro
    temp = msg.temp


def dividilista(lista):
    """
    funzione che divide in array da 10 elementi e fa la media delle 180 misure del lidar,
    :param lista: lista delle 181 misure del lidar
    :return listamedia: lista delle 19 misure medie (prese ogni 10 gradi)
    """
    listadivisa = numpy.split(lista, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170])
    listamedia = numpy.mean(listadivisa, axis=1, dtype=numpy.float64)
    listamedia = listamedia.tolist()
    return listamedia


def callback_mvcamera(msg):
    """
    funzione di callback per i messaggi provenienti dal nodo MV_Camera_Node
    :param msg: messagio ricevuto
    :return: nulla
    """
    global eureca
    eureca = msg.eureca


def callback_pi_camera(msg):
    """
    funzione di callback per i messaggi provenienti dal nodo Pi_Camer_Node
    :param msg: messagio ricevuto
    :return: nulla
    """
    global visione
    visione = msg.visione


def ifNotNone(angle16, angle8, pitch, roll, mag, acc, gyro, temp, comando, volt, sonar):
    """
    funzione di controlo delle variabili globali,
    controlla se sono state modificate tutte
    :param angle16: misura del angolo a 16
    :param angle8: misura del angolo a 8
    :param pitch: misura del pitch
    :param roll: misura del roll
    :param mag: misura del mag
    :param acc: misura del acc
    :param gyro: misura del gyro
    :param temp: misura della temperatura
    :param comando: variabile del comando da inviare
    :param volt: misura della batteria
    :param sonar: misura dei sonar
    :return: True se sono modificate, False se sono ancora nulle
    """
    return angle16 is not None and angle8 is not None and pitch is not None and roll is not None and mag is not None and acc is not None and gyro is not None and temp is not None and comando is not None and volt is not None and sonar is not None


def main():
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar18, comando, switch, sonar, volt, eureca, visione
    resetvar()
    # inizializzazione nodo Controller
    rospy.init_node("Controller_Node", disable_signals=True)
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
            controller_msg.visione = visione  # messaggio per il nodo Prolog per Py Camera

            if eureca == 'trovato':
                controller_msg.qrcode = 1  # messaggio per il nodo Prolog per qrcode

            if comando == 'stop':  # qrcode dal nodo MVCamera
                controller_msg.on_off_lidar = True

            controller_pub.publish(controller_msg)
            rospy.loginfo(controller_msg)
            r.sleep()
            resetvar()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass