# File originally downloaded from https://github.com/josharnoldjosh/simple-flask-socketio-example
# on 10/21/23.  Has been modified by Creative Engineers for the Clue-Less project.
import random
import string
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
import psycopg
from gamelogic import Lobby, GameInstance
from gameinfo import Player

ROOM_CODE_CHARS = string.ascii_lowercase + string.digits

gameRooms = {}

characters = ["Miss Scarlet", "Prof. Plum", "Mrs. Peacock", "Mr. Green",
              "Mrs. White", "Col. Mustard"]

# Init the server
application = Flask(__name__)
socketio = SocketIO(application, logger=True)


# Send HTML!
#@application.route('/')
#def root():    
#    return render_template('index.html')

# Receive a message from the front end HTML
@socketio.on('send_message')   
def message_recieved(data, buttonnum):
    match buttonnum:
        case 1:
            getCharacterLocation(data['text'])
        case 2:
            getPlayerName(data['text'])
        case 3:
            getPlayerCharacter(data['text'])
        case 4:
            getMayStay(data['text'])
        case 5:
            getCurPlayer(data['text'])
        case 6:
            getNextPlayer(data['text'])
        case 7:
            getCaseFile(data['text'])
        case 8:
            getPlayerCards(data['text'])
        case 9:
            setCharacterLocation(1, data['text'])
        case 10:
            setPlayerName(1, data['text'])
        case 11:
            setPlayerCharacter(1, data['text'])
        case 12:
            setMayStay(data['text'])
        case 13:
            setCurPlayer(data['text'])
        case 14:
            setNextPlayer(data['text'])
        case 15:
            accusation(data['text'])
            pass

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

@application.route('/host-lobby')
def create_lobby():
    return render_template('host-lobby.html', character_list=characters)

@application.route('/join-lobby')
def join_lobby():
    return render_template('join-lobby.html', character_list=characters)

@socketio.on('connect')
def test_connect():
    socketio.emit('after connect', {'data':'Connected to Flask Socket.'})

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

#Create Game Room
@socketio.on('create')
def on_create(data):
    username = data['username']
    #Create new player
    new_player = Player(username)

    #Create unique game/roomCode
    while True:
        roomCode = ''.join(random.choice(ROOM_CODE_CHARS) for i in range(6))
        # Ensure code is unique
        if roomCode not in gameRooms:
            break
    
    gameRooms[roomCode] = Lobby(roomCode)
    join_room(roomCode)
    gameRooms[roomCode].addPlayer(new_player)
    socketio.emit("room_code", {'text': roomCode})

#Join existing Game Room
@socketio.on('join')
def on_join(data):
    username = data['username']
    #Create new player
    new_player = Player(username)

    room = data['roomCode']
    if room not in gameRooms:
        socketio.emit("invalid_room_code", {'text': "Game lobby '" + room + "' does not exist.<br>Please enter a valid lobby code:"})
    else:
        join_room(room)
        gameRooms[room].addPlayer(new_player)
        socketio.emit("join_conf", {'code': room, 'text': 'User has joined the room.'})
        socketio.emit("players_in_lobby", {'num': gameRooms[room].getNumPlayers()})

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

def accusation(accString):
    numstring = accString.split(',')
    num1 = numstring[0].strip()
    num1 = int(num1)
    num2 = numstring[1].strip()
    num2 = int(num2)
    num3 = numstring[2].strip()
    num3 = int(num3)
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT case_file FROM game_info WHERE game_id = 1")
            caseFile = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (caseFile[0],))
            caselocation = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (caseFile[1],))
            casecharacter = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (caseFile[2],))
            caseweapon = cur.fetchone()[0]
            socketio.emit('message_from_server', {'text':'The case file is: ' + caselocation + ", " + casecharacter + ", " + caseweapon})
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (num1,))
            guessLocation = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (num2,))
            guessCharacter = cur.fetchone()[0]
            cur.execute("SELECT card_name FROM cards WHERE card_id = %s", (num3,))
            guessWeapon = cur.fetchone()[0]
            if num1 == caseFile[0] and num2 == caseFile[1] and num3 == caseFile[2]:
                socketio.emit('message_from_server', {'text':'You guessed: ' + guessLocation + ", " + guessCharacter + ", " + guessWeapon + ". You win!"})
            else:
                socketio.emit('message_from_server', {'text':'You guessed: ' + guessLocation + ", " + guessCharacter + ", " + guessWeapon + ". You lose."})

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
            #These can be replaced with function calls later, but we are sending visible messages for now so I can't return a value.
            location = cur.execute("SELECT location FROM players WHERE player_id = %s", (playerID,))
            location = location.fetchone()[0]
            name = cur.execute("SELECT player_name FROM players WHERE player_id = %s", (playerID,))
            playerName = name.fetchone()[0]
            if location == "Hallway":
                socketio.emit('message_from_server', {'text': playerName + ' is in a hallway and may not stay.'})
            else:
                socketio.emit('message_from_server', {'text': playerName + ' is not in a hallway and may stay.'})

def getCurPlayer(gameID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            print(gameID)
            gameId = int(gameID)
            cur.execute("SELECT currentid FROM gamestate WHERE game_id = %s", (gameId,))
            cur.execute("SELECT player_name FROM players WHERE player_id = %s", (cur.fetchone()[0],))
            playername = cur.fetchone()[0]
            socketio.emit('message_from_server', {'text':'It is ' + playername + "'s turn."})

def getNextPlayer(playerID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MAX(player_id) FROM players")
            maxID = cur.fetchone()[0]
            if int(playerID) < int(maxID):
                cur.execute("SELECT player_name FROM players WHERE player_id = %s", ((int(playerID) + 1),))
                socketio.emit('message_from_server', {'text':cur.fetchone()[0] + " has the next turn."} )
            else:
                cur.execute("SELECT player_name FROM players WHERE player_id = %s", (1,))
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
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            cur.execute("UPDATE players SET location = %s WHERE player_ID = %s", (location, playerID,))
            cur.execute("SELECT location FROM players WHERE player_ID = %s", (playerID,))
            #fetchone() returns a tuple, so we need to index it to get the value
            if cur.fetchone()[0] == (location):
                socketio.emit("message_from_server", {'text': 'Success'})

def setPlayerName(playerID, playerName):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            cur.execute("UPDATE players SET player_name = %s WHERE player_ID = %s", (playerName, playerID,))
            cur.execute("SELECT player_name FROM players WHERE player_ID = %s", (playerID,))
            #fetchone() returns a tuple, so we need to index it to get the value
            if cur.fetchone()[0] == (playerName):
                socketio.emit("message_from_server", {'text': 'Success'})

def setPlayerCharacter(playerID, character_name):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            cur.execute("UPDATE players SET character_name = %s WHERE player_ID = %s", (character_name, playerID,))
            cur.execute("SELECT character_name FROM players WHERE player_ID = %s", (playerID,))
            #fetchone() returns a tuple, so we need to index it to get the value
            if cur.fetchone()[0] == (character_name):
                socketio.emit("message_from_server", {'text': 'Success'})

def setMayStay(playerID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            #fetchone() returns a tuple, so we need to index it to get the value
            location = cur.execute("SELECT location FROM players WHERE player_id = %s", (playerID,))
            location = location.fetchone()[0]
            if location == "Hallway":
                cur.execute("UPDATE players SET may_stay = %s WHERE player_ID = %s", (False, playerID,))
                cur.execute("SELECT location FROM players WHERE player_id = %s", (playerID,))
                if not cur.fetchone()[0]:
                    socketio.emit("message_from_server", {'text': 'Success'})
            else:
                cur.execute("UPDATE players SET may_stay = %s WHERE player_ID = %s", (True, playerID,))
                cur.execute("SELECT location FROM players WHERE player_id = %s", (playerID,))
                if cur.fetchone()[0]:
                    socketio.emit("message_from_server", {'text': 'Success'})
                       
def setCurPlayer(gameID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT currentid FROM gamestate WHERE game_id = %s", (gameID,))
            cur.execute("UPDATE gamestate SET currentID = %s WHERE game_id = %s", (2, gameID,))
            socketio.emit("message_from_server", {'text': 'Success'})
            #fetchone() returns a tuple, so we need to index it to get the value
            #if cur.fetchone()[0] == (playerName):
            #    print("Success")

def setNextPlayer(playerID):
    with psycopg.connect("dbname=Skeletal user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            #execute statements with %s as a placeholder for the value require a comma after the value because it returns a tuple
            #cur.execute("UPDATE players SET player_name = %s WHERE player_ID = %s", (playerName, playerID,))
            cur.execute("SELECT player_name FROM players WHERE player_ID = %s", (playerID,))
            socketio.emit("message_from_server", {'text': 'Success'})
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