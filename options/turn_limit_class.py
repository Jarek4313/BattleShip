class Turn:
    def __init__(self,turn_limit = 25):
        self.__turn_limit = turn_limit

    @property
    def turn_limit(self):
        return self.__turn_limit
    
    @turn_limit.setter
    def turn_limit(self, turn_limit):
        self.__turn_limit = turn_limit