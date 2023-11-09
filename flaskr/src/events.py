from flask_socketio import SocketIO, emit
socketio = SocketIO()
import machineScripts as ms
from src.manager import *




# @socketio.on('value changed')
# def value_changed(message):
#     test_value[message['who']] = message['data']
#     emit('update value',message, broadcast=True)


@socketio.on('start')
def start():
    status = 'start'
    # print('starting')
    ms.CustomSystem()
    emit('stared', broadcast=True)
    emit('update_disabled', 'start', broadcast=True)


@socketio.on('disabled')
def disabled(id):
    disabled_features.append(id)
    emit('update_disabled', id, broadcast= True)
    print('updated ' + id)