#! /usr/bin/env python
import rospy
from std_msgs.msg import String
import numpy as np


global _oldmessage
_oldmessage = ''
def decision(_message):
    '''
    The state contains the worlds representation
    :return: action

    la logica da implementare:
    abbiamo 3 sensori che misurano 3 distanze

    V0  V1  V2    gli 1 sono le distanze piu grandi tra le tre
    1   0   0
    0   1   0
    0   0   1

    per ora escudo tutti i casi in cui ci sono sensori con la stessa distanza

    abbiamo anche 3 stati che generano:

    V0  V1  V2
    1   1   1          gli 1 sono i true
    1   1   0
    1   0   1
    1   0   0
    0   1   1
    0   1   0
    0   0   1
    0   0   0

    mi salvo la retromarcia se ce stata, cosi escudo di andare dritto
    R

    quindi se ce stata posso andare solo a dx o sx
    '''
    out = ('(undefined)', {})
    speed = -2  # velocita massima del rover
    distance = 1  # la distanza a cui il rover inizia a cercare una via di uscita
    distance_min = 0.8
    dietro = False
    _state = _message[1]
    _distance = _message[0]
    rospy.loginfo(str(type(_distance)))
    if _state[0] and _state[1] and _state[2]:  # caso 1 1 1
        if _distance[0] < distance_min or _distance[1] < distance_min or _distance[0] < distance_min: #caso contro il muro
            out = ('vai dietro', {'SX': -speed, 'DX': -speed})
            dietro = True
        elif _distance[0] < distance or _distance[1] < distance or _distance[2] < distance:
            if _distance[0] > _distance[1]:
                if _distance[0] > _distance[2]:  # caso 1 0 0
                    out = ('gira a sinistra', {'SX': -speed / 30, 'DX': speed})
                    dietro = False
                else:  # caso 0 0 1
                    out = ('gira a destra', {'SX': speed, 'DX': -speed / 30})
                    dietro = False
            elif _distance[1] > _distance[2]:
                if _distance[1] > _distance[0]:  # caso 0 1 0
                    out = ('vai sempre dritto caso 0 1 0', {'SX': speed, 'DX': speed})
                    dietro = False
                else:  # caso 1 0 0
                    out = ('gira a sinistra', {'SX': speed / 30, 'DX': speed})
                    dietro = False
            elif _distance[2] > _distance[1]:
                if _distance[2] > _distance[0]:  # caso 0 0 1
                    out = ('gira a destra', {'SX': speed, 'DX': speed / 30})
                    dietro = False
                else:  # caso 1 0 0
                    out = ('gira a sinistra', {'SX': speed/30, 'DX': speed})
                    dietro = False
        else:
            if not dietro:
                out = ('vai sempre dritto not indietro', {'SX': speed, 'DX': speed})
                dietro = False
            else:
                out = ('vai dietro', {'SX': -speed, 'DX': -speed})
                dietro = True
    elif _state[0] and _state[1] and not _state[2]:  # caso 1 1 0
        if _distance[0] < distance or _distance[1] < distance or _distance[2] < distance:
            out = ('gira a destra', {'SX': -speed, 'DX': -speed / 30})
            dietro = False
        else:
            out = ('vai sempre dritto caso 1 1 0ss', {'SX': speed, 'DX': speed})
            dietro = False
    # elif _state[0] and not _state[1] and _state[2]:                                 #caso 1 0 1
    #     out = ('vai sempre dritto', {'SX': speed, 'DX': speed})
    # elif _state[0] and not _state[1] and not _state[2]:                             #caso 1 0 0
    #     out = ('vai sempre dritto', {'SX': speed, 'DX': speed})
    elif not _state[0] and _state[1] and _state[2]:  # caso 0 1 1
        if _distance[0] < distance or _distance[1] < distance or _distance[2] < distance:
            out = ('gira a sinistra', {'SX': speed / 30, 'DX': speed})
            dietro = False
        else:
            out = ('vai sempre dritto 0 1 1', {'SX': speed, 'DX': speed})
            dietro = False

    elif not _state[0] and _state[1] and not _state[2]:  # caso 0 1 0
        if _distance[0] < distance or _distance[1] < distance or _distance[2] < distance:
            out = ('gira a destra', {'SX': speed, 'DX': speed / 30})
            dietro = False
        else:
            out = ('vai sempre dritto 0 1 0 e', {'SX': speed, 'DX': speed})
            dietro = False
    #         out = ('vai sempre dritto', {'SX': speed, 'DX': speed})
    # elif not _state[0] and not _state[1] and _state[2]:                             #caso 0 0 1
    #     out = ('vai sempre dritto', {'SX': speed, 'DX': speed})
    # elif not _state[0] and not _state[1] and not _state[2]:                         #caso 0 0 0
    #     out = ('vai sempre dritto', {'SX': speed, 'DX': speed})
    else:
        out = ('vai sempre dritto qui', {'SX': speed, 'DX': speed})
        # caso 1 0 1
        # caso 1 0 0
        # caso 0 0 1
        # caso 0 0 0

    return str(out)


def callback(data):
    global _oldmessage
    _splitter = data.data.split(",  ")
    _distance = np.array(_splitter[0].split("[")[1].split("]")[0].split("  ")).astype(np.float)
    _status = map(bool, _splitter[1].split("[")[1].split("]")[0].split(" "))
    _message = [_distance, _status]

    pub = rospy.Publisher('thinkNode', String)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo(_message)
        datasend = decision(_message)
        rospy.loginfo(datasend)
        pub.publish(datasend)
        rate.sleep()


def listener():
    rospy.init_node('think', anonymous=True)
    rospy.Subscriber("read-sense", String, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()

