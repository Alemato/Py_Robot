#! /usr/bin/python

from librerie import *
import numpy as np
import matplotlib.pyplot as mlp
import time

oggetti = []
oggettires = []
nomioggetti = ['Proximity_sensorCE', 'Proximity_sensorDX', 'Proximity_sensorSX', 'Lidar', 'MV_Camera',
               'Pi_Camera', 'Motore_AD', 'Motore_AS', 'Motore_PD', 'Motore_PS', 'Rover_Py_Robot']
flagstate = True


def connessione():
    """
    funzione per connessione
    :return: clientID
    """
    print('Program started')
    simxFinish(-1)  # just in case, close all opened connections
    clientID = simxStart('127.0.0.1', 19998, True, True, 5000, 5)  # Connect to V-REP
    if clientID == -1:
        print("Failed to connect to Remote API Server")
    else:
        print('Connected to Remote API Server')
        return clientID


def objectoggetti(connessione):
    for i in range(0, 11):
        res, mario = simxGetObjectHandle(connessione, nomioggetti[i], simx_opmode_blocking)
        if i < 3:
            simxReadProximitySensor(connessione, mario, simx_opmode_streaming)
        elif i < 4:
            simxReadProximitySensor(connessione, mario, simx_opmode_streaming)
            simxGetObjectOrientation(connessione, mario, sim_handle_parent, simx_opmode_streaming)
        elif i < 6:
            simxGetVisionSensorImage(connessione, mario, 0, simx_opmode_streaming)
        if not res == 0:
            print ("Creation Error")
            return
        else:
            print ("Creation " + nomioggetti[i])
            oggetti.append(mario)
    return oggetti


def readproximity(connessione, handle):
    ris, stato, coordinate, handleoggettoris, vettorenormalizzato = simxReadProximitySensor(connessione, handle,
                                                                                            simx_opmode_buffer)
    print ris
    return np.linalg.norm(coordinate)


def immagine(connessione, handle):
    ris, resolution, image = vrep.simxGetVisionSensorImage(connessione, handle, 0, vrep.simx_opmode_buffer)
    img = np.array(image, dtype=np.uint8)
    img.resize([resolution[1], resolution[0], 3])
    return img


def creahandle(conessione, nomioggetti):
    res, mario = simxGetObjectHandle(connessione, nomioggetti, simx_opmode_blocking)
    return mario


def angololidar(connessione):
    returnCode, number = simxGetObjectOrientation(connessione, oggetti[3], sim_handle_parent, simx_opmode_buffer)
    print number
    number = [number[0] * 180 / np.pi, number[1] * 180 / np.pi, number[2] * 180 / np.pi]
    print number
    return number


def lidar(connessione, lidar, corangolo):
    angolo = angololidar(connessione)
    newangolo = [(angolo[0]+ corangolo)/180*np.pi, (angolo[1])/180*np.pi, angolo[2]/180*np.pi]
    print newangolo
    ris = simxSetObjectOrientation(connessione, lidar, sim_handle_parent, newangolo, simx_opmode_oneshot_wait)
    print ris
    angolo = readproximity(connessione, lidar)
    time.sleep(0.1)
    return angolo


clientID = connessione()
print(objectoggetti(clientID))
print (readproximity(clientID, oggetti[3]))
for i in range(0, 89):
    print (lidar(clientID, oggetti[3], +1.0))
for i in range(0, 179):
    print (lidar(clientID, oggetti[3], -1.0))