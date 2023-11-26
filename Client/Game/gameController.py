from GUI.screensEnum import ScreensEnum
import time

class GameController:
    def __init__(self, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.model.attach(self)
        
    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)
        
    def update(self):
        pass
    
    def make_move(self, move_id, stake):
        pass 
    
    def quit_game(self):
        # self.model.quit_game()
        self.switch_scene(ScreensEnum.LOBBIES)
        