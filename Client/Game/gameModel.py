import re
import socketio

class GameModel:
    def __init__(self):
                
        # set up table seats
        self.seats = []
        self.shift = []
        self.nick = []
        self.shifted_players = {}
        
        self.nicknames = {}
        self.all_cards = {}
        
        # Game data from socket server
        self.community_cards = []
        self.actual_player_id = None
        self.stakes_data = None 
        self.pot_value = 0 
        self.raise_value = 0
        
    def set_up_table_order():
        pass 