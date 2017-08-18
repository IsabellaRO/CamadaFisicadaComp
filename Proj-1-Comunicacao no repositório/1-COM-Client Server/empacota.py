# Class
class Empacota(object):
    def __init__(self)
    self.headSTART = 0xFF
    self.headStruct = Struct("start" / Int8ub,"size" / Int16ub)

    def buildHead(self, dataLen):
        head = headStruct.build(dict(start = self.headSTART, size = dataLen))
        return (head)
