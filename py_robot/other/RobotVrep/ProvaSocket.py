import socket
import pickle
import numpy
from numpy.core.defchararray import strip


def conn():
    host_server = "localhost"
    port_server = 50021
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host_server, port_server))
    return client

def main():
    con = conn()
    count = 0
    a=1
    h=[]
    while a:
        c = con.recv(1024).decode()
        con.send(b'a')

        #print(c)
        #print(type(c))
        #print(c[0], c[1])
        # a=str(c[0])
        # b=str(c[1])
        # d=a+ ",  " +b
        d= c.split(",  ")
        print(d)


        #f=tyt[8:50]
        #print(tyt)
      #  h=tyt.split( "(", 2)



     #   _distance=h[1].split(")", 1)
      #  _state=_distance[0].split("],", 1)
        #print(_state[1])
        #print(_distance[0])





        count = count + 1
        if count > 20:
            con.close()
            a = 0

main()
