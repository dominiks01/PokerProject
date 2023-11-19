from GUI.screensEnum import ScreensEnum
import time

class LobbyController:
    def __init__(self, socket, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene

        self.sort_by_ = 0
        self.order = True
        
        self.socket = socket        

    def initialize(self):
        # self.socket.send_lobbies_request()
        self.send_lobbies_request()
        self.view.draw_lobby(self.get_lobbies())    
        
    def send_lobbies_request(self):
        print(f"LC.send_lobbies_request()")

        @self.socket.sio.event
        def send_lobbies_request_socket():
            self.socket.sio.emit('join_lobby', callback=self.set_lobbies_callback)

        send_lobbies_request_socket()
        
    def set_lobbies_callback(self, data):
        self.model.lobby = data['lobbies']
        self.view.draw_lobby(self.get_lobbies())    
        
    def get_lobbies(self):
        try:
            # print(self.model.lobby)
            # print(sorted(self.model.lobby, reverse=self.order))
            # return sorted(self.model.lobby, reverse=self.order)
            return self.model.lobby
        except ValueError as error:
            self.view.show_error(error)

    def join_lobby(self, value):
        try:
            self.model.lobby_id = value
            self.socket.room_id = value
            self.join_room()

        except ValueError as error:
            self.view.show_error(error)

    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)

    def join_room(self):
        self.switch_scene(ScreensEnum.ROOM)

    def sort_by(self, value):
        self.order = not self.order if value == self.sort_by_ else self.order
        self.sort_by_ = value

        for row in self.view.lobby_treeview.get_children():
            self.view.lobby_treeview.delete(row)

        self.view.draw_lobby(self.get_lobbies())
