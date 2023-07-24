class Player:
    def __init__(self, name):
        self.__Name = name
        self.__pieceColour = None

    def getName(self):
        return self.__Name

    def getPieceColour(self):
        return self.__pieceColour
    
    def setPieceColour(self, colour):
        self.__pieceColour = colour

    def setName(self, name):
        self.__Name = name