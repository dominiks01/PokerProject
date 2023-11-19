import re
import socketio

'''
    Lobby template:
    'lobby_id': {
        'players': [
            {
                'username': str,
                'player_id': int,
                'ready': bool
            }
        ],
        'max_players': int,
        'starting_money': int,
        'big_blind': int,
        'lobby_name': str,
        'owner': int
    },'
'''


class LobbyModel:
    def __init__(self, user_id):
        self.user_id = user_id
        self.lobby = {}

    @property
    def lobby(self):
        return self.__lobby

    @lobby.setter
    def lobby(self, value):
        if True:
            self.__lobby = value
        else:
            raise ValueError(f'Cannot get lobbies: ')
