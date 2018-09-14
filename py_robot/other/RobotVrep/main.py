import System
import ast
import paho.mqtt.client as mqtt
import threading


class myThread(threading.Thread):
    def __init__(self, threadID, client):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client = client


    def run(self):
        send(self.client)

def send( client):
    while True:
        sensor = world.sense()
        client.publish("topic/sense", str(sensor[0]) + ",  " + str(sensor[1]))

def on_message(client1, userdata, msg):
    print("message received ", str(msg.payload.decode("utf-8")))
    action = str(msg.payload.decode("utf-8")).split("(")[1].split(")")[0].split(", ", 1)
    action1 = ast.literal_eval(action[1])
    print(action[0])
    print(world.act(action1))

world = System.VREP(["Proximity_sensorSX", "Proximity_sensorCE", "Proximity_sensorDX"], ["Motore_Pos_SX","Motore_Ant_SX","Motore_Pos_DX", "Motore_Ant_DX"])
print(world.sense())
print("---------------")
client = mqtt.Client()
client.connect("localhost", 1883, 60)
thread1 = myThread(1,  client)
thread1.start()
client1 = mqtt.Client()
client1.connect("localhost", 1883, 60)
client1.subscribe("topic/act")
client1.on_message = on_message
client1.loop_forever()

# HOST = 'localhost'                 # Nome che rappresenta il nodo locale
# PORT = 50046                       # Porta non privilegiata arbitraria
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(2)
# while True:
#     con, addr = s.accept()

# con[0].send(str.encode(str(sensor[0]) +",  "+ str(sensor[1] )))
# action = con[1].recv(1024).split("(")[1].split(")")[0].split(", ", 1)
# socket.send(str.encode(str(sensor[0]) + ",  " + str(sensor[1])))
# action = socket.recv(1024).split("(")[1].split(")")[0].split(", ", 1)
# action1 = ast.literal_eval(action[1])
#  print(action[0])
# print(world.act(action1))
# if not action:
#     break




