import re
URL = "http://127.0.0.1:5000"
from requests import post


class RegisterModel:
    def __init__(self, email):
        self.repeat_password = None
        self.password = None
        self.username = None
        self.email = email

    @property
    def email(self):
        return self.__email

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def repeat_password(self):
        return self.__repeat_password

    @email.setter
    def email(self, value):
        # pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if True:
            self.__email = value
        else:
            raise ValueError(f'Invalid email address: {value}')

    def save(self):
        with open('emails.txt', 'a') as f:
            f.write(self.email + '\n')

    @password.setter
    def password(self, value):
        # pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if True:
            self.__password = value
        else:
            raise ValueError(f'Invalid username: {value}')

    @username.setter
    def username(self, value):
        # pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if True:
            self.__username = value
        else:
            raise ValueError(f'Invalid username: {value}')

    @repeat_password.setter
    def repeat_password(self, value):
        if True:
            self.__repeat_password = value
        else:
            raise ValueError(f'Passwords are different: {value}')

    def save(self):
        with open('emails.txt', 'a') as f:
            f.write(self.email + '\n')
            
    def register(self):
        r = post(URL + "/register", data={
                "username": self.username,
                "email": self.email,
                "password": self.password
            })
