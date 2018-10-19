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
    '''
    funzione che serve per prendere l'immagine da vrep
    :param clientID:
    :return: img immagine
    '''
    global oggetto
    err, resolution, image = simxGetVisionSensorImage(clientID, oggetto[0], 0, simx_opmode_buffer)
    img = np.array(image, dtype=np.uint8)
    img.resize([resolution[0], resolution[1], 3])
    img = np.rot90(img, 2)
    img = np.fliplr(img)
    print err
    print resolution
    print image
    # img.resize([resolution[0], resolution[1], 3])
    # img = np.rot90(img, 2)
    # img = np.fliplr(img)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def imgs(image):
    ris = cv2.Canny(image, 100, 200)
    misura = np.array([])
    height, width = ris.shape
    ris1 = ris.copy()
    for x in range(width - 1):
        for h in range(height - 1):
            hei = height - h - 1
            if ris1[hei, x] == 255:
                misura = np.append(misura, int(hei))
                break
            else:
                ris1.itemset((hei, x), 50)
    misura = np.split(misura, [90, 220])
    media_sinistra = np.median(misura[0])
    media_centrale = np.median(misura[1])
    media_destra = np.median(misura[2])
    print(media_sinistra, media_centrale, media_destra)
    if media_sinistra < media_centrale:
        if (media_sinistra < media_destra):
            print("vai a sinistra: ", media_sinistra)
            return "vai a sinistra"
        else:
            print("vai a destra: ", media_destra)
            return "vai a destra"
    elif media_centrale < media_destra:
        print("continua dritto: ", media_centrale)
        return "continua dritto"
    else:
        print("vai a destra: ", media_destra)
        return "via a destra"

def main():
    global clientID, oggetto
    clientID = connessione()
    oggetto = oggetti(clientID)
    print(oggetto)
    print(imgs(immagine(clientID)))
    # while (1):
    #     cv2.imshow('img', immagine(clientID))
    #     k = cv2.waitKey(5) & 0xFF
    #     if k == 27:
    #         break

if __name__ == '__main__':
    main()