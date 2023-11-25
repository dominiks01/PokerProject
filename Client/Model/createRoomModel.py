import re
import socketio

class CreateRoomModel:
    def __init__(self, socket):
        self.lobby_name = "None"
        self.big_blind_value = "None"
        self.money_value = "None"
        self.max_players_value = "None"
        self.room_status = False
        
        self.socket = socket    
        self._observers = []    
        
        self.call_back()
        
    def create_room(self):
        @self.socket.sio.event
        def create_room_request():
            self.socket.sio.emit(
                'create_room', {
                    'lobby_name': self.lobby_name,
                    'max_players': self.max_players_value,
                    'starting_money': self.money_value, 
                    'big_blind': self.big_blind_value, 
                    'player_id': self.socket._id, 
                    'player_username': self.socket.username
                }, 
                callback=self.join_room_callback)

        create_room_request()
    
    def join_room_callback(self, data):
        if data['status'] == 'success':
            self.room_status = True
            self.notify()
        else:
            raise ValueError(f'Could not create new lobby!')
        
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
        # self.send_lobbies_request()
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
        
    @property
    def lobby_name(self):
        return self.__lobby_name
    
    @lobby_name.setter
    def lobby_name(self, value):
        if value != "":
            self.__lobby_name = value 
        else:
            raise ValueError(f'Invalid Lobby Name: {value}')

    @property
    def big_blind_value(self):
        return self.__big_blind_value
    
    @big_blind_value.setter
    def big_blind_value(self, value):
        if value != "":
            self.__big_blind_value = value 
        else:
            raise ValueError(f'Invalid Big Blind Value: {value}')
    
    @property
    def money_value(self):
        return self.__money_value
    
    @money_value.setter
    def money_value(self, value):
        if value != "":
            self.__money_value = value 
        else:
            raise ValueError(f'Invalid Money Value: {value}')
    
    @property
    def max_players_value(self):
        return self.__max_players_value
    
    @max_players_value.setter
    def max_players_value(self, value):
        if value != "":
            self.__max_players_value = value 
        else:
            raise ValueError(f'Invalid Max Players Value: {value}')