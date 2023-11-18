from GUI.screensEnum import ScreensEnum

class LobbyController:
    def __init__(self, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene

    def join_lobby(self, lobby_id):
        try:
            self.model.lobby_id = lobby_id

        except ValueError as error:
            self.view.show_error(error)

    def initialize(self):
        self.view.draw_lobby(self.get_lobbies())

    def get_lobbies(self):
        try:
            return self.model.lobby
        except ValueError as error:
            self.view.show_error(error)

    def join_lobby(self, value):
        try:
            self.model.lobby_id = value
            self.lobby

        except ValueError as error:
            self.view.show_error(error)

    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)

    def join_room(self):
        self.switch_scene(ScreensEnum.ROOM)