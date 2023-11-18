
class Lobby:
    def __init__(self):
        self.lobbies_ = {
            '1': {
                'players': [
                    {
                        'username': 'test',
                        'playerId': '1',
                        'ready': True
                    },
                    {
                        'username': 'test2',
                        'playerId': '2',
                        'ready': True
                    }
                ],
                'maxPlayers': 4,
                'startingMoney': 1000,
                'bigBlind': 10,
                'lobbyName': 'LobbyWith2Players',
                'owner': 0
            },
            '2': {
                'players': [
                    {
                        'username': 'test',
                        'playerId': '3',
                        'ready': True
                    },
                    {
                        'username': 'test2',
                        'playerId': '4',
                        'ready': True
                    },
                    {
                        'username': 'test3',
                        'playerId': '5',
                        'ready': True
                    }
                ],
                'maxPlayers': 4,
                'startingMoney': 1000,
                'bigBlind': 10,
                'lobbyName': 'LobbyWith3Players',
                'owner': 0
            },
            '3': {
                'players': [
                    {
                        'username': 'test',
                        'playerId': '6',
                        'ready': True
                    }
                ],
                'maxPlayers': '6',
                'startingMoney': 1000,
                'bigBlind': 10,
                'lobbyName': 'LobbyWith1Player',
                'owner': 0
            }
        }
