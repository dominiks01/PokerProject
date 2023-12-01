from GUI.screensEnum import ScreensEnum
import time

class CreateRoomController:
    def __init__(self, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.model.attach(self)
        
    def create_room(self, lobby_name, big_blind_value, money_value, max_players_value):
        try:
            self.model.lobby_name = lobby_name
            self.model.big_blind_value = big_blind_value 
            self.model.money_value = money_value
            self.model.max_players_value = max_players_value
            
            self.socket.create_room(
                {
                    "lobby_name": self.model.lobby_name, 
                    "max_players": self.model.max_players_value, 
                    "big_blind": self.model.big_blind_value, 
                    "starting_money": self.model.money_value
                }
            )
        
        except ValueError as error:
            self.view.show_error(error)
        
    def cancel(self):
        self.switch_scene(ScreensEnum.LOBBIES)
        
    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)
        
    def update(self):
        if self.model.room_status:
            self.switch_scene(ScreensEnum.ROOM)
    
    def make_move(self, move_id, stake):
        pass 
    
    def quit_game(self):
        # self.model.quit_game()
        self.switch_scene(ScreensEnum.LOBBIES)
        