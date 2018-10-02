#! /usr/bin/python

from librerie import *
import numpy as np
import time
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
    nomioggetti = ['Lidar']
    res, objecthandle = simxGetObjectHandle(clientID, nomioggetti[0], simx_opmode_blocking)
    simxReadProximitySensor(clientID, objecthandle, simx_opmode_streaming)
    simxGetObjectOrientation(clientID, objecthandle, sim_handle_parent, simx_opmode_streaming)
    if not res == 0:
        print ("Creation Error")
        return
    else:
        print ("Creation " + nomioggetti[0])
        oggetto.append(objecthandle)
    return oggetto


def readproximity(clientID, handle):
    ris, stato, coordinate, handleoggettoris, vettorenormalizzato = simxReadProximitySensor(clientID, handle[0], simx_opmode_buffer)
    distanza =np.linalg.norm(coordinate)
    return distanza



def angololidar(clientID):
    returnCode, number = simxGetObjectOrientation(clientID, oggetti[3], sim_handle_parent, simx_opmode_buffer)
    number = [number[0] * 180 / np.pi, number[1] * 180 / np.pi, number[2] * 180 / np.pi]
    return number


def lidar(clientID, lidar, corangolo):
    angolo = angololidar(clientID)
    angoloeleur = [(angolo[0] + corangolo)/180*np.pi, (angolo[1])/180*np.pi, angolo[2]/180*np.pi]
    ris = simxSetObjectOrientation(clientID, lidar, sim_handle_parent, angoloeleur, simx_opmode_oneshot_wait)
    distanza = readproximity(clientID, lidar)
    angolo = angololidar(clientID)
    time.sleep(0.1)
    return distanza, angolo


def callback(msg, args):
    lidar_pub = args[0]
    r = args[1]
    clientID = args[2]
    while not rospy.is_shutdown():
        #lidar_pub.lidar =
        #lidar_pub.volt = readvolt(12)
        lidar_pub.publish(lidar_pub.sonar, lidar_pub.volt)
        r.sleep()


def main(oggetto = []):
    clientID = connessione()
    newoggetti = oggetti(clientID, oggetto)
    rospy.init_node("Lidar_Compass_Node")
    lidar_pub = rospy.Publisher("lidar_compass", PyRobot.Lidar_Compass_Node, queue_size=1)
    r = rospy.Rate(1)
    rospy.Subscriber("lidar_trigger", PyRobot.Controller_Node, callback, (lidar_pub, r, clientID))



if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass