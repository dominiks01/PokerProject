from GUI.screensEnum import ScreensEnum

class RoomController:
    def __init__(self, socket, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.sort_by_ = "player_id"
        self.order = False
        self.socket = socket
                
    def get_room(self):
        try:
            return sorted(self.model.room, key=lambda x: x[self.sort_by_],  reverse=self.order)
        except ValueError as error:
            self.view.show_error(error)
            
    def initialize(self):
        self.socket.attach(self)
        self.socket.send_room_request()        

    def switch_scene(self, ScreensEnum):
        self.socket.deattach(self)
        self.view.delete()
        self.change_scene(ScreensEnum)

    def join_lobby(self):
        self.socket.leave_room()
        self.switch_scene(ScreensEnum.LOBBIES)
        
    def update(self):
        self.model.room = self.socket.room
        self.view.draw_room(self.get_room())
        self.view.owner_view(True)
        
    def start_game(self):
        self.socket.create_live_game()
        self.switch_scene(ScreensEnum.GAME)
        
    def change_state(self):
        self.socket.change_ready_state()
        
    def sort_by(self, value):
        self.order = not self.order if value == self.sort_by_ else self.order
        self.sort_by_ = value

        self.view.draw_room(self.get_room())