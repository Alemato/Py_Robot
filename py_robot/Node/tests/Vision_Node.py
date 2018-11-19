#! /usr/bin/python

from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import time

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera)
bridge = CvBridge()
time.sleep(0.1)


def imgs():
    global camera, rawCapture, bridge
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    img = np.rot90(image, 2)
    img = np.fliplr(img)
    rawCapture.truncate(0)
    try:
        img = bridge.cv_to_imgmsg(img, "bgr8")
    except CvBridgeError, e:
        print e
    return img


def main():
    global bridge
    rospy.init_node("Vision_Node", anonymous=True)
    vision_pub = rospy.Publisher("vision", Image, queue_size=1)
    r = rospy.Rate(25)
    while not rospy.is_shutdown():
        try:
            vision_pub.publish(imgs())
        except CvBridgeError, e:
            print e
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass