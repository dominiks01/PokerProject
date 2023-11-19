lobbies_ = {
    '1': {
        'players': [
            {
                'username': 'test',
                'player_id': '1',
                'ready': True
            },
            {
                'username': 'test2',
                'player_id': '2',
                'ready': True
            }
        ],
        'max_players': '4',
        'starting_money': 1000,
        'big_blind': 10,
        'lobby_name': 'LobbyWith2Players',
        'owner': 0
    },
    '2': {
        'players': [
            {
                'username': 'test',
                'player_id': '3',
                'ready': True
            },
            {
                'username': 'test2',
                'player_id': '4',
                'ready': True
            },
            {
                'username': 'test3',
                'player_id': '5',
                'ready': True
            }
        ],
        'max_players': '4',
        'starting_money': 1000,
        'big_blind': 10,
        'lobby_name': 'LobbyWith3Players',
        'owner': 0
    },
    '3': {
        'players': [
            {
                'username': 'test',
                'player_id': '6',
                'ready': True
            }
        ],
        'max_players': '6',
        'starting_money': 1000,
        'big_blind': 10,
        'lobby_name': 'LobbyWith1Player',
        'owner': 0
    }
}

class Lobby:
    def __init__(self):
        self.lobbies_ = lobbies_
        
    def get_lobbies(self):
        return self.lobbies_
    
    def add_to_room(self, room_id: str, 
                    username: str, 
                    player_id: str, 
                    ready:bool = False):
        
        self.lobbies_[room_id]['players'].append({
            'username': username,
            'player_id': player_id,
            'ready': ready     
        })
        
    def remove_from_room(self, room_id: str, player_id : str):
        self.lobbies_[room_id]['players'] = [player for player in self.lobbies_[room_id]['players'] if not player['player_id'] == player_id]

    def get_room(self, lobby_id: str):
        return self.lobbies_[lobby_id]
    