from flask_socketio import emit, join_room, leave_room
from . import socketio

@socketio.on('connect')
def handle_connect():
    emit('connection_response', {'data': 'Connected'})

@socketio.on('join_room')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('room_announcement', f'A user has joined the room: {room}', to=room)

@socketio.on('send_message')
def handle_send_message(data):
    room = data.get('room')
    message = data.get('message')
    emit('message', {'room': room, 'message': message}, to=room)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')