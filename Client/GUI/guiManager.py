import tkinter as tk

from Controler.lobbyController import LobbyController
from Controler.registerController import RegisterController
from GUI.screensEnum import ScreensEnum
from Model.lobbyModel import LobbyModel
from Model.registerModel import RegisterModel
from View.lobbyView import LobbyView
from View.loginView import LoginView
from Model.loginModel import LoginModel
from Controler.loginController import LoginController
from View.registerView import RegisterView

import customtkinter


class GuiManager(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # self.geometry("800x600")
        self.controller = None
        self.model = None
        self.view = None
        self.current_screen = ScreensEnum.LOGIN
        self.title('Tkinter MVC Demo')

        self.__lobby_id = None
        self.__room_id = None

        self.load_screen()


    def change_screen(self, screen):
        self.current_screen = screen
        self.clear_canvas()
        self.load_screen()

    def clear_canvas(self):
        return

    def load_screen(self):
        if self.current_screen == ScreensEnum.LOGIN:
            self.view = LoginView(self)
            self.view.grid(row=0, column=0, padx=10, pady=10)
            self.model = LoginModel()
            self.controller = LoginController(self.model, self.view, self.change_screen)
            self.view.set_controller(self.controller)

        if self.current_screen == ScreensEnum.REGISTER:
            self.view = RegisterView(self)
            self.view.grid(row=0, column=0, padx=10, pady=10)
            self.model = RegisterModel("dominikszot@gmail.com")
            self.controller = RegisterController(self.model, self.view, self.change_screen)
            self.view.set_controller(self.controller)

        if self.current_screen == ScreensEnum.LOBBIES:
            self.view = LobbyView(self)
            self.view.grid(row=0, column=0, padx=10, pady=10)
            self.model = LobbyModel()
            self.controller = LobbyController(self.model, self.view, self.change_screen)
            self.view.set_controller(self.controller)
            self.controller.initialize()

        if self.current_screen == ScreensEnum.ROOM:
            return