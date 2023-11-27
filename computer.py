from player import Player

class Computer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.__difficulty = None

    def getDifficulty(self):
        return self.__difficulty
    
    def setDifficulty(self, difficulty):
        self.__difficulty = difficulty

    def getName(self):
        return self.__Name
    
    def setName(self, name):
        self.__Name = name


