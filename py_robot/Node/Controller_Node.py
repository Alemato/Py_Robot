#! /usr/bin/python
import rospy
import roslaunch.rlutil
import roslaunch.parent
import roslaunch
import py_robot.msg as PyRobot
import time
import os

controller_msg = PyRobot.Controller_Node()
controller_to_motor_msg = PyRobot.Controller_To_Motor_Node()

angle16 = None
angle8 = None
pitch = None
roll = None
mag = [None for x in range(0, 6)]
acc = [None for x in range(0, 6)]
gyro = [None for x in range(0, 6)]
temp = None
comando = None
switch = [None for x in range(0, 3)]
sonar = [None for x in range(0, 3)]
volt = None
eureca = None
visione = None
launch = None
risposta_prolog = None


def resetvar():
    """
    Funzione che setta le variabili a nullo per evitare l'invio di messaggi non completi.
    Lavora sulle variabili globali angle16, angle8, pitch, roll, mag, acc, gyro,
    temp,  comando, switch, sonar, volt, eureca e visione
    :return: nulla
    """
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, switch, sonar, volt, eureca, visione, \
        comando, risposta_prolog

    angle16 = None
    angle8 = None
    pitch = None
    roll = None
    mag = [None for x in range(0, 6)]
    acc = [None for x in range(0, 6)]
    gyro = [None for x in range(0, 6)]
    temp = None
    comando = None
    switch = [None for x in range(0, 3)]
    sonar = [None for x in range(0, 3)]
    volt = None
    eureca = None
    visione = None
    risposta_prolog = None


def callback_prolog(msg):
    """
    funzione di callback per i messaggi provenienti dal nodo Prolog_IA,
    modifica la variabile globale comando
    :param msg: messagio ricevuto
    :return: nulla
    """
    global comando, risposta_prolog

    risposta_prolog = msg.risposta

    comando = ''
    risposta_prolog = msg.risposta
    if risposta_prolog == "dritto":
        comando = "e"
    elif risposta_prolog == "destra":
        comando = "r"
    elif risposta_prolog == "sinistra":
        comando = "q"
    elif risposta_prolog == "indietro":
        comando = "i"
    elif risposta_prolog == "stop":
        comando = "s"
    elif risposta_prolog == "correggi_a_destra":
        comando = "t"
    elif risposta_prolog == "correggi_a_sinistra":
        comando = "u"
    elif risposta_prolog == "fine":
        endfunction()
    else:
        comando = 's'


def startfunction():
    """
    Funzione di inizio programma. Si occupa di far partire i nodi
    :return: nulla
    """
    path = os.getcwd()
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, [
         path +"/catkin_ws/src/py_robot/launch/node_launcher.launch"])  # qui da aggiornare con il path del file launch
    launch.start()
    rospy.loginfo("started")


def endfunction():
    """
    Funzione di fine programma. Si occupa di far terminare il Nodo Controller
    :return: nulla
    """
    global comando
    launch.shutdown()
    time.sleep(1)
    rospy.signal_shutdown('Mission Complete')


def callback_switch(msg):
    """
    Funzione Callback che processa i dati inviati dai Nodo Motor_Switch
    :param msg: messaggio ROS dal Nodo Motor_Switch
    :return: nulla
    """
    global switch
    switch = msg.switches
    rospy.loginfo(switch)


def callback_sonar_volt(msg):
    """
    Funzione Callback che processa i dati inviati dai Nodo Sonar_Volt
    :param msg: messaggio ROS dal Nodo Sonar_Volt
    :return: nulla
    """
    global sonar, volt
    sonar = msg.sonar
    volt = msg.volt


def callback_compass(msg):
    """
    Funzione Callback che processa i dati inviati dai Nodo Compass
    :param msg: messaggio ROS dal Nodo Compass
    """
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp
    angle16 = msg.angle16
    angle8 = msg.angle8
    pitch = msg.pitch
    roll = msg.roll
    mag = msg.mag
    acc = msg.acc
    gyro = msg.gyro
    temp = msg.temp


def callback_mvcamera(msg):
    """
    Funzione Callback che processa i dati inviati dai Nodo MV_Camera
    :param msg: messaggio ROS dal Nodo MV_Camera
    :return: nulla
    """
    global eureca
    eureca = msg.eureca


def callback_pi_camera(msg):
    """
    Funzione Callback che processa i dati inviati dai Nodo PI_Camera
    :param msg: messaggio ROS dal Nodo PI_Camera
    :return: nulla
    """
    global visione
    visione = msg.visione


def ifNotNone(angle16, angle8, pitch, roll, mag, acc, gyro, temp, volt, sonar, visione, risposta_prolog, switch):
    """
    funzione di controlo delle variabili globali,
    controlla se sono state modificate tutte
    :param risposta_prolog:
    :param visione:
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
    :return: True se sono modificate, False se sono ancora None
    """

    return angle16 is not None and angle8 is not None and pitch is not None and roll is not None \
           and mag is not None and acc is not None and gyro is not None and temp is not None \
           and volt is not None and sonar is not None and visione is not None \
           and risposta_prolog is not None and not switch == [None, None, None]


def main():
    """
    Funzione principale che si occupa di inizializzare il Nodo, i Pubblisher e i Subscriber. Si occupa anche di salvare
    i valori ricevuti dai vari Nodi nei mesaggi Controller_Node.msg
    :return: nulla
    """
    global angle16, angle8, pitch, roll, mag, acc, gyro, temp, switch, sonar, volt, eureca, visione, \
        comando, risposta_prolog
    # inizializzazione nodo Controller
    rospy.init_node("Controller_Node", disable_signals=True)
    startfunction()
    # inizializzazioni Publisher e Subsciber
    controller_pub = rospy.Publisher("controller", PyRobot.Controller_Node, queue_size=1)
    controller_to_motor_pub = rospy.Publisher("controller_To_Motor", PyRobot.Controller_To_Motor_Node, queue_size=1)
    rospy.Subscriber("prolog", PyRobot.Prolog_IA_Node, callback_prolog)
    rospy.Subscriber("switches", PyRobot.Motor_Switch_Node, callback_switch)
    rospy.Subscriber("sonar_volt", PyRobot.Sonar_Volt_Node, callback_sonar_volt)
    rospy.Subscriber("mv_camera", PyRobot.MV_Camera_Node, callback_mvcamera)
    rospy.Subscriber("compass", PyRobot.Compass_Node, callback_compass)
    rospy.Subscriber("pi_camera", PyRobot.Pi_Camera_Node, callback_pi_camera)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        if ifNotNone(angle16, angle8, pitch, roll, mag, acc, gyro, temp, volt, sonar, visione, risposta_prolog, switch):
            controller_msg.angle16 = angle16  # messaggio per il nodo Prolog per angle16
            controller_msg.angle8 = angle8  # messaggio per il nodo Prolog per angle8
            controller_msg.pitch = pitch  # messaggio per il nodo Prolog per pitch
            controller_msg.roll = roll  # messaggio per il nodo Prolog per roll
            controller_msg.mag = mag  # messaggio per il nodo Prolog per mag
            controller_msg.acc = acc  # messaggio per il nodo Prolog per acc
            controller_msg.gyro = gyro  # messaggio per il nodo Prolog per gyro
            controller_msg.temp = temp  # messaggio per il nodo Prolog per temp
            controller_msg.switches = switch  # messaggio per il nodo Prolog per switch
            controller_msg.volt = volt  # messaggio per il nodo Prolog per volt
            controller_msg.sonar = sonar  # messaggio per il nodo Prolog per sonar
            controller_msg.visione = visione  # messaggio per il nodo Prolog per Py Camera

            if eureca == 'trovato':
                controller_msg.qrcode = 1  # messaggio per il nodo Prolog per qrcode

            if comando is not None:
                controller_to_motor_msg.velo = comando  # messaggio per il nodo Motor_Switch per Motor

            # funzioni Publish ROS
            controller_pub.publish(controller_msg)
            controller_to_motor_pub.publish(controller_to_motor_msg)

            resetvar()
            r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
