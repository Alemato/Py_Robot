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

    # Inizializzazione Prolog
    prolog = pyswip.Prolog()

    # Creazione sentenze

    prolog.assertz("sonar(sinistra, " + str(sonar[0]) + ")")
    prolog.assertz("sonar(centro, " + str(sonar[1]) + ")")
    prolog.assertz("sonar(destra, " + str(sonar[2]) + ")")
    prolog.assertz("switch(sinistra, " + str(switch[0]) + ")")
    prolog.assertz("switch(centro, " + str(switch[1]) + ")")
    prolog.assertz("switc(destra, " + str(switch[2]) + ")")
    prolog.assertz("volt(" + str(volt) + ")")
    prolog.assertz("angolo16(" + str(angle16) + ")")
    prolog.assertz("angole8(" + str(angle8) + ")")
    prolog.assertz("pitch(" + str(pitch) + ")")
    prolog.assertz("roll(" + str(roll) + ")")
    prolog.assertz("mag(xhigh, " + str(mag[0]) + ")")
    prolog.assertz("mag(xlow " + str(mag[1]) + ")")
    prolog.assertz("mag(yhigh " + str(mag[2]) + ")")
    prolog.assertz("mag(ylow " + str(mag[3]) + ")")
    prolog.assertz("mag(zhigh " + str(mag[4]) + ")")
    prolog.assertz("mag(zlow " + str(mag[5]) + ")")
    prolog.assertz("acc(xhigh, " + str(acc[0]) + ")")
    prolog.assertz("acc(xlow " + str(acc[1]) + ")")
    prolog.assertz("acc(yhigh " + str(acc[2]) + ")")
    prolog.assertz("acc(ylow " + str(acc[3]) + ")")
    prolog.assertz("acc(zhigh " + str(acc[4]) + ")")
    prolog.assertz("acc(zlow " + str(acc[5]) + ")")
    prolog.assertz("gyro(xhigh, " + str(gyro[0]) + ")")
    prolog.assertz("gyro(xlow " + str(gyro[1]) + ")")
    prolog.assertz("gyro(yhigh " + str(gyro[2]) + ")")
    prolog.assertz("gyro(ylow " + str(gyro[3]) + ")")
    prolog.assertz("gyro(zhigh " + str(gyro[4]) + ")")
    prolog.assertz("gyro(zlow " + str(gyro[5]) + ")")
    prolog.assertz("temp(" + str(temp) + ")")

    # Creazione regole

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
