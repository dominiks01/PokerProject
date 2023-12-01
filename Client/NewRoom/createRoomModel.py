import re
import socketio

class CreateRoomModel:
    def __init__(self):
        self.lobby_name = "None"
        self.big_blind_value = "None"
        self.money_value = "None"
        self.max_players_value = "None"
        self.room_status = False
        
        self._observers = []    
        
        self.call_back()
        
        
    def notify(self):
        '''
            Notify all observers, in this case only controller, 
            that the model was updated
        '''
        for observer in self._observers:
            observer.update()
            
    def attach(self, observer: object):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def deattach(self, observer: object):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
        
    @property
    def lobby_name(self):
        return self.__lobby_name
    
    @lobby_name.setter
    def lobby_name(self, value):
        if value != "":
            self.__lobby_name = value 
        else:
            raise ValueError(f'Invalid Lobby Name: {value}')

    @property
    def big_blind_value(self):
        return self.__big_blind_value
    
    @big_blind_value.setter
    def big_blind_value(self, value):
        if value != "":
            self.__big_blind_value = value 
        else:
            raise ValueError(f'Invalid Big Blind Value: {value}')
    
    @property
    def money_value(self):
        return self.__money_value
    
    @money_value.setter
    def money_value(self, value):
        if value != "":
            self.__money_value = value 
        else:
            raise ValueError(f'Invalid Money Value: {value}')
    
    @property
    def max_players_value(self):
        return self.__max_players_value
    
    @max_players_value.setter
    def max_players_value(self, value):
        if value != "":
            self.__max_players_value = value 
        else:
            raise ValueError(f'Invalid Max Players Value: {value}')