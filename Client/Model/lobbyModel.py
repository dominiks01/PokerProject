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
    def __init__(self, socket):
        self.lobby = {}
        self.socket = socket    
        self._observers = []    
        
        self.call_back()


    def call_back(self):
        @self.socket.sio.on('lobby_update')
        def lobby_update(data):
            '''
                There was some update in database in lobbies. 
            '''
            print("lobbySocket.on('lobby_update')")
            self.lobby = data['lobbies']
            self.notify()
            
    def initialize(self):
        '''
            Send request for actual lobbies to display
        '''
        self.send_lobbies_request()
        self.notify()
        
    def notify(self):
        '''
            Notify all observers, in this case only controller, 
            that the model was updated
        '''
        for observer in self._observers:
            observer.update()
            
    def attach(self, observer: object):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def deattach(self, observer: object):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
        
    def send_lobbies_request(self):
        print(f"LC.send_lobbies_request()")

        @self.socket.sio.event
        def send_lobbies_request_socket():
            self.socket.sio.emit('join_lobby', callback=self.set_lobbies_callback)

        send_lobbies_request_socket()
        
    def set_lobbies_callback(self, data):
        print(data)
        self.lobby = data['lobbies']
        self.notify()   
    
    def join_room(self, value):
        self.socket.room_id = value
    
    @property
    def lobby(self):
        return self.__lobby

    @lobby.setter
    def lobby(self, value):
        if True:
            self.__lobby = value
        else:
            raise ValueError(f'Cannot get lobbies: ')
