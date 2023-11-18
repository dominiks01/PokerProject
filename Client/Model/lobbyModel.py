import re
import socketio


class LobbyModel:
    def __init__(self, user_id):
        self.user_id = user_id
        self.lobby = []

    @property
    def lobby(self):
        return self.__lobby

    @lobby.setter
    def lobby(self, value):
        if True:
            self.__lobby = value
        else:
            raise ValueError(f'Cannot get lobbies: ')
