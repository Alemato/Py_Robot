#! /usr/bin/python

import pyswip.prolog
import py_robot.msg as PyRobot
import rospy

controller_sub = PyRobot.Controller_Node()
prolog_pub = PyRobot.Prolog_IA_Node()


def callback(msg):
    domanda = msg.domanda
    switch = msg.switch
    sonar = msg.sonar
    volt = msg.volt
    lidar = msg.lidar
    angle16 = msg.angle16
    angle8 = msg.angle8
    pitch = msg.pitch
    roll = msg.roll
    mag = msg.mag
    acc = msg.acc
    gyro = msg.gyro
    temp = msg.temp

    prolog = pyswip.Prolog()

    prolog.assertz("sonar(sinistra, " + str(sonar[0]) + ")")
    prolog.assertz("sonar(centro, " + str(sonar[1]) + ")")
    prolog.assertz("sonar(destra, " + str(sonar[2]) + ")")
    prolog.assertz("volt(" + str(volt) + ")")
    prolog.assertz("angolo16(" + str(angle16) + ")")
    prolog.assertz("angole8(" + str(angle8) + ")")
    prolog.assertz("pitch(" + str(pitch) + ")")
    prolog.assertz("roll(" + str(roll) + ")")

    prolog.assertz("command(1, dritto)")
    prolog.assertz("commnad(2, destra)")
    prolog.assertz("command(3, sinistra)")
    prolog.assertz("commnad(4, indietro)")
    prolog.assertz("command(5, stop)")

    prolog.assertz(
        "sonar(Y) :- sonar(destra, A), sonar(centro, B), sonar(sinistra, C), D is max(A, B), X is max(D, C), sonar(Y, X)")

    prolog.assertz("command(X):- switch(_,0), volt(Y), Y > 11, C is 1, command(C,X),!. ")
    prolog.assertz("command(X):- switch(_,1), volt(Y), Y > 11, C is 4, command(C,X),!.")


def main():
    controller_sub = rospy.Subscriber("prolog_sub", PyRobot.Prolog_Node, callback)


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
