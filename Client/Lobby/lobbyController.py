from GUI.screensEnum import ScreensEnum
import time

class LobbyController:
    def __init__(self, socket, model, view, change_scene):
        self.socket = socket
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.sort_by_ = "_id"
        self.order = True        
        
    def initialize(self):
        self.socket.attach(self)
        self.model.lobby = self.socket.send_lobbies_request()['lobbies']
        
    def update(self):
        self.model.lobby = self.socket.lobbies['lobbies']
        self.view.remove_lobby()
        self.view.draw_lobby(self.get_lobbies())
        
    def get_lobbies(self):
        try:
            return sorted(self.model.lobby,  key=lambda x: x[self.sort_by_], reverse=self.order) 

        except ValueError as error:
            self.view.show_error(error)

    def join_lobby(self, value):
        try:
            self.socket.room_id = value
            self.join_room()

        except ValueError as error:
            self.view.show_error(error)

    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.socket.deattach(self)
        self.change_scene(ScreensEnum)

    def join_room(self):
        self.switch_scene(ScreensEnum.ROOM)
        
    def create_lobby(self):
        self.switch_scene(ScreensEnum.CREATE_ROOM)
        
    def log_out(self):
        self.socket.leave_lobby()
        self.switch_scene(ScreensEnum.LOGIN)
        
    def profile(self):
        self.log_out()
        
    def leaderboard(self):
        self.log_out()

    def sort_by(self, value):
        self.order = not self.order if value == self.sort_by_ else True
        self.sort_by_ = value

        self.view.remove_lobby()
        self.view.draw_lobby(self.get_lobbies())
        
        