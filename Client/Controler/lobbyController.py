from GUI.screensEnum import ScreensEnum


class LobbyController:
    def __init__(self, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene

        self.sort_by_ = 0
        self.order = True

    def initialize(self):
        self.view.draw_lobby()

    def get_lobbies(self):
        try:
            return sorted(self.model.lobby, key=lambda x: x[self.sort_by_], reverse=self.order)
        except ValueError as error:
            self.view.show_error(error)

    def join_lobby(self, value):
        try:
            self.model.lobby_id = value
            self.join_room()

        except ValueError as error:
            self.view.show_error(error)

    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)

    def join_room(self):
        self.switch_scene(ScreensEnum.ROOM)

    def sort_by(self, value):
        if self.sort_by_ == value:
            self.order = not self.order
        else:
            self.sort_by_ = value
            self.order = False

        for row in self.view.lobby_treeview.get_children():
            self.view.lobby_treeview.delete(row)

        self.view.draw_lobby()
