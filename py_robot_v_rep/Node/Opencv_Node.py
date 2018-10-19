#! /usr/bin/python

from librerie import *
import cv2
import numpy as np
import time
import py_robot.msg as PyRobot
import rospy

clientID = None
oggetto = []
img = None
ris1 = None
ris = None
pi_camera_msg = PyRobot.Pi_Camera_Node()


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
    err, resolution, image = simxGetVisionSensorImage(clientID, objecthandle, 0, simx_opmode_streaming)
    time.sleep(1)
    if not res == 0:
        print ("Creation Error")
        return
    else:
        print ("Creation " + nomioggetti[0])
        oggetto.append(objecthandle)
    return oggetto


def immagine(clientID):
    """
    funzione che serve per prendere l'immagine da vrep
    :param clientID:
    :return: img immagine
    """
    global oggetto, img
    err, resolution, image = simxGetVisionSensorImage(clientID, oggetto[0], 0, simx_opmode_buffer)
    if not err == 0:
        print ("Image Received")
    else:
        print ("ERROR IMAGE")
    img = np.array(image, dtype=np.uint8)
    img.resize([resolution[0], resolution[1], 3])
    img = np.rot90(img, 2)
    img = np.fliplr(img)
    return img


def imgs(image):
    """
    funzione che elabora l'immagine ricevuta, ritorna comando
    :param image: immagine del mondo v-rep
    :return: string command
    """
    global ris1, ris
    ris = cv2.Canny(image, 100, 200)
    misura = np.array([])
    height, width = ris.shape
    print (height, width)
    ris1 = ris.copy()
    for x in range(width - 1):
        for h in range(height - 1):
            hei = height - h - 1
            if ris1[hei, x] == 255:
                misura = np.append(misura, int(hei))
                break
            else:
                ris1.itemset((hei, x), 50)
    misura = np.split(misura, [150, 362])
    media_sinistra = np.median(misura[0])
    media_centrale = np.median(misura[1])
    media_destra = np.median(misura[2])
    print ("MEDIANS ")
    print(media_sinistra, media_centrale, media_destra)
    print ("COMMAND ")
    if media_sinistra < media_centrale:
        if (media_sinistra < media_destra):
            print("vai a sinistra: ", media_sinistra)
            return "sinistra"
        else:
            print("vai a destra: ", media_destra)
            return "vai a destra"
    elif media_centrale < media_destra:
        print("continua dritto: ", media_centrale)
        return "dritto"
    else:
        print("vai a destra: ", media_destra)
        return "destra"


def main():
    global clientID, oggetto, img, ris1, ris
    clientID = connessione()
    oggetto = oggetti(clientID)
    rospy.init_node("Pi_Camera_Node", disable_signals=True)
    pi_camera_pub = rospy.Publisher("pi_camera_pub", PyRobot.Pi_Camera_Node, queue_size=1)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        pi_camera_msg.visione = imgs(immagine(clientID))
        pi_camera_pub.publish(pi_camera_msg)
        r.sleep()
    # while (1):
    #     cv2.imshow('img', img)
    #     cv2.imshow('ris', ris)
    #     cv2.imshow('ris1', ris1)
    #     k = cv2.waitKey(5) & 0xFF
    #     if k == 27:
    #         break


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass