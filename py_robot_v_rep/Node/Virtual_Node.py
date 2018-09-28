#! /usr/bin/python

from librerie import *
import numpy as np
import matplotlib.pyplot as mlp

clientID = None
oggetti = []
oggettires = []
nomioggetti = ['Proximity_sensorCE', 'Proximity_sensorDX', 'Proximity_sensorSX', 'LaserScannerLaser_2D', 'MV_Camera',
               'Pi_Camera', 'Motore_AD', 'Motore_AS', 'Motore_PD', 'Motore_PS', 'LaserScannerJoint_2D']
# global flagstate
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
        if i < 4:
            simxReadProximitySensor(connessione, mario, simx_opmode_streaming)
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
    return np.linalg.norm(coordinate)


def immagine(connessione, handle):
    ris, resolution, image = vrep.simxGetVisionSensorImage(connessione, handle, 0, vrep.simx_opmode_buffer)
    print(resolution)
    img = np.array(image, dtype=np.uint8)
    print (img)
    img.resize([resolution[0], resolution[1], 3])
    print ("adskjfbdksjabfkj")
    print (img)
    return img


clientID = connessione()
print(objectoggetti(clientID))
print (readproximity(clientID, oggetti[3]))

mlp.imshow(immagine(clientID, oggetti[4]), origin="lower")
