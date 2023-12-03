#I think this will be the driver function for the actual gameplay portion. 
#The lobby will be taken care of prior to this
import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import psycopg
from gameinfo import *
from gamelogic import *
import threading

# Init the server
application = Flask(__name__)
socketio = SocketIO(application, logger=True)
global gameOver
gameOver = False

# Send HTML!
@application.route('/')
def root():    
    return render_template('main_menu.html')

@application.route('/play')
def play():
    return render_template('play.html')

@application.route('/rules')
def rules():
    return render_template('rules.html')

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/skeletal-tests')
def skeletal_tests():
    return render_template('skeletal-tests.html')

@application.route('/testzone')
def test_zone():
    global locationList
    global ballroom
    global billiard_room
    global Kitchen
    global caseFile
    caseFile = CaseFile("Mrs. Peacock", "Knife", "Ballroom")
    Kitchen = Location("Kitchen", "Room", 0, ["Hall10", "Hall12", "Study"])
    billiard_room = Location("Billiard Room", "Room", 1, ["Hall4", "Hall6", "Hall7", "Hall9"])
    ballroom = Location("Ballroom", "Room", 2, ["Hall9", "Hall11", "Hall12"])
    locationList = [Kitchen, billiard_room, ballroom]
    global testPlayer
    testPlayer = Player("Test Player", 1)
    testPlayer.selectCharacter("Miss Scarlet")
    global testInstance
    testInstance = GameInstance(1, [testPlayer])
    testInstance.findAvailableLocations(1, billiard_room)
    print(testInstance.getPlayerLocation(1).locName)
    global game_thread
    game_thread = threading.Thread(target=playgame, args=(testInstance, socketio, application, gameOver))
    game_thread.start()
    return render_template('testzone.html')

@socketio.on('connect')
def test_connect():
    socketio.emit('after connect', {'data':'Connected to Flask Socket.'})

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@application.route('/accusesubmit', methods = ['POST'])
def accusesubmit():
    print(f"{request.form['Weapon']}, {request.form['Character']}, {request.form['Location']}")
    caseWeapon = caseFile.weapon
    caseSuspect = caseFile.suspect
    caseRoom = caseFile.room
    accuseWeapon = request.form['Weapon']
    accuseSuspect = request.form['Character']
    accuseRoom = request.form['Location']

    if accuseWeapon == caseWeapon and accuseSuspect == caseSuspect and accuseRoom == caseRoom:
        print("Game Over!")
    else:
        return "0"
    
    return "1"

@application.route('/movesubmit', methods = ['POST'])
def movesubmit():
    newLocation = request.form['Location']
    for location in locationList:
        if location.locName == newLocation:
            testInstance.findAvailableLocations(1, location)
    return "1"

@application.route('/suggestsubmit', methods = ['POST'])
def suggestsubmit():
    print(f"{request.form['Weapon']}, {request.form['Character']}")
    return "1"

def playgame(gameInstance, socket, app, gameOver):
    print("here")
    
    
    testInstance.findAvailableLocations(1, ballroom)
    print(testInstance.getPlayerLocation(1).locName)

    while not gameOver:
        print(testInstance.getPlayerLocation(1).locName, gameOver)
        time.sleep(5)
        pass
    
    print("Game Over!")


# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """    
    socketio.run(application, port=8000, debug=True)
