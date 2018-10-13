#! /usr/bin/python

from librerie import *
import numpy as np
import time
import rospy


oggetti = []
oggettires = []
nomioggetti = ['Proximity_sensorCE', 'Proximity_sensorDX', 'Proximity_sensorSX', 'Micro_SX', 'Micro_DX', 'Micro_CE', 'Lidar', 'MV_Camera',
               'Pi_Camera', 'Motore_AD', 'Motore_AS', 'Motore_PD', 'Motore_PS']
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
    for i in range(0, 13):
        res, mario = simxGetObjectHandle(connessione, nomioggetti[i], simx_opmode_blocking)
        if i < 6:
            simxReadProximitySensor(connessione, mario, simx_opmode_streaming)
        elif i < 7:
            simxReadProximitySensor(connessione, mario, simx_opmode_streaming)
            simxGetObjectOrientation(connessione, mario, sim_handle_parent, simx_opmode_streaming)
        elif i < 9:
            simxGetVisionSensorImage(connessione, mario, 1, simx_opmode_streaming)
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


def angololidar(connessione):
    returnCode, number = simxGetObjectOrientation(connessione, oggetti[6], sim_handle_parent, simx_opmode_buffer)
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


def micro(connessione, micros):
    stati = []
    for Micro in micros:
        ris, stato, coordinate, handleoggettoris, vettorenormalizzato = simxReadProximitySensor(connessione, Micro, simx_opmode_buffer)
        stati.append(stato)
    return stati


def forward(connessione, motors, velocita):
    ris1 = simxSetJointTargetVelocity(connessione, motors[3], velocita, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(connessione, motors[1], velocita, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(connessione, motors[2], velocita, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(connessione, motors[0], velocita, simx_opmode_oneshot_wait)
    return ris1, ris2, ris3, ris4


def backward(connessione, motors, velocita):
    ris1 = simxSetJointTargetVelocity(connessione, motors[3], -velocita, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(connessione, motors[1], -velocita, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(connessione, motors[2], -velocita, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(connessione, motors[0], -velocita, simx_opmode_oneshot_wait)
    return ris1, ris2, ris3, ris4


def left(connessione, motors):
    ris1 = simxSetJointTargetVelocity(connessione, motors[0], +2, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(connessione, motors[1], -2, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(connessione, motors[2], +2, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(connessione, motors[3], -2, simx_opmode_oneshot_wait)
    return ris1, ris2, ris3, ris4


def right(connessione, motors):
    ris1 = simxSetJointTargetVelocity(connessione, motors[0], -2, simx_opmode_oneshot_wait)
    ris2 = simxSetJointTargetVelocity(connessione, motors[1], +2, simx_opmode_oneshot_wait)
    ris3 = simxSetJointTargetVelocity(connessione, motors[2], -2, simx_opmode_oneshot_wait)
    ris4 = simxSetJointTargetVelocity(connessione, motors[3], +2, simx_opmode_oneshot_wait)
    return ris1, ris2, ris3, ris4



clientID = connessione()
oggetti=objectoggetti(clientID)

# for i in range(0, 89):
#     print ("Angolo")
#     print (lidar(clientID, oggetti[6], +1.0))
# for i in range(0, 179):
#     print ("Angolo")
#     print (lidar(clientID, oggetti[6], -1.0))
# micros = [oggetti[3], oggetti[4], oggetti[5]]
# print (micro(clientID,micros))
# motor = [oggetti[9], oggetti[10], oggetti[11], oggetti[12]]
# print (left(clientID, motor))

def main():
    clientID = connessione()
    objectoggetti(clientID)
    immagine(clientID, oggetti[7])


main()