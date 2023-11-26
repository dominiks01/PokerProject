from GUI.screensEnum import ScreensEnum
import time

class leaderboardController:
    def __init__(self, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.model.attach(self)

    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)
        
    def log_out(self):
        self.switch_scene(ScreensEnum.LOGIN)
        
    def update(self):
        self.view.clear_view()
        self.view.draw_view(self.get_lobbies())
        