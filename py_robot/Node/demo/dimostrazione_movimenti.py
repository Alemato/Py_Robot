#! /usr/bin/python
import rospy
import py_robot.msg as PyRobot
import time

controller_to_motor_msg = PyRobot.Controller_To_Motor_Node()


def main():
    # lista comandi da impartire al  nodo Motor_Switch_Node
    comando = ["a", "b", "c", "d", "e", "f", "g", "h", "g", "f", "e", "d", "c", "b", "a", "t", "d", "a", "b", "c", "d",
               "e", "f", "g", "h", "g", "f", "e", "d", "c", "b", "a"]

    # lista dei tempi di funzionamento rispettivi per ogni comando
    tempi = [5, 2, 3, 4]
    indice = 0
    rospy.init_node("Controller_Node", disable_signals=True)
    controller_to_motor_pub = rospy.Publisher("controller_To_Motor", PyRobot.Controller_To_Motor_Node, queue_size=1)
    time.sleep(2)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        if indice < 4:  # da settare in base agli indici della lista
            controller_to_motor_msg.velo = comando[
                indice]  # Scrittura del comando preso dalla lista comando con indice progressivo
            rospy.loginfo(controller_to_motor_msg)
            controller_to_motor_pub.publish(controller_to_motor_msg)  # pub nel topic
            time.sleep(tempi[indice])  # tempo di attesa preso nella lista tempi con indice progressivo
            indice = indice + 1
        else:
            controller_to_motor_msg.velo = "s"  # comando di stop dopo la fine della lista per fine dimostrazione
            controller_to_motor_pub.publish(controller_to_motor_msg)  # pub stop nel topic
            time.sleep(1)
            rospy.signal_shutdown('Dimostrazione Terminata')  # spegnimento nodo
            print("Dimostrazione Terminata")
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
