import socketio

class GameSocketWrapper:
    sio = socketio.Client()
    def __init__(self, user_id, game_id, room_id):
        self.setup()
        self.user_id    = user_id
        self.game_id    = game_id
        self.new_update = False
        self.cards = None
        self.winner = False
        self.new_game = False
        self.game_status = None
        self.room_id =  room_id
        
        self.owner  = None
        self._observers = []    


    def setup(self):
        print("gameSocket.setup()")
        try:
            self.sio.connect('http://127.0.0.1:5500')
        except Exception as ex:
            print("Failed to establish initial connection to server:", type(ex).__name__)

        self.call_backs(data=None)

    def disconnect(self):
        self.sio.disconnect()

    def set_data(self, data):
        self.game_status = data
        self.new_update = True

        if self.cards is None:
            self.cards = self.game_status['cards']

    def leave_game(self):
        print(f"leave_game")

        @self.sio.event
        def leave_lobby_socket():
            self.sio.emit(
                'leave_game', {
                    'player_id': self.user_id,
                    'game_id': self.game_id,
                    'roomId': self.room_id
                })

        leave_lobby_socket()

    def set_game_data(self, data):
        print('set_game_data()')
        self.room_id = data['game']['roomId']
        self.room = data['game']

    def call_backs(self, data=None):
        print("XD")
        @self.sio.on('room_update')
        def game_update(data):
            print("gameSocket.on('room_update')")
            self.game_status = data
            self.new_update = True
            print(data)

        @self.sio.on('finish_game')
        def game_update(data):
            print("gameSocket.on('finish_game')")
            self.winner = True
            self.game_status = data
            self.new_update = True
            self.owner = data['owner']
            
        @self.sio.on('start_game')
        def game_status():
            print("gameSocket.on('start_game')")

        @self.sio.on('next_round')
        def start_next_round(data=None):
            print("SNR")
            self.winner = None
            self.cards = None
            self.new_update = True
            self.new_game = True

        @self.sio.on('game_update')
        def game_update(data):
            print("gameSocket.on('game_update')", data)

            if self.game_id is None:
                self.game_id = data['gameId']
            
            self.new_update = True
            self.game_status = data

        @self.sio.on('game_created')
        def game_created(data):
            self.game_status = data

            @self.sio.event
            def start_game():
                self.sio.emit('room_start_game', {
                    'roomId': self.room_id,
                    'gameId': self.game_id
                }),

            start_game()

    def move_played(self, data):
        @self.sio.event
        def game_move_played():
            print( {'playerId': self.user_id, 'gameId': self.game_id, 'move_id': data['move_id'], 'raise_bet': data['raise_bet']})
            self.sio.emit(
                'game_move_played',
                {
                    'player_id': self.user_id, 
                    'game_id': self.game_id, 
                    'move_id': data['move_id'],
                    'raise_bet': data['raise_bet']
                },
                callback=self.set_data),

        game_move_played()

    def room_start_game(self):
        @self.sio.event
        def room_start_game():
            self.sio.emit('room_start_game', {'player_id':self.user_id, 'game_id': self.game_id, 'room_id': self.room_id})
        room_start_game()

    def run(self):
        print("gameSocket.run()")
        self.setup()

    def notify(self):
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