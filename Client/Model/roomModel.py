import re

class RoomModel:
    def __init__(self, socket):
        self.socket = socket
        self.room = {}
        self.owner = None
        self._observers = []
        self.callback()

    def callback(self):
        @self.socket.sio.on('room_update')
        def room_update(data):
            self.room = data['room']['players']
            self.owner = data['room']['owner']
            self.notify()

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
    
    def initialize(self):
        self.send_room_request()
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
        
    def send_room_request(self):
        print(f"RC.send_room_request()")

        @self.socket.sio.event
        def send_room_request_socket():
            
            self.socket.sio.emit('join_room', {
                'player_id': self.socket._id,
                'room_id': self.socket.room_id, 
                'username': self.socket.username, 
                }, callback=self.set_room_callback)

        send_room_request_socket()
        
    def leave_room(self):
        print(f"RC.leave_room()")

        @self.socket.sio.event
        def leave_room_request():
            
            self.socket.sio.emit('leave_room', {
                'player_id': self.socket._id,
                'room_id': self.socket.room_id, 
                })
        leave_room_request()

        
    def set_room_callback(self, data):
        if data['status'] == "success":
            self.notify()
        else:
            self.join_lobby()
        # self.view.draw_lobby(self.get_lobbies()) 