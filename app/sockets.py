# app/sockets.py
from flask_socketio import emit
from . import socketio

@socketio.on('send_message')
def handle_send_message(data):
    """Handle sending a message"""
    emit('receive_message', data, broadcast=True)

@socketio.on('join_room')
def handle_join_room(data):
    """Handle user joining a room"""
    username = data['username']
    room = data['room']
    join_room(room)
    emit('user_joined', {'username': username, 'room': room}, room=room)