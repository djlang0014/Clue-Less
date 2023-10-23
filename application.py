# File originally downloaded from https://github.com/josharnoldjosh/simple-flask-socketio-example
# on 10/21/23.  Has been modified by Creative Engineers for the Clue-Less project.

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import psycopg

# Init the server
application = Flask(__name__)
socketio = SocketIO(application, logger=True)

"""
# Send HTML!
@application.route('/')
def root():    
    return render_template('index.html')

# Receive a message from the front end HTML
@socketio.on('send_message')   
def message_recieved(data):
    print(data.items())
    if data['text'] == "test":
        getCharacterLocation('1')
    print(data['text'])
    socketio.emit('message_from_server', {'text':'Message received!'})
"""
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

@socketio.on('connect')
def test_connect():
    socketio.emit('after connect', {'data':'Connected to Flask Socket.'})

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

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
The exact database layout will need to be refined for the minimal implementation, but this should be good for the skeletal.
"""
def getCharacterLocation(playerID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT location FROM players WHERE player_id = %s", (playerID,))
            socketio.emit('message_from_server', {'text':'Here is the player location: ' + cur.fetchone()[0]})

def getPlayerName(playerID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT player_name FROM players WHERE player_id = %s", (playerID,))
            socketio.emit('message_from_server', {'text':'Here is the player name: ' + cur.fetchone()[0]})

def getPlayerCharacter(playerID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT character_name FROM players WHERE player_id = %s", (playerID,))
            socketio.emit('message_from_server', {'text':'Here is the player character: ' + cur.fetchone()[0]})

def getMayStay(playerID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_playerID FROM players")
            currentPlayerID = cur.fetchone()[0]
            if playerID == currentPlayerID:
                #These can be replaced with function calls later, but we are sending visible messages for now so I can't return a value.
                location = cur.execute("SELECT location FROM players WHERE player_id = %s", (playerID,))
                name = cur.execute("SELECT player_name FROM players WHERE player_id = %s", (playerID,))
                if location == "Hallway":
                    socketio.emit('message_from_server', {'text':name + 'is in a hallway and may not stay.'})
                else:
                    socketio.emit('message_from_server', {'text':name + 'is not in a hallway and may stay.'})
            else:
                socketio.emit('message_from_server', {'text':'It is not your turn.'})

def getCurPlayer(gameID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_playerID FROM players WHERE game_id = %s", (gameID,))
            socketio.emit('message_from_server', {'text':'It is : ' + cur.fetchone()[0]} + "'s turn.")

def getNextPlayer(playerID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MAX(player_id) FROM players")
            if playerID < cur.fetchone()[0]:
                cur.execute("SELECT player_name FROM players WHERE player_id = %s", (playerID + 1,))
                socketio.emit('message_from_server', {'text':cur.fetchone()[0] + " has the next turn."} )    

def getCaseFile(gameID):
    #This can be a join or something
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #Returns an array of card IDs which are integers. Will be in location, character, weapon order.
            cur.execute("SELECT case_file FROM game_info WHERE game_id = %s", (gameID,))
            caseFile = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (caseFile[0],))
            location = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (caseFile[1],))
            character = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (caseFile[2],))
            weapon = cur.fetchone()[0]
            socketio.emit('message_from_server', {'text':'The case file is: ' + location + ", " + character + ", " + weapon})

def getPlayerCards(playerID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #Returns an array of card IDs which are integers. Will be in location, character, weapon order.
            cur.execute("SELECT card_ids FROM players WHERE player_ID = %s", (playerID,))
            caseFile = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (caseFile[0],))
            location = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (caseFile[1],))
            character = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (caseFile[2],))
            weapon = cur.fetchone()[0]
            socketio.emit('message_from_server', {'text':'The case file is: ' + location + ", " + character + ", " + weapon})

"""
Will we need to set default values at the start of each round? 
I think everything will be different each time so we will just need to run these setters for each character.
We could also make a larger function that accepts and sets all of the values for each character at the start of the game.
"""
# Setters
def setCharacterLocation(playerID, location):
    with psycopg.connect("dbname=testdb user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            cur.execute("UPDATE players SET location = %s WHERE player_ID = %s", (location, playerID,))
            cur.execute("SELECT location FROM players WHERE player_ID = %s", (playerID,))
            #fetchone() returns a tuple, so we need to index it to get the value
            if cur.fetchone()[0] == (location):
                print("Success")

def setPlayerName(playerID, playerName):
    with psycopg.connect("dbname=testdb user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            cur.execute("UPDATE players SET player_name = %s WHERE player_ID = %s", (playerName, playerID,))
            cur.execute("SELECT player_name FROM players WHERE player_ID = %s", (playerID,))
            #fetchone() returns a tuple, so we need to index it to get the value
            if cur.fetchone()[0] == (playerName):
                print("Success")

def setPlayerCharacter(playerID, character_name):
    with psycopg.connect("dbname=testdb user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            cur.execute("UPDATE players SET character_name = %s WHERE player_ID = %s", (character_name, playerID,))
            cur.execute("SELECT character_name FROM players WHERE player_ID = %s", (playerID,))
            #fetchone() returns a tuple, so we need to index it to get the value
            if cur.fetchone()[0] == (character_name):
                print("Success")

def setMayStay(playerID):
    with psycopg.connect("dbname=testdb user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            #fetchone() returns a tuple, so we need to index it to get the value
            location = cur.execute("SELECT location FROM players WHERE player_id = %s", (playerID,))
            location = location[0]
            if location == "Hallway":
                cur.execute("UPDATE players SET may_stay = %s WHERE player_ID = %s", (False, playerID,))
                cur.execute("SELECT location FROM players WHERE player_id = %s", (playerID,))
                if not cur.fetchone()[0]:
                    print("Success")
            else:
                cur.execute("UPDATE players SET may_stay = %s WHERE player_ID = %s", (True, playerID,))
                cur.execute("SELECT location FROM players WHERE player_id = %s", (playerID,))
                if cur.fetchone()[0]:
                    print("Success")
                       
def setCurPlayer(gameID):
    with psycopg.connect("dbname=testdb user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_playerID FROM game_states WHERE game_id = %s", (gameID,))
            #fetchone() returns a tuple, so we need to index it to get the value
            #if cur.fetchone()[0] == (playerName):
            #    print("Success")

def setNextPlayer(playerID):
    with psycopg.connect("dbname=testdb user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            #cur.execute("UPDATE players SET player_name = %s WHERE player_ID = %s", (playerName, playerID,))
            cur.execute("SELECT player_name FROM players WHERE player_ID = %s", (playerID,))
            #fetchone() returns a tuple, so we need to index it to get the value
            #if cur.fetchone()[0] == (playerName):
            #    print("Success")

def setCaseFile(gameID):
    pass

def setPlayerCards(playerID):
    pass

####################################################



# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """    
    socketio.run(application, port=8000, debug=True)