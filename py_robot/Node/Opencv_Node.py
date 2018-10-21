#! /usr/bin/python

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
import py_robot.msg as PyRobot
import rospy

pi_camera_msg = PyRobot.Pi_Camera_Node()

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera)
time.sleep(0.1)


def imgs():
    global camera, rawCapture
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
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
    rawCapture.truncate(0)
    if media_sinistra < media_centrale:
        if (media_sinistra < media_destra):
            print("vai a sinistra: ", media_sinistra)
            return "sinistra"
        else:
            print("vai a destra: ", media_destra)
            return "destra"
    elif media_centrale < media_destra:
        print("continua dritto: ", media_centrale)
        return "centro"
    else:
        print("vai a destra: ", media_destra)
        return "destra"


def main():
    rospy.init_node("Pi_Camera_Node", disable_signals=True)
    pi_camera_pub = rospy.Publisher("pi_camera_pub", PyRobot.Pi_Camera_Node, queue_size=1)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        pi_camera_msg.visione = imgs()
        pi_camera_pub.publish(pi_camera_msg)
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass