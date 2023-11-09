from flask_socketio import SocketIO, emit
socketio = SocketIO()

from src.manager import *

@socketio.on('value changed')
def value_changed(message):
    status[message['who']] = message['data']
    emit('update value',message, broadcast=True)