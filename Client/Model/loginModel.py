import re

class LoginModel:
    def __init__(self):
        self.email = "abcdef@gmail.com"
        self.password = "abc"
        self.user_id = "RedDevil"
        self.username = "RedDevil"

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password
    
    @property
    def user_id(self):
        return self.__user_id

    @property
    def username(self):
        return self.__username

    @email.setter
    def email(self, value):
        # pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # if re.fullmatch(pattern, value):
        if True:
            self.__email = value
        else:
            raise ValueError(f'Invalid email address: {value}')

    @user_id.setter
    def user_id(self, value):
        if value != "":
            self.__user_id = value
        else:
            raise ValueError(f'Empty user_id: ')
    
    @password.setter
    def password(self, value):
        if value != "":
            self.__password = value
        else:
            raise ValueError(f'Empty Password: ')
        
    @username.setter
    def username(self, value):
        if value != "":
            self.__username = value
        else:
            raise ValueError(f'Empty username: ')