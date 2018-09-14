try:
    import vrep
    import vrepConst
    import numpy
except:
    print('---------------------------')
    print('"vrep.py" could not be imported. This means very probably that')
    print('either "vrep.py or the remoteApi library could not be found')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "vrep.py"')
    print('  ')

import time

print('Program started')


class VREP(object):
    def __init__(self, prossimita, motori):
        '''

        :param prossimita:
        :param motori:
        '''
        global velocityholdSX
        global velocityholdDX
        velocityholdSX = 0
        velocityholdDX = 0
        # creazione liste per sensori e motori
        self.prox = []
        self.mot = []
        # imposto la comunicazione con V-rep
        vrep.simxFinish(-1)
        self.clientID = vrep.simxStart('127.0.0.1', 10000, True, True, 5000, 5)  # Connect to V-REP
        if self.clientID == -1:
            print('Connessione fallita')
        else:
            print('Connesso!')
        kind = "S"
        self.creare(prossimita, kind)
        # print(ris , "=Sensori pronti!!")
        kind = "M"
        self.creare(motori, kind)
        # print(ris, "=Motori pronti!!")

    def creare(self, array, kind):
        '''
        In questa parte di codice viene definito un metodo che ci permette di creare tutti gli handle di
        cui necessitiamo
        :param array:
        :param kind:
        :return:
        '''
        for nomeHandle in array:
            ris, obj = vrep.simxGetObjectHandle(self.clientID, nomeHandle, vrep.simx_opmode_blocking)
            g = (ris, obj)
            if kind == "S":
                ris = self.prox.append(g)
                print("Sensore " + str(nomeHandle) + " pronto.")

            elif kind == "M":
                self.mot.append(g)
                print("Mot. " + str(nomeHandle) + " pronto.")

    def sense(self):
        '''
        implementazione della parte sense del nostro robot
        :return:
        '''
        detectionState = [None, None, None]
        self.detectedPoint = [None, None, None]
        self.detectedObjectHandle = [None, None, None]
        self.detectedSurfaceNormalVector = [None, None, None]
        distance = numpy.array([])
        for i in range(len(self.prox)):
            errorCode, detectionState[i], self.detectedPoint[i], self.detectedObjectHandle[i], \
            self.detectedSurfaceNormalVector[i] = vrep.simxReadProximitySensor(self.clientID, self.prox[i][1],
                                                                               vrep.simx_opmode_blocking)
        if errorCode == 0:
            for i in range(len(detectionState)):
                distance = numpy.append(distance, (self.detectedPoint[i][0] * self.detectedPoint[i][0]) + (
                    self.detectedPoint[i][1] * self.detectedPoint[i][1]) + (
                                            self.detectedPoint[i][2] * self.detectedPoint[i][2]))
            risult = numpy.sqrt(distance)
            #risult= list(risult)
            return risult, detectionState

        else:
            print("Errore")

    def act(self,  dParams):
        '''
        implementazione dell'act per il robot
        :param command: action command to execute
        :param dParams: action parameters
        :return: True is action was actuated
        '''
        assert isinstance(dParams, dict)
        pass
        out = False
        velocitySX = dParams['SX']
        velocityDX = dParams['DX']
        vrep.simxSetJointTargetVelocity(self.clientID, self.mot[0][1], velocitySX, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(self.clientID, self.mot[1][1], velocitySX, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(self.clientID, self.mot[2][1], velocityDX, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(self.clientID, self.mot[3][1], velocityDX, vrep.simx_opmode_blocking)
        out = True
        # if command == 'vai avanti':
        #     velocitySX = dParams['SX']
        #     velocityDX = dParams['DX']
        #     if velocityholdSX != velocitySX:
        #         vrep.simxSetJointTargetVelocity(self.clientID, self.mot[0][1], velocitySX, vrep.simx_opmode_blocking)
        #         vrep.simxSetJointTargetVelocity(self.clientID, self.mot[1][1], velocitySX, vrep.simx_opmode_blocking)
        #         velocityholdSX = velocitySX
        #     elif velocityholdDX != velocityDX:
        #         vrep.simxSetJointTargetVelocity(self.clientID, self.mot[2][1], velocityDX, vrep.simx_opmode_blocking)
        #         vrep.simxSetJointTargetVelocity(self.clientID, self.mot[3][1], velocitySX, vrep.simx_opmode_blocking)
        #         velocityholdDX = velocityDX
        #     out = True
        # if command == 'gira a sinistra' or command == 'gira a destra':
        #     velocitySX = dParams['SX']
        #     velocityDX = dParams['DX']
        #     vrep.simxSetJointTargetVelocity(self.clientID, self.mot[0][1], velocitySX, vrep.simx_opmode_blocking)
        #     vrep.simxSetJointTargetVelocity(self.clientID, self.mot[1][1], velocitySX, vrep.simx_opmode_blocking)
        #     velocityholdSX = velocitySX
        #     vrep.simxSetJointTargetVelocity(self.clientID, self.mot[2][1], velocityDX, vrep.simx_opmode_blocking)
        #     vrep.simxSetJointTargetVelocity(self.clientID, self.mot[3][1], velocitySX, vrep.simx_opmode_blocking)
        #     velocityholdDX = velocityDX
        #     out = True
        #     time.sleep(0.1)
        return out