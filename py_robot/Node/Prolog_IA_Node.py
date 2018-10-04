#! /usr/bin/python

import pyswip.prolog
import py_robot.msg as PyRobot
import rospy

controller_sub = PyRobot.Controller_Node()
prolog_pub = PyRobot.Prolog_IA_Node()


def callback(msg, args):
    commandolder = args[0]
    qrcode = msg.qrcode
    fotocamera = msg.fotocamera
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
    prolog.assertz("fotocamera(" + str(fotocamera) + ")")
    prolog.assertz("qrcode(" + str(qrcode) + ")")
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
    prolog.assertz("commandolder(" + str(commandolder) + ")")

    # Creazione comandi
    prolog.assertz("command(avanti, 1)")
    prolog.assertz("commnad(destra, 2)")
    prolog.assertz("command(sinistra, 3)")
    prolog.assertz("commnad(indietro, 4)")
    prolog.assertz("command(stop, 5)")

    # Creazione regole
    prolog.assertz(
        "sonar(Y) :- sonar(destra, A), sonar(centro, B), sonar(sinistra, C), D is max(A, B), X is max(D, C), sonar(Y, X)")

    # avanti
    prolog.assertz(
        "command(X):- commandolder(O), O \== indietro, switch(_,0), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == centro, fotocamera(F), F == centro, C is 3, command(X,C),!")
    prolog.assertz(
        "command(X):- commandolder(O), O \== indietro, switch(_,0), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == centro, C is 3, command(X,C),!")

    # sinistra
    prolog.assertz(
        "command(X):- commandolder(O), O \== indietro, switch(_,0), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == sinistra, fotocamera(F), F == sinistra, C is 1, command(X,C),!")
    prolog.assertz(
        "command(X):- commandolder(O), O \== indietro, switch(_,0), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == sinistra, C is 1, command(X,C),!")

    # destra
    prolog.assertz(
        "command(X):- commandolder(O), O \== indietro, switch(_,0), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == destra, fotocamera(F), F == destra, C is 2, command(X,C),!")
    prolog.assertz(
        "command(X):- commandolder(O), O \== indietro, switch(_,0), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == destra, C is 2, command(X,C),!")

    # indietro
    prolog.assertz("command(X):- commandolder(O), O \== indietro, switch(_,1), volt(Y), Y > 11, qrcode(Q), Q == 0, C is 4, command(X,C),!")

    # stop
    prolog.assertz("command(X):- commandolder(O), O == indietro, C is 5, command(X,C),!.")
    prolog.assertz("command(X):- C is 5, command(X,C),!")


def main():
    commandolder = None
    controller_sub = rospy.Subscriber("prolog_sub", PyRobot.Prolog_Node, callback, commandolder)


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
