#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX
from empacota import *

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False


    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################

    def sendData(self, data):
        """ Send data over the enlace interface
        """
        package = Empacota(data, "data",1,1).buildPackage()
        self.tx.sendBuffer(package)

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """

        package = self.rx.getHeadPayload()
        data = desempacota(package)
        print(data)

        return(data[0], data[1],(len(data[0])), data[2])

    def sendAck(self):
        #Envia os ACKs para autorizar inicio da conexão ou confirmar recebimentoss
        package = Empacota(None, "ACK",1,1).buildPackage()
        self.tx.sendBuffer(package)

    def sendNack(self):
        #Avisa que pacote chegou corrompido
        package = Empacota(None, "NACK",1,1).buildPackage()
        self.tx.sendBuffer(package)

    def sendSync(self):
        #Para estabelecer conexão
        package = Empacota(None, "sync",1,1).buildPackage()
        self.tx.sendBuffer(package)

    def waitConnection(self): #Papel do Server
        #print("connected", connected)
        #Fica conferindo recebimento do sync e se recebe, confirma enviando ack. Depois envia o sync e confirma se recebeu ack de confirmação.
        while self.connected ==  False:
            print("Loop waitconnection")
            response = self.getData()
            print("Waiting sync...")
            print("response", response)
            if response[3] == "sync":
                print("Sync received")
                self.sendSync()
                time.sleep(0.5)
                self.sendAck()
                print("ACK SENT")
                response = self.getData()
                if response[3] == "ACK":
                    print("Ready to receive package")
                    return True
            else:
                return False

        
    def establishConnection(self): #Papel do Client
        #Envia o Sync para iniciar e pega a resposta. Se tiver Ack (confirmação de recebimento sync), procura pelo recebimento de sync e envia ack. 
        while self.connected ==  False:
            self.sendSync()
            response = self.getData()
            print("Waiting sync...")
            if response[3] == "ACK" or "sync":
                print("Sync received")
                response = self.getData()
                if response[3] == "sync" or "ACK":
                    print("ACK received")
                    time.sleep(0.5)
                    self.sendAck()
                    return True
            else:
                return False                    

    def verifyPackage(self, data):
        package = Package(data).buildPackage()
        sizePack = len(package)
        expected = len(self.getData())
        if sizePack == expected:
            self.sendAck()
            return True
        else:
            self.sendNack()
            return False

    def numberofPackets(self, size):
    	#Inicializar quantidade de pacotes necessário
        total = ((self.size//max_bits)+1)
        return (total)

    