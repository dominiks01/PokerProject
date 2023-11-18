import re


class LobbyModel:
    def __init__(self):
        self.lobby_id = None
        self.lobby = [
             (2, 'Aaryan', 'Pune', 18),
             (3, 'Vaishnavi', 'Mumbai', 20),
             (4, 'Rachna', 'Mumbai', 21),
             (5, 'Shubham', 'Delhi', 21)]

    @property
    def lobby_id(self):
        return self.__lobby_id

    @property
    def lobby(self):
        return self.__lobby

    @lobby.setter
    def lobby(self, value):
        if True:
            self.__lobby = value
        else:
            raise ValueError(f'Cannot get lobbies: ')

    @lobby_id.setter
    def lobby_id(self, value):
        if True:
            print(f"Joined lobby {value}")
            self.__lobby_id = value
        else:
            raise ValueError(f'Cannot join lobby: ')
