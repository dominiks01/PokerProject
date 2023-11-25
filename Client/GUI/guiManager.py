import tkinter as tk
import sys
sys.path.append("./..")

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
from View.roomView import RoomView
from Model.roomModel import RoomModel
from Controler.roomController import RoomController
from Sockets.clientSocket import ClientSocketWrapper
from View.gameView import GameView
from Model.gameModel import GameModel
from Controler.gameController import GameController
from View.createRoomView import CreateRoomView
from Model.createRoomModel import CreateRoomModel
from Controler.createRoomController import CreateRoomController

import customtkinter


class GuiManager(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.model = None
        self.view = None
        self.__client_socket = ClientSocketWrapper()
        self.current_screen = ScreensEnum.LOBBIES
        self.title('Tkinter MVC Demo')
        self.load_screen()


    def change_screen(self, screen : ScreensEnum) -> None:
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
            self.controller = LoginController(self.__client_socket, self.model, self.view, self.change_screen)
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
            self.model = LobbyModel(self.__client_socket)
            self.controller = LobbyController(self.model, self.view, self.change_screen)
            self.view.set_controller(self.controller)
            self.model.initialize()

        if self.current_screen == ScreensEnum.ROOM:
            self.view = RoomView(self)
            self.view.grid(row=0, column=0, padx=10, pady=10)
            self.model = RoomModel(self.__client_socket,)
            self.controller = RoomController(self.model, self.view, self.change_screen)
            self.view.set_controller(self.controller)
            self.model.initialize()
            
        if self.current_screen == ScreensEnum.CREATE_ROOM:
            self.view = CreateRoomView(self)
            self.view.grid(row=0, column=0, padx=10, pady=10)
            self.model = CreateRoomModel(self.__client_socket)
            self.controller = CreateRoomController(self.model, self.view, self.change_screen)
            self.view.set_controller(self.controller)
            self.model.initialize()
            
        if self.current_screen == ScreensEnum.GAME:
            self.view = GameView(self)
            self.view.grid(row=0, column=0, padx=10, pady=10)
            self.model = GameModel(self.__client_socket)
            self.controller = GameController(self.model, self.view, self.change_screen)
            self.view.set_controller(self.controller)
            self.model.initialize()