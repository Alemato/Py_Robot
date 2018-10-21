#! /usr/bin/python

import rospy
import py_robot.msg as PyRobot

controller_msg = PyRobot.Controller_Node()
controller_to_lidar_msg = PyRobot.Controller_To_Lidar_Node()

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
    '''
    Funzione che setta le variabili a nullo per evitare l'invio di messaggi non completi.
    Lavora sulle variabili globali angle16, angle8, pitch, roll, mag, acc, gyro,
    temp, lidar18, comando, switch, sonar, volt, eureca e visione
    '''
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
    '''
    Funzione Callback che processa i dati inviati dai Nodo IA_Prolog
    :param msg: messaggio ROS dal Nodo IA_Prolog
    '''
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
    elif risposta_prolog == 'attiva_lidar':
        comando = ""
    elif risposta_prolog == 'fine':
        endfunction()


def endfunction():
    '''
    Funzione di fine programma. Si occupa di far terminare il Nodo Controller
    '''
    global comando
    # comando = 'stop'                             # da rivedere
    rospy.signal_shutdown('Mission Complete')


def callback_switch(msg):
    '''
    Funzione Callback che processa i dati inviati dai Nodo Motor_Switch
    :param msg: messaggio ROS dal Nodo Motor_Switch
    '''
    global switch
    switch = msg.switches


def callback_sonar_volt(msg):
    '''
    Funzione Callback che processa i dati inviati dai Nodo Sonar_Volt
    :param msg: messaggio ROS dal Nodo Sonar_Volt
    '''
    global sonar, volt
    sonar = msg.sonar
    volt = msg.volt


def callback_lidar_compass(msg):
    '''
    Funzione Callback che processa i dati inviati dai Nodo Lidar_Compass
    :param msg: messaggio ROS dal Nodo Lidar_Compass
    '''
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar18
    lidar18 = msg.lidar
    angle16 = msg.angle16
    angle8 = msg.angle8
    pitch = msg.pitch
    roll = msg.roll
    mag = msg.mag
    acc = msg.acc
    gyro = msg.gyro
    temp = msg.temp


def callback_mvcamera(msg):
    '''
    Funzione Callback che processa i dati inviati dai Nodo MV_Camera
    :param msg: messaggio ROS dal Nodo MV_Camera
    '''
    global eureca
    eureca = msg.eureca


def callback_pi_camera(msg):
    '''
    Funzione Callback che processa i dati inviati dai Nodo PI_Camera
    :param msg: messaggio ROS dal Nodo PI_Camera
    '''
    global visione
    visione = msg.visione


def ifNotNone(angle16, angle8, pitch, roll, mag, acc, gyro, temp, comando, volt, sonar, visione):
    '''
    Funzione che controlla se tutte le variabili non sono nulle per poterle includere nel messaggio

    :param angle16, angle8, pitch, roll, mag, acc, gyro, temp, comando, volt, sonar, visione: variabili globali
    :return angle16, angle8, pitch, roll, mag, acc, gyro, temp, comando, volt, sonar, visione: variabili globali se non nulle
    '''
    return angle16 is not None and angle8 is not None and pitch is not None and roll is not None and mag is not None and acc is not None and gyro is not None and temp is not None and comando is not None and volt is not None and sonar is not None and visione is not None


def main():
    '''
    Funzione principale che si occupa di inizializzare il Nodo, i Pubblisher e i Subscriber. Si occupa anche di salvare
    i valori ricevuti dai vari Nodi nei mesaggi Controller_Node.msg e Controller_To_Lidar.msg.
    '''
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, lidar18, comando, switch, sonar, volt, eureca, visione
    resetvar()
    # inizializzazione nodo Controller
    rospy.init_node("Controller_Node", disable_signals=True)
    # inizializzazioni Publisher e Subsciber
    controller_pub = rospy.Publisher("controller", PyRobot.Controller_Node, queue_size=1)
    controller_to_lidar_pub = rospy.Publisher("controller_To_Lidar", PyRobot.Controller_To_Lidar_Node, queue_size=1)
    rospy.Subscriber("prolog_ia", PyRobot.Prolog_IA_Node, callback_prolog)
    rospy.Subscriber("switch", PyRobot.Motor_Switch_Node, callback_switch)
    rospy.Subscriber("sonar_volt", PyRobot.Sonar_Volt_Node, callback_sonar_volt)
    rospy.Subscriber("mv_camera", PyRobot.MV_Camera_Node, callback_mvcamera)
    rospy.Subscriber("lidar_compass", PyRobot.Lidar_Compass_Node, callback_lidar_compass)
    rospy.Subscriber("pi_camera", PyRobot.Pi_Camera_Node, callback_pi_camera)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        if ifNotNone(angle16, angle8, pitch, roll, mag, acc, gyro, temp, comando, volt, sonar, visione):
            controller_msg.lidar = lidar18  # messaggio per il nodo Prolog per distanze lidar
            controller_msg.angle16 = angle16  # messaggio per il nodo Prolog per angle16
            controller_msg.angle8 = angle8  # messaggio per il nodo Prolog per angle8
            controller_msg.pitch = pitch  # messaggio per il nodo Prolog per pitch
            controller_msg.roll = roll  # messaggio per il nodo Prolog per roll
            controller_msg.mag = mag  # messaggio per il nodo Prolog per mag
            controller_msg.acc = acc  # messaggio per il nodo Prolog per acc
            controller_msg.gyro = gyro  # messaggio per il nodo Prolog per gyro
            controller_msg.temp = temp  # messaggio per il nodo Prolog per temp
            controller_msg.switches = switch  # messaggio per il nodo Prolog per switch
            controller_msg.velo = comando  # messaggio per il nodo Motor_Switch per Motor
            controller_msg.volt = volt  # messaggio per il nodo Prolog per volt
            controller_msg.sonar = sonar  # messaggio per il nodo Prolog per sonar
            controller_msg.visione = visione  # messaggio per il nodo Prolog per Py Camera

            if eureca == 'trovato':
                controller_msg.qrcode = 1  # messaggio per il nodo Prolog per qrcode

            if comando == 'stop':  # messaggio per il Nodo  Compass_Servo_Lidar
                controller_to_lidar_msg.on_off_lidar = True

            # funzioni Publish ROS
            controller_pub.publish(controller_msg)
            controller_to_lidar_pub.publish(controller_to_lidar_msg)
            resetvar()
            r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
