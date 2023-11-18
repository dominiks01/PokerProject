import re


class LoginModel:
    def __init__(self):
        self.email = "abcdef@gmail.com"
        self.password = "abc"

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    @email.setter
    def email(self, value):
        # pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # if re.fullmatch(pattern, value):
        if True:
            self.__email = value
        else:
            raise ValueError(f'Invalid email address: {value}')

    @password.setter
    def password(self, value):
        if value != "":
            self.__password = value
        else:
            raise ValueError(f'Empty Password: ')

    def save(self):
        with open('emails.txt', 'a') as f:
            f.write(self.email + '\n')