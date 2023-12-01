import socketio

class ClientSocketWrapper:
    sio = socketio.Client()

    def __init__(self):
        self.message_from_server = ""
        self.setup()
        self._id = ""
        self.username = ""
        self.room_id = ""
        self.lobbies = ""
        self.room = ""
        self.owner = ""
        self.game_id = ""
        self.new_update = False
        self.cards = None
        self.winner = False
        self.new_game = False
        self.game_status = None
        self._observers = []    
    
    def notify(self):
        '''
            Notify observers about new update
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
        
    # Setup Connection
    def setup(self):
        print(f"LobbySocket.setup()")
        try:
            self.sio.connect('http://127.0.0.1:5500')
        except Exception as ex:
            print("Failed to establish initial connection to server:", type(ex).__name__)
        self.call_backs()
        
    def run(self):
        print(f"LobbySocket.run()")
        # self.setup()

    def loop(self):
        self.sio.wait()
    
    def disconnect(self):
        print("disconnecting!")
        if self.room_id is not None:
            self.leave_room()
        
        self.sio.disconnect()

        
    '''
        Join loobby and get all lobbies details
    '''
    def send_lobbies_request(self):
        print(f"lobbySocket.send_lobbies_request()")

        @self.sio.event
        def send_lobbies_request_socket():
            self.sio.emit('join_lobby', callback=self.set_lobbies_callback)

        send_lobbies_request_socket()
        
    def set_lobbies_callback(self, data):
        self.lobbies = data
        self.notify()
            
    '''
        Join selected room and get room details from server
    '''
    def send_room_request(self):
        print(f"RC.send_room_request()")

        @self.sio.event
        def send_room_request_socket():
            self.sio.emit('join_room', {
                'player_id': self._id,
                'room_id': self.room_id, 
                'username': self.username, 
                }, callback=self.set_room_callback)

        send_room_request_socket()
        
    def set_room_callback(self, data):
        if data['status'] == "success":
            self.room = data['room']['players']
        self.notify()
        
    '''
        Leave room
    '''
    def leave_room(self):
        @self.sio.event
        def leave_room_request():
            
            self.sio.emit('leave_room', {
                'player_id': self._id,
                'room_id': self.room_id, 
                }, callback=self.leave_room_callback)
        leave_room_request()
        
    def leave_room_callback(self, data):
        if data['status'] == "success":
            self.room_id = None
            self.room = None
        self.notify()
        
        
    def set_room_data(self, data):
        print(f"LobbySocket.set_room_data()")
        # self.room = data['room']
        # self.new_data = True

    def call_backs(self):
        @self.sio.on('lobby_update')
        def lobby_update(data):
            print("lobbySocket.on('lobby_update')")
            # self.lobbies = data['lobbies']
            # self.new_data = True
            # # self.set_lobbies_callback(data)

        @self.sio.on('room_update')
        def room_update(data):
            print("lobbySocket.on('room_update')")
            # self.room = data['room']
            # self.new_data = True
            # pass

        @self.sio.on('game_created')
        def room_update(data):
            print("lobbySocket.on('game_created')")
            # self.game_id = data['game_id']

        @self.sio.on('room_game_start')
        def game_handler(data):
            print('lobbySocket.room_game_start')
            # self.is_game = True


    def create_room(self, data):
        print(f"lobbySocket.create_room")

        @self.sio.event
        def create_room_socket():
            self.sio.emit(
                'create_room', 
                  data.update(
                      {
                          "player_username": self.username, 
                          "player_id":self._id, 
                      }
                  ),
                callback=self.join_room_callback)

        create_room_socket()

    # LOBBY MANAGEMENT
    def leave_lobby(self):
        print(f"lobbySocket.leave_lobby()")

        @self.sio.event
        def leave_lobby_socket():
            self.sio.emit('leave_lobby', {
                'player_id': self._id,
                'room_id': self.room_id
            })

        self.roomId = None
        leave_lobby_socket()

    def start_game(self):
        print(f"lobbySocket.start_game()")
        
        @self.sio.event
        def room_start_game():
            self.sio.emit(
                'room_start_game', {
                    'player_id': self._id,
                    'room_id': self.room_id,
                    'game_id': self.game_id
                })

        room_start_game()

    def set_game_data(self, data):
        print("lobbySocket.on('set_game_data')")

        if 'game_id' in data:
            self.game_id = data['game_id']
            self.start_game()

        elif 'content' in data:
            print(f"[ERROR] {data['content']}")
            self.message_from_server = data['content']

    def create_live_game(self):
        print(f"lobbySocket.create_live_game()")

        @self.sio.event
        def new_game():
            self.sio.emit(
                'create_live_game', {
                    'room_id': self.room_id, 
                    'player_id': self._id
                }, callback=self.set_game_data)

        new_game()

    def change_ready_state(self):
        print(f"lobbySocket.create_live_game()")

        @self.sio.event
        def change_ready_state_socket():
            self.sio.emit(
                'room_change_ready',{
                    'player_id': self._id, 
                    'room_id': self.room_id
                 }, callback=self.set_room_callback)

        change_ready_state_socket()
        # self.loop()

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