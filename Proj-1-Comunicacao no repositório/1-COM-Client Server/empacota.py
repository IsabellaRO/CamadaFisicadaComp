from construct import *
import binascii


def desempacota(package):
    #Desempacota e confere o tipo, retorna payload, tamanho e tipo (se e payload ou comando).
    size = int(binascii.hexlify(package[1:3]), 16) 
    print(size)
    type_package = package[3:4]
    print(type_package)
    number_of_packages = int(binascii.hexlify(package[4:6]), 16) 
    package_index = int(binascii.hexlify(package[6:7]), 8) 
    max_bits = int(binascii.hexlify(package[8:9]), 8)
    if type_package == b'\x00':
        type_package = "data"
    elif type_package == b'\x10':
        type_package = "sync"
    elif type_package == b'\x11':
        type_package = "ACK"
    elif type_package == b'\x12':
        type_package = "NACK"
    payload=package[8:]
    return (payload, size, type_package, number_of_packages, package_index, max_bits)


# Class
class Empacota(object):
    #def __init__(self,data):
        #self.data = data
        #self.dataLen= len(data)
    def __init__(self, data, datatype, number_of_packages, package_index):
        if datatype == "data":
            self.dataType = 0x00
        elif datatype == "sync":
            self.dataType = 0x10
        elif datatype == "ACK":
            self.dataType = 0x11
        elif datatype == "NACK":
            self.dataType = 0x12
        
        self.max_bits = 2048

        self.data = data
        if self.data == None:
            self.dataLen = 0
            self.data = bytearray([])
        else:
            self.dataLen = len(data)


        self.headSTART = 0xFF
        self.package_index = package_index
        self.number_of_packages = number_of_packages
        self.headStruct = Struct("start" / Int8ub, "size"  / Int16ub, "type" / Int8ub, "number_of_packages" / Int16ub, "package_index" / Int8ub, "max_bits" / Int8ub )
        self.eopSTART = bytearray([0xFF, 0xFC, 0xF4, 0xF7])

    def buildHead(self):
        #Constroi e retorna Head de acordo com as infos inicializadas
        head = self.headStruct.build(dict(start = self.headSTART, size = self.dataLen, type = self.dataType, number_of_packages = self.number_of_packages, package_index = self.package_index, max_bits = self.max_bits))
        return (head)

    def buildPackage(self):
        package = self.buildHead()
        package += self.data
        package += self.eopSTART#()
        print(package)
        return package

#elements=[10,5,0,5,10,10,5,0]

#values= bytearray(elements)

#print(Empacota(values).buildPackage())
