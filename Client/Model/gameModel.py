import re
import socketio

class GameModel:
    def __init__(self, socket):
        self.socket = socket    
        self._observers = [] 
        
        # set up table seats
        self.seats = []
        self.shift = []
        self.nick = []
        self.shifted_players = {}
        
        self.nicknames = {}
        self.all_cards = {}
        
        # Game data from socket server
        self.community_cards = []
        self.actual_player_id = None
        self.stakes_data = None 
        self.pot_value = 0 
        self.raise_value = 0
        self.call_back()
        
    def set_up_table_order():
        pass 

    def callback(self):
        @self.socket.sio.on('game_update')
        def game_update(data):
            print(data)
            # self.game_status = data
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
    