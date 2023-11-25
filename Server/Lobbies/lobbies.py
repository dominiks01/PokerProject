from credits import cluster
from pymongo import MongoClient
import random

class Lobby:
    def __init__(self):
        self.client = MongoClient(cluster)
        self.db = self.client["PokerProject"]
        self.lobbies_ = self.db["lobbies"]
        
    def get_lobbies(self):
        result = list(self.lobbies_.find())
        
        for docs in result:
            docs["_id"] = str(docs["_id"])
                
        print(result)
        return result
    
    def remove_from_room(self):
        return
    
    def add_to_room(self, room_id: str, 
                    username: str, 
                    player_id: str, 
                    ready:bool = False):
        pass
        
        # self.lobbies_[room_id]['players'].append({
        #     'username': username,
        #     'player_id': player_id,
        #     'ready': ready     
        # })
        
    def create_room(self, data):
        lobby_id = self.lobbies_.insert_one({
            'players'           :[{
                'username': data['player_username'], 
                'ready': True,
                'player_id': data['player_id']}],
            'max_players'        : data['max_players'],
            'starting_money'     : data['starting_money'],
            'lobby_name'         : data['lobby_name'],
            'owner'              : data['player_username'],
            'big_blind'          : data['big_blind']
        }).inserted_id
                
        return lobby_id
        
    def remove_from_room(self, room_id: str, player_id : str):
        self.lobbies_[room_id]['players'] = [player for player in self.lobbies_[room_id]['players'] if not player['player_id'] == player_id]

    def get_room(self, lobby_id: str):
        return self.lobbies_[lobby_id]
    