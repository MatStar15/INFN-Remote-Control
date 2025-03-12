from app import create_app, socketio

app = create_app(config_name='Development')

if __name__ == '__main__':
    socketio.run(app,
                 debug=True,
                 host='0.0.0.0',
                 port=5000,
                 use_reloader=True,
                 use_debugger=True,
                 # transports=['websocket'],
                 # websocket = True,
                 log_output=True
             )
