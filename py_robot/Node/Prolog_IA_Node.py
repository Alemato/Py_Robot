#! /usr/bin/python

import pyswip.prolog
import py_robot.msg as PyRobot
import rospy

prolog_msg = PyRobot.Prolog_IA_Node()

commandolder = "avanti"
oldangle = None
commandIA = None


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

def resetNone():
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



def prologIA(commandolder, qrcode, fotocamera, switch, sonar, volt, lidar, angle16, angle8, pitch, roll, mag, acc, gyro,
             temp, oldangle):
    """
    funzione che esegue prolog
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

    print("entro")
    # Inizializzazione Prolog
    prolog = pyswip.Prolog()

    ###################
    # Creazione fatti #
    ###################

    # fotocomera
    prolog.assertz("fotocamera(" + str(fotocamera) + ")")

    # qrcode 0 per false 1 per true
    prolog.assertz("qrcode(" + str(qrcode) + ")")

    # mettere prima il destro cosi se sono 3 sonar uguali il sistema prendera il primo e quindi va avanti
    prolog.assertz("sonar(sinistra, " + str(sonar[0]) + ")")
    prolog.assertz("sonar(centro, " + str(sonar[1]) + ")")
    prolog.assertz("sonar(destra, " + str(sonar[2]) + ")")

    # switch
    prolog.assertz("switch(sinistra, " + str(switch[0]) + ")")
    prolog.assertz("switch(centro, " + str(switch[1]) + ")")
    prolog.assertz("switch(destra, " + str(switch[2]) + ")")

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

    #
    prolog.assertz("commandolder(" + commandolder + ")")
    # Creazione comandi
    prolog.assertz("command(avanti, 1)")
    prolog.assertz("command(destra, 2)")
    prolog.assertz("command(sinistra, 3)")
    prolog.assertz("command(indietro, 4)")
    prolog.assertz("command(stop, 5)")
    prolog.assertz("command(fine, 6)")
    prolog.assertz("command(batteria, 7)")
    prolog.assertz("command(correggi_a_destra, 8)")
    prolog.assertz("command(correggi_a_sinistra, 9)")
    prolog.assertz("command(attiva_lidar, 10)")

    #############################
    # Creazione regole generali #
    #############################

    # regola per gli switch false se sbatte true se non sbatte
    prolog.assertz("switch(_):- switch(sinistra,X), switch(centro,Y), switch(destra, Z), X == 0, Y == 0, Z == 0, !")

    # regola per i sonar, serve per far cambiare la direzione predefinita dritto a una certa distanza da un possibile ostacolo
    prolog.assertz("sonartrue(_):- sonar(destra, A), sonar(centro, B), sonar(sinistra, C),  A > 10, B > 10, C > 10, !")

    # regola per capire quale e' il sonar con la distanza maggiore
    prolog.assertz("sonar(Y) :- sonar(centro, A), sonar(destra, B), sonar(sinistra, C), D is max(A, B), X is max(D, "
                   "C), sonar(Y, X),!")

    # comando batteria
    prolog.assertz("command(X):- volt(Y), Y < 11, C is 7, command(X, C),!")

    # comando fine
    prolog.assertz("command(X):- qrcode(1), C is 6, command(X,C),!")

    # comando attiva lidar
    prolog.assertz("command(X):- commandolder(O), O \== indietro, switch(_,1), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "C is 10, command(X,C),!")

    # comando coregi a destra
    prolog.assertz("command(X):-commandolder(O), O == avanti, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "sonartrue(_), angle8(A), oldangle8(B), S is A-B, S > 10, C is 8, command(X, C),!")

    # comando coregi a sinistra
    prolog.assertz("command(X):-commandolder(O), O == avanti, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "sonartrue(_), angle8(A), oldangle8(B), S is B-A, S > 10, C is 9, command(X, C),!")

    # comando indietro
    prolog.assertz("command(X):- commandolder(O), O \== indietro, \+ sonartrue(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "C is 4, command(X,C),!")

    # comando avanti
    prolog.assertz("command(X):- commandolder(O), O == avanti, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "sonartrue(_), C is 3, command(X,C),!")
    prolog.assertz("command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "sonar(U), U == centro, fotocamera(F), F == centro, C is 3, command(X,C),!")
    prolog.assertz("command(X):- commandolder(O), O \== indietro,switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "sonar(U), U == centro, C is 3, command(X,C),!")

    # comando sinistra
    prolog.assertz("command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "sonar(U), U == sinistra, fotocamera(F), F == sinistra, C is 1, command(X,C),!")
    prolog.assertz("command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "sonar(U), U == sinistra, C is 1, command(X,C),!")

    # comando destra
    prolog.assertz("command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "sonar(U), U == destra, fotocamera(F), F == destra, C is 2, command(X,C),!")
    prolog.assertz("command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, "
                   "sonar(U), U == destra, C is 2, command(X,C),!")

    # comando stop
    prolog.assertz("command(X):- C is 5, command(X,C),!")

    ###############################
    # Fatti e Regole per il lidar #
    ###############################

    if commandolder == "attiva_lidar":
        ################################
        # Creazione fatti per il lidar #
        ################################

        # lidar ogni 10 gradi
        prolog.assertz("lidar(0, " + str(lidar[0]) + ")")
        prolog.assertz("lidar(10, " + str(lidar[1]) + ")")
        prolog.assertz("lidar(20, " + str(lidar[2]) + ")")
        prolog.assertz("lidar(30, " + str(lidar[3]) + ")")
        prolog.assertz("lidar(40, " + str(lidar[4]) + ")")
        prolog.assertz("lidar(50, " + str(lidar[5]) + ")")
        prolog.assertz("lidar(60, " + str(lidar[6]) + ")")
        prolog.assertz("lidar(70, " + str(lidar[7]) + ")")
        prolog.assertz("lidar(80, " + str(lidar[8]) + ")")
        prolog.assertz("lidar(90, " + str(lidar[9]) + ")")
        prolog.assertz("lidar(100, " + str(lidar[10]) + ")")
        prolog.assertz("lidar(110, " + str(lidar[11]) + ")")
        prolog.assertz("lidar(120, " + str(lidar[12]) + ")")
        prolog.assertz("lidar(130, " + str(lidar[13]) + ")")
        prolog.assertz("lidar(140, " + str(lidar[14]) + ")")
        prolog.assertz("lidar(150, " + str(lidar[15]) + ")")
        prolog.assertz("lidar(160, " + str(lidar[16]) + ")")
        prolog.assertz("lidar(170, " + str(lidar[17]) + ")")
        prolog.assertz("lidar(180, " + str(lidar[18]) + ")")

        #################################
        # Creazione regole per il lidar #
        #################################

        # regola per il lidar ritorna l'angolo con la distanza maggiore
        prolog.assertz("lidar(X):- lidar(0,A),lidar(10,B),lidar(20,C),lidar(30,D),lidar(40,E),lidar(50,F),lidar(60,"
                       "G),lidar(70,H),lidar(80,I),lidar(90,L),lidar(100,M),lidar(110,N),lidar(120,O),lidar(130,P),"
                       "lidar(140,Q),lidar(150,R),lidar(160,S),lidar(170,T),lidar(180,U), V is max(A,B), V1 is max(V,"
                       "C),V2 is max(V1,D),V3 is max(V2,E),V4 is max(V3,F),V5 is max(V4,G), V6 is max(V5,H), "
                       "V7 is max(V6,I), V8 is max(V7,L), V9 is max(V8,M), V10 is max(V9,N), V11 is max(V10,O), "
                       "V12 is max(V11,P), V13  is max(V12,Q), V14 is max(V13,R), V15 is max(V14,S), V16 is max(V15,"
                       "T), V17 is max(V16,U), lidar(X,V17),!")

        # comando avanti
        prolog.assertz("commandlidar(X):-lidar(B), B < 121, B > 61, switch(_), volt(Y), Y > 11,qrcode(Q), Q == 0, "
                       "C is 3, command(X,C),!")

        # comando sinistra
        prolog.assertz(
            "commandlidar(X):-lidar(B), B > 120,switch(_), volt(Y), Y > 11,qrcode(Q), Q == 0, C is 1, command(X,C),!")

        # comando destra
        prolog.assertz(
            "commandlidar(X):-lidar(B), B < 60,switch(_), volt(Y), Y > 11,qrcode(Q), Q == 0, C is 2, command(X,C),!")

        # comando stop
        prolog.assertz("commandlidar(X):- C is 5, command(X,C),!")

        ####################
        # Esequzione Query #
        ####################
        result = list(prolog.query("commandlidar(Result)"))



    #############################
    # Esequzione query generale #
    #############################
    result1 = list(prolog.query("command(Result)"))
    prolog = None
    if commandolder == "attiva_lidar":
        return result
    else:
        return result1

def callback(msg):
    """
    funzione di callback di Ros, effetua le valutazioni del mondo circostante e fa uuna scelta
    :param msg: messaggio ros dal controller
    :return: nulla
    """
    global commandolder, oldangle, commandIA, qrcode, fotocamera, switch,sonar,volt,lidar,angle8,angle16,pitch,roll,mag,acc,gyro,temp
    qrcode = msg.qrcode
    fotocamera = msg.visione
    switch = msg.switches
    switch[0] = int(switch[0])
    switch[1] = int(switch[1])
    switch[2] = int(switch[2])
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

def ifNotNone(angle16, angle8, pitch, roll, mag, acc, gyro, temp, volt, sonar, fotocamera):
    """
    funzione di controlo delle variabili globali,
    controlla se sono state modificate tutte
    :param angle16: misura del angolo a 16
    :param angle8: misura del angolo a 8
    :param pitch: misura del pitch
    :param roll: misura del roll
    :param mag: misura del mag
    :param acc: misura del acc
    :param gyro: misura del gyro
    :param temp: misura della temperatura
    :param comando: variabile del comando da inviare
    :param volt: misura della batteria
    :param sonar: misura dei sonar
    :return: True se sono modificate, False se sono ancora nulle
    """
    return angle16 is not None and angle8 is not None and pitch is not None and roll is not None and mag is not None and acc is not None and gyro is not None and temp is not None and volt is not None and sonar is not None and fotocamera is not None




def main():
    global commandIA
    global commandolder, oldangle, commandIA, qrcode, fotocamera, switch, sonar, volt, lidar, angle8, angle16, pitch, roll, mag, acc, gyro, temp
    rospy.init_node("Prologo_IA_Node", disable_signals=True)
    prolog_pub = rospy.Publisher("prolog_ia", PyRobot.Prolog_IA_Node, queue_size=1)
    rospy.Subscriber("controller", PyRobot.Controller_Node, callback)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        if commandIA is None:
            if ifNotNone(angle16,angle8,pitch,roll,mag,acc,gyro,temp,volt,sonar,fotocamera):
                if commandolder == "correggi_a_destra" or commandolder == "correggi_a_sinistra" or oldangle is None:
                    oldangle = angle8

                    commandIA = prologIA(commandolder, qrcode, fotocamera, switch, sonar, volt, lidar, angle16, angle8, pitch,roll, mag, acc, gyro, temp, oldangle)
                    print commandIA
                if commandIA == "sinistra" or commandIA == "destra" or commandIA == "indietro":
                    oldangle = None

                commandolder = commandIA
                prolog_msg.risposta = commandIA
                resetNone()
                commandIA = None
                prolog_pub.publish(prolog_msg)
                rospy.loginfo(prolog_msg)
                r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass