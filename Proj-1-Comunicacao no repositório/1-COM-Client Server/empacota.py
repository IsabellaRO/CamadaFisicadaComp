from construct import *

# Class
class Empacota(object):
    def __init__(self,data):
        self.data = data
        self.dataLen= len(data)
        self.headSTART = 0xFF
        self.headStruct = Struct("start" / Int8ub,"size" / Int16ub)
        self.eopSTART = 0xFFFCF4F7
        self.eopStruct = Struct("start" / Int32ub)

    def buildHead(self):
        head = self.headStruct.build(dict(start = self.headSTART, size = self.dataLen))
        return (head)

    def buildEOP(self):
        eop = self.eopStruct.build(dict(start = self.eopSTART))
        return eop

    def buildPackage(self):
        package = self.buildHead()
        package += self.data
        package += self.buildEOP()
        return package

elements=[10,5,0,5,10,10,5,0]

values= bytearray(elements)

print(Empacota(values).buildPackage())
