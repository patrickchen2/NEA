class BoardPiece:
    def __init__(self, value):
        self.__Value = value #black is 1 and white is 2
    
    
    def getValue(self):
        return self.__Value
    
    def setValue(self, value):
        self.__Value = value
