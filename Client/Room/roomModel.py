import re

class RoomModel:
    def __init__(self):
        self.room = {}
        self.owner = None
        self._observers = []

    @property
    def room_id(self):
        return self.__room_id

    @property
    def room(self):
        return self.__room

    @room.setter
    def room(self, value):
        if True:
            self.__room = value
        else:
            raise ValueError(f'Cannot get lobbies: ')

    @room_id.setter
    def room_id(self, value):
        if True:
            self.__room_id = value
        else:
            raise ValueError(f'Cannot join lobby: ')
        
    def start_game_callback(self, data):
        pass 