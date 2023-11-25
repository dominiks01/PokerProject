
from pokerGame import PokerGame
import random

games = {}
games_lobbies = {}
history = {}

class Game: 
    def __init__(self):
        self._games = games

    def pass_data(self, data):
        user_id = data['user_id']
        game_id = data['game_id']
        game_data = {}
        if game_id is None:
            game_id = games_lobbies[data['room_id']]

        try:
            game_data = games[game_id].get_data()
            game_data['cards'] = games[game_id].tables.players[user_id].get_cards()
        except KeyError:
            print(f"[ERROR] no such key")

        game_data['game_id'] = game_id

        return game_data


    def player_left_game(self, data):
        print(f"Games.player_left_game()")
        games[data['game_id']].player_left_table(data['playerId'])
        game_data = games[data['game_id']].get_data()

        if games[data['game_id']].winner is not None:
            players_cards = {}

            for uuid, player in games[data['game_id']].tables.players.items():
                if uuid in game_data['players_at_table']:
                    players_cards[uuid] = player.get_cards()

            game_data['all_cards'] = players_cards
            game_data['owner'] = games[data['game_id']].owner
            self.save_game_result(data['game_id'])

        return game_data


    def create_new_game(self, data):
        print(f"Games.create_new_game()")
        hash = random.getrandbits(128)
        games[hash] = PokerGame()
        return hash


    def update_data(self, data):
        print('Games.update_data()')

        if games[data['gameId']].player_index != data['playerId']:
            return

        games[data['gameId']].calculate_move(data['playerId'], data['move_id'], data['raise_bet'])
        game_data = games[data['gameId']].get_data()
        game_data['gameId'] = data['gameId']
        
        if games[data['gameId']].winner is not None:
            players_cards = {}

            for uuid, player in games[data['gameId']].tables.players.items():
                if uuid in game_data['players_at_table']:
                    players_cards[uuid] = player.get_cards()

            game_data['all_cards'] = players_cards
            game_data['owner'] = games[data['gameId']].owner
            self.save_game_result(data['gameId'])

        return game_data


    def save_game_result(self, game_id):
        print(f"Games.end_game()")
        history[game_id] = games[game_id]


    def start_game(self, game_id, data, room_id):
        print(f"Games.start_game()")
        games_lobbies[room_id] = game_id
        games[game_id].config(data)
        games[game_id].start()


    def play_next_round(self, data, config):
        print(f"Games.play_next_round()")
        games[data['game_id']].config(config)
        games[data['game_id']].start()

