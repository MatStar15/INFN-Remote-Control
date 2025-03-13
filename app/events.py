from . import socketio, db, get_socketio
from flask_socketio import SocketIO
import os



@socketio.on('error')
def handle_error(e):
    print(f"Socket error: {e}")
    return {'message': 'Error handling socket event'}


@socketio.on('connect')
def handle_connect():
    print("Socket connected")
    socketio.emit('welcome', {'message': 'Hi! Welcome to the server'})
    return {'message': 'Connected to socket'}


@socketio.on('test')
def handle_connect():
    print("test received from client")
    socketio.emit('test', {'message': 'TEST'})