from requests import post

from GUI.screensEnum import ScreensEnum
URL = "http://127.0.0.1:5000"


class RegisterController:
    def __init__(self, model, view, change_scene):
        self.model = model
        self.view = view
        self.change_scene = change_scene

    def save(self, email):
        try:
            self.model.email = email
            self.view.show_success(f'The email {email} saved!')

        except ValueError as error:
            self.view.show_error(error)

    def login(self):
        self.switch_screen(ScreensEnum.LOGIN)

    def register(self, username, email, password, repeat_password):
        try:
            self.model.username = username
            self.model.email = email
            self.model.password = password
            self.model.repeat_password = repeat_password

            r = post(URL + "/register", data={
                "username": self.model.username,
                "email": self.model.email,
                "password": self.model.password
            })

            self.login()

        except ValueError as error:
            self.view.show_error(error)

    def switch_screen(self, ScreensEnum):
        self.view.delete()
        self.change_scene(ScreensEnum)
