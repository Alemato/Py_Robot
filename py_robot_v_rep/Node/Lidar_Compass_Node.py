#! /usr/bin/python

from librerie import *
import numpy as np
import time
import rospy
import py_robot_v_rep.msg as PyRobot

oggetto = []
lidar_compass = PyRobot.Lidar_Compass_Node()
lidarvar = None
clientID = None
handle = None


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


def oggetti(clientID):
    """
    funzione che crea l'oggetto lidar nel modo v-rep
    :var globale oggetto: rappresenta l'oggetto lidar, e' di tipo lista
    :param clientID: connesione v-rep
    :return:
    """
    global oggetto
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
    """
    funzione che ritorna una lettura, la lettura in questo caso  e' del lidar
    :param clientID: connessione v-rep
    :param handle: oggetto dal quale provine la lettura
    :return ditsanza: distanza letta
    """
    ris, stato, coordinate, handleoggettoris, vettorenormalizzato = simxReadProximitySensor(clientID, handle,
                                                                                            simx_opmode_buffer)
    if ris > 0:
        print ("Error read proximity")
    distanza = np.linalg.norm(coordinate)
    return distanza


def angololidar(clientID, handle):
    """
    funzione che ci dice l' orientamento del oggetto passato rispetto al padre nel mondo v-rep,
    in quessto caso  e' l'orientamento del lidar rispetto il padre (corpo del rover)
    :param clientID: connessione v-rep
    :param handle: oggetto a qui misurare l' orientamento rispetto al padre
    :return number: lista che contiene la rotazione rispetto ai 3 assi (misura in gradi deg)
    """
    returnCode, number = simxGetObjectOrientation(clientID, handle, sim_handle_parent, simx_opmode_buffer)
    if returnCode > 0:
        print ("Error angololidar orientation")
    number = [number[0] * 180 / np.pi, number[1] * 180 / np.pi, number[2] * 180 / np.pi]
    return number


def lidar(clientID, lidar, corangolo):
    """
    funzione che esegue la lettura e lo spostamento del lidar
    :param clientID: connesione v-rep
    :param lidar: oggetto lidar
    :param corangolo: angolo di spostamento/correzione del lidar per la prossima posizione
    :return: distanza misuarata dal lidar
    """
    angolo = angololidar(clientID)
    angoloeleur = [(angolo[0] + corangolo) / 180 * np.pi, (angolo[1]) / 180 * np.pi, angolo[2] / 180 * np.pi]
    ris = simxSetObjectOrientation(clientID, lidar, sim_handle_parent, angoloeleur, simx_opmode_oneshot_wait)
    if ris > 0:
        print ("Error lidar orientation")
    distanza = readproximity(clientID, lidar)
    time.sleep(0.1)
    return distanza


def callback(msg):
    """
    funzione chiamata dalla sottoscrizione del nodo di controllo, effettua le letture
    :param msg: messaggio ros ricevuto
    :return: nulla
    """
    global lidarvar, clientID, handle
    lidarvar[0] = lidar(clientID, handle, +89)
    for i in range(0, 179):
        lidarvar[i + 1] = lidar(clientID, handle, -1.0)


def main():
    global oggetto, clientID, handle, lidarvar
    clientID = connessione()
    handle = oggetti(clientID)
    rospy.init_node("Lidar_Compass_Node")
    rospy.Subscriber("lidar_trigger", PyRobot.Controller_Node, callback)
    lidar_pub = rospy.Publisher("lidar_compass", PyRobot.Lidar_Compass_Node, queue_size=1)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        lidar_compass.lidar = lidarvar
        lidar_compass.angle16 = 0
        lidar_compass.angle8 = 0
        lidar_compass.pitch = 0
        lidar_compass.roll = 0
        lidar_compass.mag = [0, 0, 0, 0, 0, 0]
        lidar_compass.acc = [0, 0, 0, 0, 0, 0]
        lidar_compass.gyro = [0, 0, 0, 0, 0, 0]
        lidar_compass.temp = 24
        lidar_pub.publish(lidar_compass)
        rospy.loginfo(lidar_compass)
        lidarvar = []
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
