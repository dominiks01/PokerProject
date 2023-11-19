import socketio

class LobbySocketWrapper:
    sio = socketio.Client()

    def __init__(self):
        self.call_backs()
        self.message_from_server = ""
        self.setup()
        
        self._id = ""
        self.username = ""
        self.room_id = ""
        
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
        self.sio.disconnect()
        
    def send_lobbies_request(self):
        print(f"lobbySocket.send_lobbies_request()")

        @self.sio.event
        def send_lobbies_request_socket():
            self.sio.emit('join_lobby', callback=self.set_lobbies_callback)

        send_lobbies_request_socket()
        
    def set_room_data(self, data):
        print(f"LobbySocket.set_room_data()")
        # self.room = data['room']
        # self.new_data = True

    def set_room_callback(self, data):
        print(f"LobbySocket.set_room_callback()")
        # self.room = data['room']
        # self.new_data = True

    def set_lobbies_callback(self, data):
        print(f"LobbySocket.set_lobbies_callback()")
        print(data)
        self.lobbies = data
        

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
        def game_handler():
            print('lobbySocket.room_game_start')
            # self.is_game = True

    # ROOM MANAGEMENT
    def join_room_callback(self, data):
        print("lobbySocket.join_room_callback")
        # if data['status'] == 'success':
        #     self.roomId = data['roomId']
        #     self.room = data['room']
        # else:
        #     print(f"[ERROR] JOIN ROOM FAILED!")
        # self.new_data = True

    def join_room(self, data):
        print(f"lobbySocket.join_room()")

        # @self.sio.event
        # def join_room_socket():
        #     self.sio.emit('join_room', {
        #         'playerId': data['playerId'],
        #         'roomId': data['roomId'],
        #         'playerName': data['playerName']
        #     }, callback=self.join_room_callback)

        # join_room_socket()

    def create_room(self, data):
        print(f"lobbySocket.create_room")

        # @self.sio.event
        # def create_room_socket():
        #     self.sio.emit('create_room', data,
        #                   callback=self.join_room_callback)

        # create_room_socket()

    def leave_room(self):
        print(f"lobbySocket.leave_room")

        # @self.sio.event
        # def leave_room_socket():
        #     self.sio.emit('leave_room', {'playerId': self.user_id, 'roomId': self.roomId})

        # leave_room_socket()

        # self.new_data = True
        # self.roomId = None
        # self.room = None

    # LOBBY MANAGEMENT
    def leave_lobby(self):
        print(f"lobbySocket.leave_lobby()")

        # @self.sio.event
        # def leave_lobby_socket():
        #     self.sio.emit('leave_lobby', {
        #         'playerId': self.user_id,
        #         'lobbyId': self.roomId})

        # self.roomId = None
        # leave_lobby_socket()

    def start_game(self):
        print(f"lobbySocket.start_game()")

        # @self.sio.event
        # def room_start_game():
        #     self.sio.emit('room_start_game', {'playerId': self.user_id, 'roomId': self.roomId, 'gameId': self.game_id})

        # room_start_game()

    def set_game_data(self, data):
        print("lobbySocket.on('set_game_data')")

        # if 'game_id' in data:
        #     self.game_id = data['game_id']
        #     self.start_game()

        # elif 'content' in data:
        #     print(f"[ERROR] {data['content']}")
        #     self.message_from_server = data['content']

    def create_live_game(self):
        print(f"lobbySocket.create_live_game()")

        # @self.sio.event
        # def new_game():
        #     self.sio.emit('create_live_game', {'room_id': self.roomId, 'player_id': self.user_id}, callback=self.set_game_data)

        # new_game()

    def change_ready_state(self):
        print(f"lobbySocket.create_live_game()")

        # @self.sio.event
        # def change_ready_state_socket():
        #     self.sio.emit('room_change_ready',
        #                   {'playerId': self.user_id, 'roomId': self.roomId}, callback=self.set_room_callback)

        # change_ready_state_socket()
        # # self.loop()