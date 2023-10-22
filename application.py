# File originally downloaded from https://github.com/josharnoldjosh/simple-flask-socketio-example
# on 10/21/23.  Has been modified by Creative Engineers for the Clue-Less project.

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import psycopg

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
    if data == "test":
        getCharacterLocation(1)
    print(data['text'])
    socketio.emit('message_from_server', {'text':'Message recieved!'})

####################################################
# Messages for ClueLess

## Server to Client:
# Send message to indicate current game state (in case of refresh) - character positions, player’s cards, and all players’ names
def sendGameState():
    socketio.emit('game_state', {'text':''})

# Send message to indicate beginning of player’s turn
def sendTurnStart():
    socketio.emit('begin_turn', {'text':''})

# Send message to indicate the new space a character has moved to (character, new space name)
def broadcastMovementUpdate():
    socketio.emit('bc_movement_update', {'text':''})

# Send message to indicate what suggestion a player has made (character, weapon, room name)
def broadcastSuggestion():
    socketio.emit('bc_suggestion', {'text':''})

# Send message to the player who made a suggestion indicating what cards other players have chosen to show them that proves the suggestion false 
def sendSuggestionDisproof():
    socketio.emit('suggestion_disproof', {'text':''})

# Send message to indicate what accusation a player has made (character, weapon, room name) 4
def broadcastAccusation():
    socketio.emit('bc_accusation', {'text':''})

# Send message to an accusing player to indicate the true character, weapon, and room name 
def sendCaseFile():
    socketio.emit('case_file', {'text':''})

# Send message to players indicating if an accusation was false or true (indicating a winner)
def broadcastAccusationResult():
    socketio.emit('bc_accusation_result', {'text':''})

## Client to Server:
# Request for game state refresh
socketio.on('game_state_request')
def onGameStateRequest(data):
    pass

# Send message to indicate which space player has moved to (character, new space name)
socketio.on('player_move')
def onPlayerMove(data):
    pass

# Send message with a suggestion from the player (character, weapon, room name)
socketio.on('suggestion')
def onSuggestion(data):
    pass

# Send message to indicate which card disproves a player’s suggestion (card name, card type)
socketio.on('suggestion_disproof')
def onSuggestionDisproof(data):
    pass

# Send message with an accusation from the player (character, weapon, room name)
socketio.on('accusation')
def onAccusation(data):
    pass

## Server to Database:
# Request and update data according to gameplay
## Database to Server:
# Return requested data and success status of an update request
# Getters
"""
Currently, these will be dummy functions. We will need to replace dbname, user, and password with approriate values.
Select statements will have to be fixed as well.
"""
def getCharacterLocation(characterID):
    with psycopg.connect("dbname=testdb user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT location FROM *table3* WHERE unique_id = %s", (characterID,))
            print(cur.fetchone())
            for row in cur:
                print(row)
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
"""
Will we need to set default values at the start of each round? 
I think everything will be different each time so we will just need to run these setters for each character.
We could also make a larger function that accepts and sets all of the values for each character at the start of the game.
"""
# Setters
def setCharacterLocation(characterID, location):
    with psycopg.connect("dbname=testdb user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            cur.execute("UPDATE *table3* SET location = %s WHERE characterID = %s", (location, characterID,))
            cur.execute("SELECT location FROM *table3* WHERE characterID = %s", (characterID,))
            #fetchone() returns a tuple, so we need to index it to get the value
            if cur.fetchone()[0] == (location):
                print("Success")
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