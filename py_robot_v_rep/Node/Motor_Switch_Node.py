#! /usr/bin/python

from librerie import *
import numpy as np
import py_robot_v_rep.msg as PyRobot
import time
import rospy


switch_pub = PyRobot.Motor_Switch_Node()

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


def oggetti(clientID, oggetto):
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
    ris1 = simxSetJointTargetVelocity(clientID, motors[3], velocita, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], velocita, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], velocita, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[0], velocita, simx_opmode_oneshot_wait)
    return ris1, ris2, ris3, ris4


def backward(clientID, motors, velocita):
    ris1 = simxSetJointTargetVelocity(clientID, motors[3], -velocita, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], -velocita, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], -velocita, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[0], -velocita, simx_opmode_oneshot_wait)
    return ris1, ris2, ris3, ris4


def left(clientID, motors):
    ris1 = simxSetJointTargetVelocity(clientID, motors[0], +2, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], -2, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], +2, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[3], -2, simx_opmode_oneshot_wait)
    return ris1, ris2, ris3, ris4


def right(clientID, motors):
    ris1 = simxSetJointTargetVelocity(clientID, motors[0], -2, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(clientID, motors[1], +2, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(clientID, motors[2], -2, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(clientID, motors[3], +2, simx_opmode_oneshot_wait)
    return ris1, ris2, ris3, ris4


def micro(clientID, micros):
    stati = []
    for Micro in micros:
        ris, stato, coordinate, handleoggettoris, vettorenormalizzato = simxReadProximitySensor(clientID, Micro, simx_opmode_buffer)
        stati.append(stato)
    return stati


def callback(msg, args):
    clientID = args[0]
    motors = args[1]
    if msg.vel == "a":
        forward(clientID, motors, 1)
    elif msg.vel =="b":
        forward(clientID, motors, 1.5)
    elif msg.vel =="c":
        forward(clientID, motors, 2)
    elif msg.vel == "d":
        forward(clientID, motors, 2.5)
    elif msg.vel == "e":
        forward(clientID, motors, 3)
    elif msg.vel == "f":
        forward(clientID, motors, 3.5)
    elif msg.vel == "g":
        forward(clientID, motors, 4)
    elif msg.vel == "h":
        forward(clientID, motors, 5)
    elif msg.vel == "i":
        backward(clientID, motors, 1)
    elif msg.vel == "l":
        backward(clientID, motors, 1.5)
    elif msg.vel == "m":
        backward(clientID, motors, 2)
    elif msg.vel == "n":
        backward(clientID, motors, 2.5)
    elif msg.vel == "o":
        backward(clientID, motors, 3)
    elif msg.vel == "p":
        left(clientID, motors)
        time.sleep(2)
    elif msg.vel == "q":
        right(clientID, motors)
        time.sleep(2)
    elif msg.vel == "r":
        backward(clientID, motors, 4)
    elif msg.vel == "s":
        forward(clientID, motors, 0)


def main(oggetto=[]):
    clientID = connessione()
    newoggetti = oggetti(clientID, oggetto)
    micros = [newoggetti[0], newoggetti[1], newoggetti[2]]
    motors = [newoggetti[3], newoggetti[4], newoggetti[5], newoggetti[6]]
    rospy.init_node("Motor_Switch_Node")
    rospy.Subscriber("motor", PyRobot.Controller_Node, callback, (clientID, motors))
    switch_pub = rospy.Publisher("switch", PyRobot.Motor_Switch_Node, queue_size=1)
    r = rospy.Rate(1)

    while not rospy.is_shutdown():
        switch_pub.switch = micro(clientID, micros)
        switch_pub.publish(switch_pub.switch)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass