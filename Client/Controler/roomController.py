from GUI.screensEnum import ScreensEnum

class RoomController:
    def __init__(self, socket, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.sort_by_ = 0
        self.order = False
        self.socket = socket

    def initialize(self):
        self.send_room_request()
        self.view.draw_room(self.get_room())
        
    def send_room_request(self):
        print(f"RC.send_room_request()")

        @self.socket.sio.event
        def send_room_request_socket():
            
            self.socket.sio.emit('join_room', {
                'player_id': self.socket._id,
                'room_id': self.socket.room_id, 
                'player_name': self.socket.username, 
                }, callback=self.set_room_callback)

        send_room_request_socket()
        
    def set_room_callback(self, data):
        if data['status'] == "success":
            self.model.room = data['room']['players']
            self.view.draw_room(self.get_room())    
        else:
            self.join_lobby()
        # self.view.draw_lobby(self.get_lobbies()) 

    def get_room(self):
        try:
            return self.model.room
        except ValueError as error:
            self.view.show_error(error)

    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)

    def join_room(self):
        self.switch_scene(ScreensEnum.ROOM)

    def join_lobby(self):
        self.switch_scene(ScreensEnum.LOBBIES)

    def sort_by(self, value):
        self.order = not self.order if value == self.sort_by_ else self.order
        self.sort_by_ = value

        for row in self.view.room_treeview.get_children():
            self.view.room_treeview.delete(row)

        self.view.draw_room()