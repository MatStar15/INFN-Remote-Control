from flaskr import create_app,socketio
from flask_socketio import SocketIO


def main():
    app = create_app()
    socketio.run(app, host = '0.0.0.0', debug= False)


if __name__ == '__main__':
    main()