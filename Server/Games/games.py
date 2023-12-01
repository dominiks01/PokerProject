
from pokerGame import PokerGame
import random

history = {}

class Game: 
    def __init__(self):
        self.games = {}
        self.games_lobbies = {}

    def pass_data(self, data):
        user_id = data['user_id']
        game_id = data['game_id']
        game_data = {}
        if game_id is None:
            game_id = self.games_lobbies[data['room_id']]

        try:
            game_data = self.games[game_id].get_data()
            game_data['cards'] = self.games[game_id].tables.players[user_id].get_cards()
        except KeyError:
            print(f"[ERROR] no such key")

        game_data['game_id'] = game_id

        return game_data


    def player_left_game(self, data):
        print(f"self.Games.player_left_game()")
        self.games[data['game_id']].player_left_table(data['playerId'])
        game_data = self.games[data['game_id']].get_data()

        if self.games[data['game_id']].winner is not None:
            players_cards = {}

            for uuid, player in self.games[data['game_id']].tables.players.items():
                if uuid in game_data['players_at_table']:
                    players_cards[uuid] = player.get_cards()

            game_data['all_cards'] = players_cards
            game_data['owner'] = self.games[data['game_id']].owner
            self.save_game_result(data['game_id'])

        return game_data


    def create_new_game(self, data):
        print(f"self.Games.create_new_game()")
        hash = random.getrandbits(128)
        self.games[hash] = PokerGame()
        return hash


    def update_data(self, data):
        print('self.Games.update_data()')

        if self.games[data['gameId']].player_index != data['playerId']:
            return

        self.games[data['gameId']].calculate_move(data['playerId'], data['move_id'], data['raise_bet'])
        game_data = self.games[data['gameId']].get_data()
        game_data['gameId'] = data['gameId']
        
        if self.games[data['gameId']].winner is not None:
            players_cards = {}

            for uuid, player in self.games[data['gameId']].tables.players.items():
                if uuid in game_data['players_at_table']:
                    players_cards[uuid] = player.get_cards()

            game_data['all_cards'] = players_cards
            game_data['owner'] = self.games[data['gameId']].owner
            self.save_game_result(data['gameId'])

        return game_data


    def save_game_result(self, game_id):
        print(f"self.Games.end_game()")
        history[game_id] = self.games[game_id]


    def start_game(self, game_id, data, room_id):
        print(f"self.Games.start_game()")
        self.games_lobbies[room_id] = game_id
        self.games[game_id].config(data)
        self.games[game_id].start()


    def play_next_round(self, data, config):
        print(f"self.Games.play_next_round()")
        self.games[data['game_id']].config(config)
        self.games[data['game_id']].start()

