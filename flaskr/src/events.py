from flask_socketio import SocketIO, emit
socketio = SocketIO()


def finished(img_index):
    # print('Image Index in Finished: ' + str(img_index))
    update_picture(test_images[img_index])
    emit('finished', broadcast= True)

from src.manager import *

@socketio.on('connected')
def connect(socket_id):
    print("\n" + socket_id + " connected\nCurrently Disabled Feature:" + str(get_disabled_features()) + "\n")
    for feature in get_disabled_features():
        if feature != '':
            emit('update_disabled', feature, to= socket_id)
            print('updated ' + feature)


@socketio.on('start')
def start():
    if get_status != 'started':
       set_status('started')
       emit('update_disabled', 'start', broadcast=True)
       foo()
       

@socketio.on('disabled')
def disabled(id):
    print('disable: ' + id)
    if id not in disabled_features and not '':
        update_disabled_features(id)
        emit('update_disabled', id, broadcast= True)
        print('updated ' + id + "\nDisabled features: " + str(disabled_features))


def update_picture(picture):
    emit('update_picture', picture, broadcast=True)
