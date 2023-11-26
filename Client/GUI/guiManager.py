import tkinter as tk
import sys
sys.path.append("./..")

from Lobby.lobbyController import LobbyController
from Register.registerController import RegisterController
from GUI.screensEnum import ScreensEnum
from Lobby.lobbyModel import LobbyModel
from Register.registerModel import RegisterModel
from Lobby.lobbyView import LobbyView
from Login.loginView import LoginView
from Login.loginModel import LoginModel
from Login.loginController import LoginController
from Register.registerView import RegisterView
from Room.roomView import RoomView
from Room.roomModel import RoomModel
from Room.roomController import RoomController
from Sockets.clientSocket import ClientSocketWrapper
from Game.gameView import GameView
from Game.gameModel import GameModel
from Game.gameController import GameController
from NewRoom.createRoomView import CreateRoomView
from NewRoom.createRoomModel import CreateRoomModel
from NewRoom.createRoomController import CreateRoomController

import customtkinter


class GuiManager(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.model = None
        self.view = None
        self.__client_socket = ClientSocketWrapper()
        self.current_screen = ScreensEnum.LOGIN
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
            self.model = RegisterModel()
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