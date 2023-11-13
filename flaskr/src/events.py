from flask_socketio import SocketIO, emit
socketio = SocketIO()
from src.manager import *


@socketio.on('connected')
def connect(socket_id):
    print("\n" + socket_id + " connected\n")
    # print("\n Currently disabled features: " + disabled_features + "\n")
    for feature in disabled_features:
        socket_id.emit('update_disabled', feature )
        print('updated ' + feature)

@socketio.on('start')
def start():
    if get_status != 'started':
       set_status('started')
       foo()
       emit('update_disabled', 'start', broadcast=True)


@socketio.on('disabled')
def disabled(id):
    if id not in disabled_features:
        disabled_features.append(id)
        emit('update_disabled', id, broadcast= True)
        print('updated ' + id + "\nDisabled features: " + str(disabled_features))

def update_picture(picture):
    emit('update_picture', picture, broadcast=True)