#! /usr/bin/env python
import rospy
from std_msgs.msg import String


def decision(_state):
    '''
    The state contains the worlds representation
    :return: action
    '''
    out = ('(undefined)', {})
    speed = 5
    if _state[0] and _state[1] and _state[2]:
        if _distance[0] < _distance[1]:
            out = ('gira a destra', {'SX': -speed / 2, 'DX': -speed})
        elif _state[0] and _state[1]:
            out = ('gira a destra', {'SX': -speed / 30, 'DX': -speed})
        elif _state[1] and _state[2]:
            out = ('gira a sinistra', {'SX': -speed, 'DX': -speed / 30})
        elif _state[0]:
            out = ('gira a destra', {'SX': -speed / 30, 'DX': -speed})
        elif _state[1] or _state[2]:
            out = ('gira a sinistra', {'SX': -speed, 'DX': -speed / 30})
        else:
            out = ('vai sempre dritto', {'SX': speed, 'DX': speed})
    return out


def callback(data):
    _splitter = data.data.split(",  ")
    _distance = list(map(float, _splitter[0].split("[")[1].split("]")[0].split(" ")))
    _status = list(map(bool, _splitter[1].split("[")[1].split("]")[0].split(" ")))
    _message = [_distance, _status]
    rospy.loginfo(_message)


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("read-sense", String, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()

# TODO:   Dividere data.data in 2 sottostringhe // Salvarsi lo stato precedente
