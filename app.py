from app import app, is_production, socketio


import os


# Run app with SocketIO
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ.get('PORT'), debug=False)
