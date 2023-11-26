from credits import cluster
from pymongo import MongoClient
import random
from bson.objectid import ObjectId

class Lobby:
    def __init__(self):
        self.client = MongoClient(cluster)
        self.db = self.client["PokerProject"]
        self.lobbies_ = self.db["lobbies"]
        
    def get_lobbies(self):
        result = list(self.lobbies_.find())
        
        for docs in result:
            docs["_id"] = str(docs["_id"])
                
        return result
    
    def remove_from_room(self):
        return
    
    def change_ready(self, data):
        result = list(self.lobbies_.find({'_id': ObjectId(str(data["room_id"]))}))[0]['players']
        
        for dict_element in result:
            if dict_element["player_id"] == data["player_id"]:
                dict_element["ready"] = not bool(dict_element["ready"])
                
        self.lobbies_.update_one(
            {'_id': ObjectId(str(data["room_id"]))}, 
            { "$set": {
                "players" : result
            }}
        )
        

    def add_to_room(
        self,
        room_id: str, 
        username: str, 
        player_id: str, 
        ready:bool = False):
        
        result = list(self.lobbies_.find({'_id': ObjectId(str(room_id))}))[0]['players']
        
        player_ = {
            'username': username, 
            'ready': ready, 
            'player_id': player_id
        }
        
        if player_ in result:
            print("Player Already in lobby!")
            return
        
        self.lobbies_.update_one({
            '_id': ObjectId(str(room_id))}, 
            {'$push': { "players": player_}
        })
        
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
        result = list(self.lobbies_.find({'_id': ObjectId(str(lobby_id))}))
        result[0]["_id"] = str(result[0]["_id"])
                
        return result[0]
    