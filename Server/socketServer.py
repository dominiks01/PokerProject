import socketio
import eventlet
import sys

from Lobbies.lobbies import Lobby
from Games.games import Game

sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)
lobby = Lobby()
game = Game()

@sio.event
def connect(sid, environ):
    print(sid, 'connected    ')


@sio.event
def disconnect(sid):
    print(sid, 'disconnected')
    

@sio.on('join_lobby')
def join_lobby(sid):
    print(f"SocketServer.join_lobby()")
    sio.enter_room(sid, 'lobby')
    return {'lobbies': lobby.get_lobbies()}


@sio.on('leave_game')
def leave_game(sid, data):
    print("SocketServer.leave_game()")
    game_data = game.player_left_game(data)

    game.leave_room(data)
    sio.leave_room(sid, data['game_id'])
    sio.leave_room(sid, data['room_id'])

    if game_data['winner'] is not None:
        sio.emit('finish_game', game_data, room=data['game_id'])

    sio.emit('game_update', game_data, room= data['game_id'])
    sio.emit('lobby_update', {'lobbies':lobby.get_lobbies()}, room='lobby')


@sio.on('leave_lobby')
def leave_lobby(sid, data):
    print("SocketServer.leave_lobby()")
    sio.leave_room(sid, 'lobby')
    sio.emit('lobby_update', {'lobbies': lobby.get_lobbies()}, room='lobby')


# Room Management
@sio.on('create_room')
def create_room(sid, data):
    print("socketServer.create_room()")
    sio.leave_room(sid, 'lobby')

    room_id = lobby.create_room(data)

    sio.enter_room(sid, str(room_id))
    sio.enter_room(sid, data['player_id'])

    sio.emit('lobby_update', {'lobbies': lobby.get_lobbies()}, room='lobby')
    print(list(lobby.get_lobbies())) 
    
    return {
        'status': 'success', 
        'room_id': room_id, 
        'room': lobby.get_lobbies()}


@sio.on('leave_room')
def leave_room(sid, data):
    print("socketServer.leave_room()")
    sio.leave_room(sid, data['room_id'])
    sio.leave_room(sid, data['player_id'])

    lobby.leave_room(data)

    sio.enter_room(sid, 'lobby')
    sio.emit('lobby_update', {'lobbies': lobby.get_lobbies()}, room='lobby')


@sio.on('room_change_ready')
def room_change_ready(sid, data):
    print(f"SocketServer.room_change_ready()")
    lobby.change_ready(data)

    sio.emit('room_update', {'room': lobby.get_room(data['room_id'])}, room=data['room_id'])
    sio.emit('lobby_update', {'lobbies': lobby.get_lobbies()}, room='lobby')

    return { 'status': "success", 'room': lobby.get_room(data['room_id'])}

@sio.on('join_room')
def join_room(sid, data):
    print(f"SocketServer.join_room()")
    sio.enter_room(sid, data['room_id'])
    sio.leave_room(sid, 'lobby')
    
    lobby.add_to_room(
        data['room_id'],
        data['username'],
        data['player_id'],
        False
    )
    
    sio.emit('lobby_update', {'lobbies': lobby.get_lobbies()}, room='lobby')
    sio.emit('room_update', {'room': lobby.get_room(data['room_id'])}, room=data['room_id'])

    return {'status': 'success', 'room_id': data['room_id'], 'room':lobby.get_room(data['room_id'])}

@sio.on('leave_room')
def leave_room(sid, data):
    print(f"SocketServer.leave_room()")
    sio.leave_room(sid, data['room_id'])
    sio.enter_room(sid, 'lobby')
    
    lobby.remove_from_room(
        data['room_id'],
        data['player_id'],
    )
    
    sio.emit('lobby_update', {'lobbies': lobby.get_lobbies()}, room='lobby')
    sio.emit('room_update', {'room': lobby.get_room(data['room_id'])}, room=data['room_id'])
    
    return {'status': "success"}


# Game Management
@sio.on('create_live_game')
def create_live_game(sid, data):
    print("socketServer.create_live_game()")

    # for player in lobby.get_lobbies()[data['room_id']]['players']:
    #     if player['ready'] is False:
    #         return {'content': 'Players not ready!'}

    hash = game.create_new_game(data)
    sio.emit('game_created', {'game_id': hash}, room=data['room_id'])
    return {'game_id': hash}


@sio.on('game_move_played')
def update_data(sid, data):
    print("socketServer.game_move_played()")
    game_data = game.update_data(data)

    if game_data['winner'] is not None:
        sio.emit('finish_game', game_data, room = data['gameId'])

    sio.emit('game_update', game_data, room=data['gameId'])
    return game_data


@sio.on('room_start_game')
def room_start_game(sid, data):
    print(f"SocketServer.room_start_game()", data)
    if True:
        game.games_lobbies[data['room_id']] = data['game_id']
        game.start_game(data['game_id'], lobby.get_room(data['room_id']), data['room_id'])

        sio.emit('room_game_start', {'content': 'The game has started!'}, room=data['room_id'])
        sio.emit('next_round', room=data['game_id'])
        sio.emit('lobby_update', { 'lobbies':lobby.get_lobbies()}, room='lobby')

# Info
@sio.on('set_data')
def get_connection(sid, data):
    print(f"SocketServer.set_data()")
    # if data['player_id'] not in sio.rooms(sid):
    #     sio.enter_room(sid, str(data['player_id']))

    # sio.emit('room_update', {'room': Lobbies.lobbies[data['roomId']]}, room=data['roomId'])

@sio.on('data_request')
def data_request(sid, data):
    print(f"SocketServer.data_request()")
    # games_config = Games.pass_data(data)    
    # if games_config is None:
    #     return None
    
    # sio.enter_room(sid, games_config['game_id'])

    # return games_config


@sio.on('start_round')
def start_next_round(sid, data):
    print(f"SocketServer.start_round()")
    game.play_next_round(data, lobby.get_lobbies()[data['room_id']])
    sio.emit('next_round', room=data['game_id'])
    sio.emit('room_game_start', {'content': 'The game has started!'}, room=data['room_id'])


eventlet.wsgi.server(eventlet.listen(('', 5500)), app)
