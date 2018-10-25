#! /usr/bin/python

from librerie import *
import numpy as np
import py_robot_v_rep.msg as PyRobot
import time
import rospy


switch_msg = PyRobot.Motor_Switch_Node()
clientID = None
oggetto = []
micros = []
motors = []
stati = []


def connessione():
    """
    funzione per connessione
    :return: clientID
    """
    print('Program started')
    simxFinish(-1)  # just in case, close all opened connections
    clientID = simxStart('127.0.0.1', 20000, True, True, 5000, 5)  # Connect to V-REP
    if clientID == -1:
        print("Failed to connect to Remote API Server at Port 20000")
    else:
        print('Connected to Remote API Server at Port 20000')
        return clientID


def oggetti(clientID):
    """
    funzione che crea gli oggetti nel modo v-rep
    :var globale oggetto: rappresenta gli oggetti creati, e' di tipo lista
    :param clientID: connesione v-rep
    :return: oggetto
    """
    global oggetto
    nomioggetti = ['Micro_SX', 'Micro_DX', 'Micro_CE', 'Motore_AD', 'Motore_AS', 'Motore_PD', 'Motore_PS']
    for i in range(0, 7):
        res, objecthandle = simxGetObjectHandle(clientID, nomioggetti[i], simx_opmode_blocking)
        if i < 4:
            simxReadProximitySensor(clientID, objecthandle, simx_opmode_streaming)
        if not res == 0:
            print ("Creation Error")
            return
        else:
            print ("Creation " + nomioggetti[i])
            oggetto.append(objecthandle)
    return oggetto


def forward(clientID, motors, velocita):
    """
    funzione che setta i motori per andare avanti
    :param clientID: connesione v-rep
    :param motors: lista degli oggetti motori del mondo v-rep
    :param velocita: velocita' da settare ai motori
    :return: nulla
    """
    ris1 = simxSetJointTargetVelocity(clientID, motors[3], velocita, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], velocita, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], velocita, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[0], velocita, simx_opmode_oneshot_wait)
    if ris1 > 0 or ris2 > 0 or ris3 > 0 or ris4 > 0:
        print ("Error forward")


def backward(clientID, motors, velocita):
    """
    funzione che setta i motori per andare indietro
    :param clientID: connesione v-rep
    :param motors: lista degli oggetti motori del mondo v-rep
    :param velocita: velocita' da settare ai motori
    :return: nulla
    """
    ris1 = simxSetJointTargetVelocity(clientID, motors[3], -velocita, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], -velocita, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], -velocita, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[0], -velocita, simx_opmode_oneshot_wait)
    if ris1 > 0 or ris2 > 0 or ris3 > 0 or ris4 > 0:
        print ("Error backward")


def left(clientID, motors):
    """
    funzione che setta i motori per andare a sinistra
    :param clientID: connesione v-rep
    :param motors: lista degli oggetti motori del mondo v-rep
    :return: nulla
    """
    ris1 = simxSetJointTargetVelocity(clientID, motors[0], +2, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], -2, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], +2, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[3], -2, simx_opmode_oneshot_wait)
    if ris1 > 0 or ris2 > 0 or ris3 > 0 or ris4 > 0:
        print ("Error left")

def left_correction(clientID, motors):
    """
    funzione che setta i motori per eseguire una correzione a sinistra
    :param clientID: connesione v-rep
    :param motors: lista degli oggetti motori del mondo v-rep
    :return: nulla
    """
    ris1 = simxSetJointTargetVelocity(clientID, motors[0], +2, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], -2, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], +2, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[3], -2, simx_opmode_oneshot_wait)
    if ris1 > 0 or ris2 > 0 or ris3 > 0 or ris4 > 0:
        print ("Error left_correction")


def right(clientID, motors):
    """
    funzione che setta i motori per andare a destra
    :param clientID: connesione v-rep
    :param motors: lista degli oggetti motori del mondo v-rep
    :return: nulla
    """
    ris1 = simxSetJointTargetVelocity(clientID, motors[0], -2, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], +2, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], -2, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[3], +2, simx_opmode_oneshot_wait)
    if ris1 > 0 or ris2 > 0 or ris3 > 0 or ris4 > 0:
        print ("Error right")

def right_correction(clientID, motors):
    """
    funzione che setta i motori per eseguire una correzione a destra
    :param clientID: connesione v-rep
    :param motors: lista degli oggetti motori del mondo v-rep
    :return: nulla
    """
    ris1 = simxSetJointTargetVelocity(clientID, motors[0], -2, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], +2, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], -2, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[3], +2, simx_opmode_oneshot_wait)
    if ris1 > 0 or ris2 > 0 or ris3 > 0 or ris4 > 0:
        print ("Error right_correction")

def micro(clientID):
    """
    funzione che rileva lo stato dei microswitch nel modo r-rep
    :param clientID: connesione v-rep
    :return stati: ritorna gli stati dei microswitch e' di tipo lista
    """
    global micros, stati
    for Micro in micros:
        ris, stato, coordinate, handleoggettoris, vettorenormalizzato = simxReadProximitySensor(clientID, Micro, simx_opmode_buffer)
        stati.append(stato)
    return stati


def callback(msg):
    """
    funzione che esegue i comandi che arrivano dal controller_node
    :param msg: messaggio ros ricevuto
    :return: nulla
    """
    global clientID, motors
    print msg.velo
    if msg.velo == "a":
        forward(clientID, motors, 1)
    elif msg.velo == "b":
        forward(clientID, motors, 1.5)
    elif msg.velo == "c":
        forward(clientID, motors, 2)
    elif msg.velo == "d":
        forward(clientID, motors, 2.5)

    # dritto
    elif msg.velo == "e":
        forward(clientID, motors, 3)

    elif msg.velo == "f":
        forward(clientID, motors, 3.5)
    elif msg.velo == "g":
        forward(clientID, motors, 4)
    elif msg.velo == "h":
        forward(clientID, motors, 5)

    # indietro
    elif msg.velo == "i":
        backward(clientID, motors, 1)

    elif msg.velo == "l":
        backward(clientID, motors, 1.5)
    elif msg.velo == "m":
        backward(clientID, motors, 2)
    elif msg.velo == "n":
        backward(clientID, motors, 2.5)
    elif msg.velo == "o":
        backward(clientID, motors, 3)
    elif msg.velo == "p":
        left(clientID, motors)
        time.sleep(2)
        forward(clientID, motors, 0)

    # sinistra
    elif msg.velo == "q":
        left(clientID, motors)
        time.sleep(2)
        forward(clientID, motors, 0)

    # destra
    elif msg.velo == "r":
        right(clientID, motors)
        time.sleep(2)
        forward(clientID, motors, 0)

    # stop
    elif msg.velo == "s":
        forward(clientID, motors, 0)

    # correggi a destra
    elif msg.velo == "t":
        left_correction(clientID, motors)

    # correggi a sinistra
    elif msg.velo == "u":
        right_correction(clientID, motors)

    # attiva lidar
    elif msg.velo == "v":
        forward(clientID, motors, 0)

    else:
        forward(clientID, motors, 0)


def main():
    global clientID, oggetto, micros, motors, stati
    clientID = connessione()
    newoggetti = oggetti(clientID)
    micros = [newoggetti[0], newoggetti[1], newoggetti[2]]
    motors = [newoggetti[3], newoggetti[4], newoggetti[5], newoggetti[6]]
    rospy.init_node("Motor_Switch_Node")
    rospy.Subscriber("controller_To_Motor", PyRobot.Controller_To_Motor_Node, callback)
    switch_pub = rospy.Publisher("switches", PyRobot.Motor_Switch_Node, queue_size=1)
    r = rospy.Rate(1)

    while not rospy.is_shutdown():
        microswitch = micro(clientID)
        if microswitch[0] or microswitch[1] or microswitch[2]:
            forward(clientID, motors, 0)
        switch_msg.switches = microswitch
        switch_pub.publish(switch_msg)
        rospy.loginfo(switch_msg)
        stati = []
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass