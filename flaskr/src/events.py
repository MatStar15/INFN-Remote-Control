from flask_socketio import SocketIO, emit
socketio = SocketIO()
from src.manager import *


@socketio.on('connected')
def connect(socket_id):
    print("\n" + socket_id + " connected\nCurrently Disabled Feature:" + str(get_disabled_features()) + "\n")

    for feature in get_disabled_features():
        emit('update_disabled', feature, to= socket_id)
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
        update_disabled_features(id)
        emit('update_disabled', id, broadcast= True)
        print('updated ' + id + "\nDisabled features: " + str(disabled_features))


def update_picture(picture):
    emit('update_picture', picture, broadcast=True)


def finished():
    update_picture(test_images[img_index])
    emit('finished', broadcast= True)