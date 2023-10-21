# File originally downloaded from https://github.com/josharnoldjosh/simple-flask-socketio-example
# on 10/21/23.  Has been modified by Creative Engineers for the Clue-Less project.

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Init the server
application = Flask(__name__)
application.config['SECRET_KEY'] = 'some super secret key!'
socketio = SocketIO(application, logger=True)

# Send HTML!
@application.route('/')
def root():    
    return render_template('index.html')

# Receive a message from the front end HTML
@socketio.on('send_message')   
def message_recieved(data):
    print(data['text'])
    socketio.emit('message_from_server', {'text':'Message recieved!'})

####################################################
# Messages for ClueLess

## Server to Client:
# Send message to indicate current game state (in case of refresh) - character positions, player’s cards, and all players’ names
def sendGameState():
    pass

# Send message to indicate beginning of player’s turn
def sendTurnStart():
    pass

# Send message to indicate the new space a character has moved to (character, new space name)
def broadcastMovementUpdate():
    pass

# Send message to indicate what suggestion a player has made (character, weapon, room name)
def broadcastSuggestion():
    pass

# Send message to the player who made a suggestion indicating what cards other players have chosen to show them that proves the suggestion false 
def sendSuggestionDisproof():
    pass

# Send message to indicate what accusation a player has made (character, weapon, room name) 4
def broadcastAccusation():
    pass

# Send message to an accusing player to indicate the true character, weapon, and room name 
def sendCaseFile():
    pass

# Send message to players indicating if an accusation was false or true (indicating a winner)
def broadcastAccusationResult():
    pass

## Client to Server:
# Request for game state refresh
def onGameStateRequest():
    pass

# Send message to indicate which space player has moved to (character, new space name)
def onPlayerMove():
    pass

# Send message with a suggestion from the player (character, weapon, room name)
def onSuggestion():
    pass

# Send message to indicate which card disproves a player’s suggestion (card name, card type)
def onSuggestionDisproof():
    pass

# Send message with an accusation from the player (character, weapon, room name)
def onAccusation():
    pass

## Server to Database:
# Request and update data according to gameplay
## Database to Server:
# Return requested data and success status of an update request
# Getters
def getCharacterLocation(characterID):
    pass

def getPlayerName(playerID):
    pass

def getPlayerCharacter(playerID):
    pass

def getMayStay(playerID):
    pass

def getCurPlayer(gameID):
    pass

def getNextPlayer(playerID):
    pass

def getCaseFile(gameID):
    pass

def getPlayerCards(playerID):
    pass

# Setters
def setCharacterLocation(characterID):
    pass

def setPlayerName(playerID):
    pass

def setPlayerCharacter(playerID):
    pass

def setMayStay(playerID):
    pass

def setCurPlayer(gameID):
    pass

def setNextPlayer(playerID):
    pass

def setCaseFile(gameID):
    pass

def setPlayerCards(playerID):
    pass

####################################################



# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """    
    socketio.run(application, port=8000, debug=True)