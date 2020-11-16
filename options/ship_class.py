class Ship:
    def __init__(self,fleet_size = 2):
        self.__fleet_size = fleet_size

    @property
    def fleet_size(self):
        return self.__fleet_size
    
    @fleet_size.setter
    def fleet_size(self, fleet_size):
        self.__fleet_size = fleet_size