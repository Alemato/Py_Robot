#! /usr/bin/python

from librerie import *
import cv2
import numpy as np


clientID = None
oggetto = []


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
    funzione che crea l'oggetto Pi_Camera nel modo v-rep
    :var globale oggetto: rappresenta l'oggetto Pi_Camera, e' di tipo lista
    :param clientID: connesione v-rep
    :return: oggetto
    """
    global oggetto
    nomioggetti = ['Pi_Camera']
    res, objecthandle = simxGetObjectHandle(clientID, 'Pi_Camera', simx_opmode_oneshot_wait)
    print res
    if not res == 0:
        print ("Creation Error")
        return
    else:
        print ("Creation " + nomioggetti[0])
        oggetto.append(objecthandle)
    return oggetto


def immagine(clientID):
    global oggetto
    err, resolution, image = simxGetVisionSensorImage(clientID, oggetto[0], 1, simx_opmode_streaming)
    err, resolution, image = simxGetVisionSensorImage(clientID, oggetto[0], 1, simx_opmode_buffer)
    img = np.array(image, dtype=np.uint8)
    print err
    print resolution
    print image
    # img.resize([resolution[0], resolution[1], 3])
    # img = np.rot90(img, 2)
    # img = np.fliplr(img)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def main():
    global clientID, oggetto
    clientID = connessione()
    oggetto = oggetti(clientID)
    print oggetto
    immagine(clientID)
    # while (1):
    #     cv2.imshow('img', immagine(clientID))
    #     k = cv2.waitKey(5) & 0xFF
    #     if k == 27:
    #         break

if __name__ == '__main__':
    main()