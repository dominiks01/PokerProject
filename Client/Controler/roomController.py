from GUI.screensEnum import ScreensEnum

class RoomController:
    def __init__(self, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.sort_by_ = 0
        self.order = False

    def join_room(self, lobby_id):
        try:
            self.model.room_id = lobby_id

        except ValueError as error:
            self.view.show_error(error)

    def initialize(self):
        self.view.draw_room()

    def get_room(self):
        try:
            return sorted(self.model.room, key=lambda x: x[self.sort_by_], reverse=self.order)
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