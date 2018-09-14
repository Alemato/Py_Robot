import serial
import serial.tools.list_ports


class Mondo(object):

    def __init__(self, val):
        self.val = val
        self.p = serial.tools.list_ports.comports()
        self.comunication = []

    def com(self):
        for i in range(self.p.__len__()):
            self.comunication.append(serial.Serial(self.p[i][0], 115200))
            print('Comunicazione avvenuta')
        return self.comunication

    def scrivi(self, com):
        for i in com:
            i.write('a'.encode('ascii'))
