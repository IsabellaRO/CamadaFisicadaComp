from construct import *
import binascii

# Class
class Empacota(object):
    #def __init__(self,data):
        #self.data = data
        #self.dataLen= len(data)
    def __init__(self, data, datatype):
        if datatype == "data":
            self.dataType = 0x00
        elif datatype == "sync":
            self.dataType = 0x10
        elif datatype == "ACK":
            self.dataType = 0x11
        elif datatype == "NACK":
            self.dataType = 0x12
        
        self.data = data
        if self.data == None:
            self.dataLen = 0
            self.data = bytearray([])
        else:
            self.dataLen = len(data)


        self.headSTART = 0xFF
        self.headStruct = Struct("start" / Int8ub, "size"  / Int16ub, "type" / Int8ub )
        self.eopSTART = bytearray([0xFF, 0xFC, 0xF4, 0xF7])

    def buildHead(self):
        #Constroi e retorna Head de acordo com as infos inicializadas
        head = self.headStruct.build(dict(start = self.headSTART, size = self.dataLen, type = self.dataType))
        return (head)

#    def buildEOP(self):
#        eop = self.eopStruct.build(dict(start = self.eopSTART))
#        return eop

    def buildPackage(self):
        package = self.buildHead()
        package += self.data
        package += self.eopSTART#()
        return package

#elements=[10,5,0,5,10,10,5,0]

#values= bytearray(elements)

#print(Empacota(values).buildPackage())
    def desempacota(package):
    #Desempacota e confere o tipo, retorna payload, tamanho e tipo (se é payload ou comando).
        head = package[0:3]
        size = int(binascii.hexlify(package[1:3]), 16) 
        data = package[4:] #Head, size e type sao primeiro, data vem a partir do 4
        type_package = package[3:4]

        if type_package == b'\x00':
            type_package = "data"
        elif type_package == b'\x10':
            type_package = "sync"
        elif type_package == b'\x11':
            type_package = "ACK"
        elif type_package == b'\x11':
            type_package = "NACK"
        
        return (data, size, type_package)