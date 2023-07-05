class BoardPiece:
    '''
        Class: BoardPiece
        Attributes:
            Value: an integer that represents the colour of the piece
        
        Methods:
            getValue
            setValue
    '''
    def __init__(self, value):
        '''
            Initialises the value of the piece
            takes the value as a parameter
        '''
        
        self.__Value = value #black is 1 and white is 2
    
    
    def getValue(self):
        '''
            Method: getValue
            Parameters: None
            Returns: the value of the piece
            
            Does: returns the value of the piece
        '''

        return self.__Value
    
    def setValue(self, value):
        '''
            Method: setValue
            Parameters: value
            Returns: None
            
            Does: sets the value of the piece
        '''
        
        self.__Value = value
