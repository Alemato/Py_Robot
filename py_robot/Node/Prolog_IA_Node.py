#! /usr/bin/python

import pyswip.prolog
import py_robot.msg as PyRobot
import rospy
import time
import numpy as np

prolog_msg = PyRobot.Prolog_IA_Node()

prolog = None
commandolder = "avanti"
oldangle = None


# var global
qrcode = None
fotocamera = None
switch = None
sonar = None
volt = None
lidar = None
angle16 = None
angle8 = None
pitch = None
roll = None
mag = None
acc = None
gyro = None
temp = None
lidarm = None


def resetNone():
    """
    Funzione per il reset delle variabili ambientali
    :return:
    """
    global qrcode, fotocamera, switch, sonar, volt, lidar, angle16, angle8, pitch, roll, mag, acc, gyro, temp
    qrcode = None
    fotocamera = None
    switch = None
    sonar = None
    volt = None
    lidar = None
    angle16 = None
    angle8 = None
    pitch = None
    roll = None
    mag = None
    acc = None
    gyro = None
    temp = None


def prologinit_and_rules():
    """
    Funzione per l'inizializzazione di prolog e la creazione delle regole
    :return: nulla
    """
    global prolog

    ###########################
    # INIZIALIZZAZIONE PROLOG #
    ###########################

    prolog = pyswip.Prolog()

    ###########################
    # CREAZIONE COMANDI ROVER #
    ###########################

    # comandi disponibili
    prolog.assertz("command(avanti, 1)")
    prolog.assertz("command(sinistra, 2)")
    prolog.assertz("command(destra, 3)")
    prolog.assertz("command(indietro,4)")
    prolog.assertz("command(stop, 5)")
    prolog.assertz("command(fine, 6)")
    prolog.assertz("command(batteria, 7)")
    prolog.assertz("command(correggi_a_destra, 8)")
    prolog.assertz("command( correggi_a_sinistra, 9)")

    #############################
    # CREAZIONE REGOLE GENERALI #
    #############################

    # regola per gli switch false se sbatte true se non sbatte
    prolog.assertz("switch(_):- switch(sinistra,X), switch(centro,Y), switch(destra, Z), X == 0, Y == 0, Z == 0, !")

    # regola per il cambio direzione
    prolog.assertz("distancetrue(_):- sonar(destra, A), sonar(centro, B), sonar(sinistra, C),  A > 50, B > 50, C > 50, !")

    # regola per il cambio direzione (indietro) a una certa distanza da un possibile ostacolo troppo vicino
    prolog.assertz("sonartrue(_):- sonar(destra, A), sonar(centro, B), sonar(sinistra, C),  A > 30, B > 30, C > 30, !")

    # regola per capire quale e' il sonar con la distanza maggiore
    prolog.assertz("sonar(Y) :- sonar(centro, A), sonar(destra, B), sonar(sinistra, C), D is max(A, B),"
                   " X is max(D, C), sonar(Y, X),!")

    # regola per capire quale e' il sonar tra destra e sinistra maggiore
    prolog.assertz("sonardxsx(Y):- sonar(destra, A), sonar(sinistra, B), X is max(A, B), sonar(Y, X), Y \== centro, !")

    # regola per le condizioni necessarie per il cambio di qualasiasi direzione
    prolog.assertz("condictrue(_):- switch(_), volt(Y), Y>11, qrcode(Q), Q == 0, !")

    # commando batteria
    prolog.assertz("command(X):- volt(Y), Y < 11, C is 7, command(X, C),!")

    # comando fine
    prolog.assertz("command(X):- qrcode(1), C is 6, command(X,C),!")

    # comando coregi a destra
    prolog.assertz("command(X):-commandolder(O), O == avanti, condictrue(_), distancetrue(_), angle8(A), oldangle8(B),"
                   " S is A-B, S > 10, command(X, 8),!")

    # comando coregi a sinistra
    prolog.assertz("command(X):-commandolder(O), O == avanti, condictrue(_), distancetrue(_), angle8(A), oldangle8(B),"
                   " S is B-A, S > 10, command(X, 9),!")

    # comando indietro
    prolog.assertz("command(X):- commandolder(O), O \== indietro, \+ sonartrue(_), volt(Y), Y > 11,"
                   " qrcode(Q), Q == 0, command(X,4),!")
    prolog.assertz("command(X):- commandolder(O), O \== indietro, switch(_,1), volt(Y), Y > 11,"
                   " qrcode(Q), Q == 0, command(X,4),!")

    # comando avanti
    prolog.assertz("command(X):- commandolder(O), O == avanti, condictrue(_), distancetrue(_), command(X,1), !")
    prolog.assertz("command(X):- commandolder(O), O \== indietro, condictrue(_), distancetrue(_), sonar(U), "
                   "U == centro, fotocamera(F), F == centro, command(X,1), !")
    prolog.assertz("command(X):- commandolder(O), O \== indietro, condictrue(_), distancetrue(_),"
                   " sonar(U), U == centro, command(X,1), !")
    prolog.assertz("command(X):- commandolder(O), O \== indietro, condictrue(_), distancetrue(_), command(X,1), !")

    # comando sinistra
    prolog.assertz("command(X):- condictrue(_), sonartrue(_), sonardxsx(U), U == sinistra, fotocamera(F),"
                   " F == sinistra, command(X,2),!")
    prolog.assertz("command(X):- condictrue(_), sonartrue(_), sonardxsx(U), U == sinistra, command(X,2),!")

    # comando destra
    prolog.assertz("command(X):- condictrue(_), sonartrue(_), sonardxsx(U), U == destra, fotocamera(F),"
                   " F == destra, command(X,3), !")
    prolog.assertz("command(X):- condictrue(_), sonartrue(_), sonardxsx(U), U == destra, command(X,3) ,!")

    # comando indietro che viene eseguito quando non c'e' spazio per girare a destra o a sinista
    prolog.assertz("command(X):- \+ sonartrue(_), volt(Y), Y > 11, qrcode(Q), Q == 0, command(X,4),!")

    # comando stop (errore)
    prolog.assertz("command(X):- command(X,5),!")


def prologIA(commandolder, qrcode, fotocamera, switch, sonar, volt, lidar,
             angle16, angle8, pitch, roll, mag, acc, gyro, temp, oldangle, lidarm):
    """
    Funzione per il caricamento dei fatti, per esecuzione delle query e della demolizione dei fatti caricati
    :param commandolder:  vecchio comando di default e' avanti
    :param qrcode: 0 per non trovato 1 per trovato
    :param fotocamera: vale sinistra o destra o centro e identifica lo spazio libero
    :param switch: 0 se non attivo 1 per attivo e' un arry di 3 elementi
    :param sonar: vale la misurazione effettuata e' un array di 3 elementi
    :param volt: vale la misurazione effettuata
    :param lidar: vale le misurazioni effettuate e' un array di 19 elementi
    :param angle16: vale la misurazione effettuata
    :param angle8: vale la misurazione effettuata
    :param pitch: vale la misurazione effettuata
    :param roll: vale la misurazione effettuata
    :param mag: vale le misurazioni effettuate e' un array di 6 elementi
    :param acc: vale le misurazioni effettuate e' un array di 6 elementi
    :param gyro: vale le misurazioni effettuate e' un array di 6 elementi
    :param temp: vale la misurazione effettuata
    :param oldangle: vale un angolo iniziale
    :return: resultato della query
    """
    global prolog

    ###################
    # CREAZIONE FATTI #
    ###################

    # comando vecchio
    prolog.assertz("commandolder(" + str(commandolder) + ")")

    # qrcode:  0 per false 1 per true
    prolog.assertz("qrcode(" + str(qrcode) + ")")

    # fotocomera
    prolog.assertz("fotocamera(" + str(fotocamera) + ")")

    # switch
    prolog.assertz("switch(centro, " + str(switch[1]) + ")")
    prolog.assertz("switch(sinistra, " + str(switch[0]) + ")")
    prolog.assertz("switch(destra, " + str(switch[2]) + ")")

    # sonar: mettere prima il centro cosi se sono 3 sonar uguali il sistema prendera il primo e quindi va avanti
    prolog.assertz("sonar(centro, " + str(sonar[1]) + ")")
    prolog.assertz("sonar(sinistra, " + str(sonar[0]) + ")")
    prolog.assertz("sonar(destra, " + str(sonar[2]) + ")")

    # volt
    prolog.assertz("volt(" + str(volt) + ")")

    # compass
    prolog.assertz("angle16(" + str(angle16) + ")")
    prolog.assertz("angle8(" + str(angle8) + ")")
    prolog.assertz("pitch(" + str(pitch) + ")")
    prolog.assertz("roll(" + str(roll) + ")")
    prolog.assertz("mag(xhigh, " + str(mag[0]) + ")")
    prolog.assertz("mag(xlow, " + str(mag[1]) + ")")
    prolog.assertz("mag(yhigh, " + str(mag[2]) + ")")
    prolog.assertz("mag(ylow, " + str(mag[3]) + ")")
    prolog.assertz("mag(zhigh, " + str(mag[4]) + ")")
    prolog.assertz("mag(zlow, " + str(mag[5]) + ")")
    prolog.assertz("acc(xhigh, " + str(acc[0]) + ")")
    prolog.assertz("acc(xlow, " + str(acc[1]) + ")")
    prolog.assertz("acc(yhigh, " + str(acc[2]) + ")")
    prolog.assertz("acc(ylow, " + str(acc[3]) + ")")
    prolog.assertz("acc(zhigh, " + str(acc[4]) + ")")
    prolog.assertz("acc(zlow, " + str(acc[5]) + ")")
    prolog.assertz("gyro(xhigh, " + str(gyro[0]) + ")")
    prolog.assertz("gyro(xlow, " + str(gyro[1]) + ")")
    prolog.assertz("gyro(yhigh, " + str(gyro[2]) + ")")
    prolog.assertz("gyro(ylow, " + str(gyro[3]) + ")")
    prolog.assertz("gyro(zhigh, " + str(gyro[4]) + ")")
    prolog.assertz("gyro(zlow, " + str(gyro[5]) + ")")
    prolog.assertz("temp(" + str(temp) + ")")

    # angolo vecchio
    prolog.assertz("oldangle8(" + str(oldangle) + ")")

    ###################################################################################################################

    ##########################
    # ESEQUZIONE DELLA QUERY #
    ##########################

    result = list(prolog.query("command(Result)"))

    ###################################################################################################################

    #################################
    # DEMOLIZIONE DEI FATTI CARICATI#
    #################################

    # comando vecchio
    prolog.retract("commandolder(" + str(commandolder) + ")")

    # qrcode:  0 per false 1 per true
    prolog.retract("qrcode(" + str(qrcode) + ")")

    # fotocomera
    prolog.retract("fotocamera(" + str(fotocamera) + ")")

    # switch
    prolog.retract("switch(centro, " + str(switch[1]) + ")")
    prolog.retract("switch(sinistra, " + str(switch[0]) + ")")
    prolog.retract("switch(destra, " + str(switch[2]) + ")")

    # sonar: mettere prima il centro cosi se sono 3 sonar uguali il sistema prendera il primo e quindi va avanti
    prolog.retract("sonar(centro, " + str(sonar[1]) + ")")
    prolog.retract("sonar(sinistra, " + str(sonar[0]) + ")")
    prolog.retract("sonar(destra, " + str(sonar[2]) + ")")

    # volt
    prolog.retract("volt(" + str(volt) + ")")

    # compass
    prolog.retract("angle16(" + str(angle16) + ")")
    prolog.retract("angle8(" + str(angle8) + ")")
    prolog.retract("pitch(" + str(pitch) + ")")
    prolog.retract("roll(" + str(roll) + ")")
    prolog.retract("mag(xhigh, " + str(mag[0]) + ")")
    prolog.retract("mag(xlow, " + str(mag[1]) + ")")
    prolog.retract("mag(yhigh, " + str(mag[2]) + ")")
    prolog.retract("mag(ylow, " + str(mag[3]) + ")")
    prolog.retract("mag(zhigh, " + str(mag[4]) + ")")
    prolog.retract("mag(zlow, " + str(mag[5]) + ")")
    prolog.retract("acc(xhigh, " + str(acc[0]) + ")")
    prolog.retract("acc(xlow, " + str(acc[1]) + ")")
    prolog.retract("acc(yhigh, " + str(acc[2]) + ")")
    prolog.retract("acc(ylow, " + str(acc[3]) + ")")
    prolog.retract("acc(zhigh, " + str(acc[4]) + ")")
    prolog.retract("acc(zlow, " + str(acc[5]) + ")")
    prolog.retract("gyro(xhigh, " + str(gyro[0]) + ")")
    prolog.retract("gyro(xlow, " + str(gyro[1]) + ")")
    prolog.retract("gyro(yhigh, " + str(gyro[2]) + ")")
    prolog.retract("gyro(ylow, " + str(gyro[3]) + ")")
    prolog.retract("gyro(zhigh, " + str(gyro[4]) + ")")
    prolog.retract("gyro(zlow, " + str(gyro[5]) + ")")
    prolog.retract("temp(" + str(temp) + ")")

    # angolo vecchio
    prolog.retract("oldangle8(" + str(oldangle) + ")")

    return result


def callback(msg):
    """
    funzione di callback di Ros, effetua le valutazioni del mondo circostante e fa uuna scelta
    :param msg: messaggio ros dal controller
    :return: nulla
    """
    global commandolder, oldangle, commandIA, qrcode, fotocamera, switch, sonar, volt,\
        lidar, angle8, angle16, pitch, roll, mag, acc, gyro, temp
    qrcode = msg.qrcode
    fotocamera = msg.visione
    switch = msg.switches
    switch[0] = int(switch[0])
    switch[1] = int(switch[1])
    switch[2] = int(switch[2])
    sonare = msg.sonar
    sonar = (int(sonare[0]), int(sonare[1]), int(sonare[2]))
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


def ifNotNone(qrcode, fotocamera, switch, sonar, volt, lidar, angle16, angle8, pitch, roll, mag, acc, gyro, temp):
    """
    Funzione di controlo delle variabili globali,
    controlla se sono state modificate tutte
    :param qrcode:
    :param fotocamera:
    :param switch:
    :param sonar:
    :param volt:
    :param lidar:
    :param angle16:
    :param angle8:
    :param pitch:
    :param roll:
    :param mag:
    :param acc:
    :param gyro:
    :param temp:
    :return: True se non sono None e False se sono None
    """
    return qrcode is not None and fotocamera is not None and switch is not None and sonar is not None and\
           volt is not None and lidar is not None and angle16 is not None and angle8 is not None and\
           pitch is not None and roll is not None and mag is not None and acc is not None and\
           gyro is not None and temp is not None


def main():
    global commandolder, oldangle, commandIA, qrcode, fotocamera, switch, sonar,\
        volt, lidar, angle8, angle16, pitch, roll, mag, acc, gyro, temp, lidarm
    commandIA = ''
    prologinit_and_rules()
    print("prolog rules")
    rospy.init_node("Prologo_IA_Node", disable_signals=True)
    prolog_pub = rospy.Publisher("prolog_ia", PyRobot.Prolog_IA_Node, queue_size=0)
    rospy.Subscriber("controller", PyRobot.Controller_Node, callback)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        if commandIA == '':
            if ifNotNone(qrcode, fotocamera, switch, sonar, volt, lidar,
                         angle16, angle8, pitch, roll, mag, acc, gyro, temp):

                if commandolder == "correggi_a_destra" or\
                        commandolder == "correggi_a_sinistra" or oldangle is None:
                    oldangle = angle8

                commandIA = prologIA(commandolder, qrcode, fotocamera, switch, sonar, volt, lidar,
                                     angle16, angle8, pitch, roll, mag, acc, gyro, temp, oldangle, lidarm)

                if commandIA == "sinistra" or commandIA == "destra" or commandIA == "indietro":
                    oldangle = None

                commandolder = None
                commandolder = commandIA[0]['Result']
                prolog_msg.risposta = commandIA[0]['Result']
                prolog_pub.publish(prolog_msg)
                rospy.loginfo(prolog_msg)
                commandIA = ''
                resetNone()
                r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass