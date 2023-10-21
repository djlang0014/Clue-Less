from flask import Flask, render_template

from flask_socketio import SocketIO

application = Flask(__name__)

socketInstance = SocketIO(application)

@application.route('/')
def test():
    return render_template('index.html')
    # return "<h>Clue-Less Test page.<br>Developed by Creative Engineers.</h>"

@socketInstance.on('connect')
def test_connect():
    socketInstance.emit('after connect', {'data':'Connected to Flask Socket.'})

@socketInstance.on('message')
def handle_message(data):
    print('received message: ' + data)


#run the app
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # application.debug = True
    socketInstance.run(application, debug=True)