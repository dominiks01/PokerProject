from requests import post
from GUI.screensEnum import ScreensEnum

URL = "http://127.0.0.1:5000"

class LoginController:
    def __init__(self, socket, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene
        self.socket = socket

    def save(self, email):
        try:
            self.model.email = email
            self.view.show_success(f'The email {email} saved!')

        except ValueError as error:
            self.view.show_error(error)

    def login(self, email, password):
        try:
            self.model.email = email
            self.model.password = password

            r = post(URL + "/login", data={"userName": self.model.email, "password": self.model.password})
            data = r.json()
            
            if data["status"] == "success":
                print(data)
                self.socket.username = data["user"]["username"]
                self.socket._id = data["user"]["_id"]
                self.switch_scene(ScreensEnum.LOBBIES)
            else:
                raise Exception("Could not Log in")

        except ValueError as error:
            self.view.show_error(error)

    def switch_scene(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)

    def register(self):
        self.switch_scene(ScreensEnum.REGISTER)