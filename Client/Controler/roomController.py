from GUI.screensEnum import ScreensEnum

class RoomController:
    def __init__(self, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.sort_by_ = 0
        self.order = False
        self.model.attach(self)

    def get_room(self):
        try:
            # x[1][self.sort_by_]
            if self.sort_by_ == 0:
                return self.model.room
            return sorted(self.model.room, key=lambda x: x[self.sort_by_],  reverse=self.order)
        except ValueError as error:
            self.view.show_error(error)

    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)

    def join_room(self):
        self.switch_scene(ScreensEnum.ROOM)

    def join_lobby(self):
        self.model.leave_room()
        self.switch_scene(ScreensEnum.LOBBIES)
        
    def update(self):
        self.view.remove_room()
        self.view.draw_room(self.get_room())
        self.view.owner_view(self.model.owner == self.model.socket._id)
        
    def start_game(self):
        print("SG")
        
    def sort_by(self, value):
        self.order = not self.order if value == self.sort_by_ else self.order
        self.sort_by_ = value

        for row in self.view.room_treeview.get_children():
            self.view.room_treeview.delete(row)

        self.view.draw_room(self.get_room())