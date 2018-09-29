#! /usr/bin/python

from librerie import *
import numpy as np
import rospy
import py_robot_v_rep.msg as PyRobot

def connessione():
    """
    funzione per connessione
    :return: clientID
    """
    print('Program started')
    simxFinish(-1)  # just in case, close all opened connections
    clientID = simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to V-REP
    if clientID == -1:
        print("Failed to connect to Remote API Server")
    else:
        print('Connected to Remote API Server')
        return clientID


def oggetti(clientID, oggetto):
    nomioggetti = ['Proximity_sensorCE', 'Proximity_sensorDX', 'Proximity_sensorSX']
    for i in range(0, 4):
        res, objecthandle = simxGetObjectHandle(clientID, nomioggetti[i], simx_opmode_blocking)
        simxReadProximitySensor(clientID, objecthandle, simx_opmode_streaming)
        if not res == 0:
            print ("Creation Error")
            return
        else:
            print ("Creation " + nomioggetti[i])
            oggetto.append(objecthandle)
    return oggetto


def readproximity(clientID, handle):
    distanza = []
    ris, stato, coordinate, handleoggettoris, vettorenormalizzato = simxReadProximitySensor(clientID, handle[0], simx_opmode_buffer)
    distanza.append(np.linalg.norm(coordinate))
    ris, stato, coordinate, handleoggettoris, vettorenormalizzato = simxReadProximitySensor(clientID, handle[1],
                                                                                            simx_opmode_buffer)
    distanza.append(np.linalg.norm(coordinate))
    ris, stato, coordinate, handleoggettoris, vettorenormalizzato = simxReadProximitySensor(clientID, handle[2],
                                                                                            simx_opmode_buffer)
    distanza.append(np.linalg.norm(coordinate))
    return distanza


def readvolt(volt):
    return volt


def main(oggetto=[]):
    clientID = connessione()
    newoggetti = oggetti(clientID, oggetto)
    rospy.init_node("Sonar_Volt_Node")
    switch_pub = rospy.Publisher("sonar_volt", PyRobot.Sonar_Volt_Node, queue_size=1)
    r = rospy.Rate(1)

    while not rospy.is_shutdown():
        switch_pub.sonar = readproximity(clientID, newoggetti)
        switch_pub.volt = readvolt(12)
        switch_pub.publish(switch_pub.sonar, switch_pub.volt)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass