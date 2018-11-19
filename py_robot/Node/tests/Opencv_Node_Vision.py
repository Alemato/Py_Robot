#! /usr/bin/python

import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import py_robot.msg as PyRobot

pi_camera_msg = PyRobot.Pi_Camera_Node()
bridge = CvBridge()


def callback_img(msg):
    global bridge, original_pub, canndy_pub, result_pub, pi_camera_pub
    #command = None
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print e

    ris = cv2.Canny(cv_image, 100, 200)
    # creo un array vuoto che mi serve per le altezze
    misura = np.array([])

    # prendo le misure del fotogramma
    height, width = ris.shape

    # creo una copia del fotogramma
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
            comand = "sinistra"
        else:
            print("vai a destra: ", media_destra)
            comand = "destra"
    elif media_centrale < media_destra:
        print("continua dritto: ", media_centrale)
        comand = "centro"
    else:
        print("vai a destra: ", media_destra)
        comand = "destra"

    original_pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    canndy_pub.publish(bridge.cv2_to_imgmsg(ris, "mono8"))
    result_pub.publish(bridge.cv2_to_imgmsg(ris1, "mono8"))
    pi_camera_msg.visione = comand
    pi_camera_pub.publish(pi_camera_msg)


def main():
    global bridge, original_pub, canndy_pub, result_pub, pi_camera_pub
    rospy.init_node("OpenCV_Node", anonymous=True)
    rospy.Subscriber("vision", Image, callback_img)
    original_pub = rospy.Publisher("original_image", Image, queue_size=1)
    canndy_pub = rospy.Publisher("canndy_image", Image, queue_size=1)
    result_pub = rospy.Publisher("result_image", Image, queue_size=1)
    pi_camera_pub = rospy.Publisher("pi_camera", PyRobot.Pi_Camera_Node, queue_size=1)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass