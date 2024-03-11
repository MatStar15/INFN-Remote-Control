from flaskr import create_app,socketio
from flask_socketio import SocketIO


def main():
    app = create_app()
    
    socketio.run(app, host = '0.0.0.0', debug= True, use_reloader=True, log_output=True) #TODO: Remove debug and use_reloader in production 


if __name__ == '__main__':
    main()