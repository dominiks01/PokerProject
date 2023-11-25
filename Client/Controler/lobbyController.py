from GUI.screensEnum import ScreensEnum
import time

class LobbyController:
    def __init__(self, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.sort_by_ = 0
        self.order = True
        self.model.attach(self)
        
    def get_lobbies(self):
        try:
            if self.sort_by_ == 0:
                return sorted(self.model.lobby.items(), reverse=self.order)
            return sorted(self.model.lobby.items(), key=lambda x: x[1][self.sort_by_],  reverse=self.order)
        except ValueError as error:
            self.view.show_error(error)

    def join_lobby(self, value):
        try:
            self.model.join_room(value)
            self.join_room()

        except ValueError as error:
            self.view.show_error(error)

    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)

    def join_room(self):
        self.switch_scene(ScreensEnum.ROOM)
        
    def create_lobby(self):
        self.switch_scene(ScreensEnum.CREATE_ROOM)

    def sort_by(self, value):
        self.order = not self.order if value == self.sort_by_ else self.order
        self.sort_by_ = value

        self.view.remove_lobby()
        self.view.draw_lobby(self.get_lobbies())
        
    def update(self):
        self.view.remove_lobby()
        self.view.draw_lobby(self.get_lobbies())
        