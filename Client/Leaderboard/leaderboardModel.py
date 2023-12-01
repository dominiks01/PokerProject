import re
import socketio


class LeaderboardModel:
    def __init__(self):
        self._observers = []    
        
        self.call_back()
            
    def initialize(self):
        '''
            Send request for actual lobbies to display
        '''
        self.notify()
        
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