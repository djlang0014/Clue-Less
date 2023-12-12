# File originally downloaded from https://github.com/josharnoldjosh/simple-flask-socketio-example
# on 10/21/23.  Has been modified by Creative Engineers for the Clue-Less project.
import random
import string
from config import DB_NAME, DB_USERNAME, DB_PASSWORD
from flask import Flask, render_template, request, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session
import psycopg
from gameinfo import *
from gamelogic import *
import threading
import os
import time, datetime


ROOM_CODE_CHARS = string.ascii_lowercase + string.digits

gameRooms = {}

playerList = []
playerDict = {} #Key: username, Value: Player

#TODO: Disproof won't exit, make sure you can only end turn once, gray out if it's not your turn


characterPlayerDict = {}
#add a disabled characters list to disable them for people who join later

cardCharacterList = [
    Card("Character", "Miss Scarlet"),
    Card("Character", "Col. Mustard"),
    Card("Character", "Mrs. White"),
    Card("Character", "Mr. Green"),
    Card("Character", "Mrs. Peacock"),
    Card("Character", "Prof. Plum"),
]
cardWeaponList =[
    Card("Weapon", "Rope"),
    Card("Weapon", "Lead Pipe"),
    Card("Weapon", "Knife"),
    Card("Weapon", "Wrench"),
    Card("Weapon", "Candlestick"),
    Card("Weapon", "Revolver"),
]
cardLocationList = [
    Card("Location", "Study"),
    Card("Location", "Hall"),
    Card("Location", "Lounge"),
    Card("Location", "Library"),
    Card("Location", "Billiard"),
    Card("Location", "Dining"),
    Card("Location", "Conservatory"),
    Card("Location", "Ballroom"),
    Card("Location", "Kitchen"),
]

suggestionLocations = [
    "Study",
    "Hall",
    "Lounge",
    "Library",
    "Billiard",
    "Dining",
    "Conservatory",
    "Ballroom",
    "Kitchen",
]
    

locationList = [
    Location("Study", "Room", 2, ["Hall1", "Hall3", "Kitchen"]),
    Location("Hall1", "Hallway", 1, ["Study", "Hall"]),
    Location("Hall", "Room", 2, ["Hall1", "Hall2", "Hall4"]),
    Location("Hall2", "Hallway", 1, ["Hall", "Lounge"]),
    Location("Lounge", "Room", 2, ["Hall3", "Hall5", "Conservatory"]),
    Location("Hall3", "Hallway", 1, ["Study", "Library"]),
    Location("Hall4", "Hallway", 1, ["Hall", "Billiard"]),
    Location("Hall5", "Hallway", 1, ["Lounge", "Dining"]),
    Location("Libary", "Room", 2, ["Hall3", "Hall6", "Hall8"]),
    Location("Hall6", "Hallway", 1, ["Billiard", "Library"]),
    Location("Billiard", "Room", 2, ["Hall4", "Hall6", "Hall7", "Hall9"]),
    Location("Hall7", "Hallway", 1, ["Billiard", "Dining"]),
    Location("Dining", "Room", 2, ["Hall5", "Hall7", "Hall10"]),
    Location("Hall8", "Hallway", 1, ["Library", "Conservatory"]),
    Location("Hall9", "Hallway", 1, ["Billiard", "Ballroom"]),
    Location("Hall10", "Hallway", 1, ["Dining", "Kitchen"]),
    Location("Conservatory", "Room", 2, ["Hall8", "Hall11", "Lounge"]),
    Location("Hall11", "Hallway", 1, ["Conservatory", "Ballroom"]),
    Location("Ballroom", "Room", 2, ["Hall9", "Hall11", "Hall12"]),
    Location("Hall12", "Hallway", 1, ["Ballroom", "Kitchen"]),
    Location("Kitchen", "Room", 2, ["Hall10", "Hall12", "Study"]),
]

characters = ["Miss Scarlet", "Prof. Plum", "Mrs. Peacock", "Mr. Green",
              "Mrs. White", "Col. Mustard"]

# Init the server
application = Flask(__name__)
application.config["SESSION_TYPE"] = "filesystem"
Session(application)
socketio = SocketIO(application, logger=True, manage_session=False)

# create database connection with credentials
# can remove all other psycopg.connect() lines


application.secret_key = os.urandom(24)  

conn = psycopg.connect(f"dbname={DB_NAME} user={DB_USERNAME} password={DB_PASSWORD}")
 
# Send HTML!
@application.route('/')
def root():
    if 'user_id' not in session:
        session['user_id'] = os.urandom(24).hex()    
    return render_template('main_menu.html')

@application.route('/debug')
def print_all():
    json = {}
    for roomCode in gameRooms:
        tmp2 = []
        for key in gameRooms[roomCode].playersDict:
            tmp2.append(key)
        json[roomCode] = tmp2
    return json

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
    session['username'] = username
    session.modified = True
    user_id = session['user_id']
    new_player = Player(username, request.sid)
    playerList.append(new_player)
    # playerDict[username] = new_player
    #Create unique game/roomCode
    while True:
        roomCode = ''.join(random.choice(ROOM_CODE_CHARS) for i in range(6))
        # Ensure code is unique
        if roomCode not in gameRooms:
            break
    
    gameRooms[roomCode] = Lobby(roomCode)
    join_room(roomCode)
    session['roomCode'] = roomCode
    session.modified = True
    gameRooms[roomCode].addPlayer(new_player)
    socketio.emit("room_code", {'text': roomCode}, to=request.sid)

#Join existing Game Room
@socketio.on('join')
def on_join(data):
    username = data['username']

    #Create new player
    user_id = session['user_id']
    session['username'] = username
    session.modified = True
    new_player = Player(username, request.sid)

    playerList.append(new_player)

    room = data['roomCode']
    if room not in gameRooms:
        socketio.emit(
            "invalid_room_code", 
            {'text': "Game lobby '" + room + "' does not exist.<br>Please enter a valid lobby code:"},
            to=request.sid
        )
    else:
        join_room(room)
        session['roomCode'] = room
        session.modified = True
        gameRooms[room].addPlayer(new_player)

        #When other game started, updated all host pages with the new room code,
        # but joining a game did not trigger the response on the host
        socketio.emit("join_conf", {'code': room, 'text': 'User has joined the room.'}, to=request.sid)
        socketio.emit("players_in_lobby", {'num': gameRooms[room].getNumPlayers()}, to=room)
        # socketio.emit("to_host", {'text':'Test messageNOW'}, to=gameRooms[room].players[0].sid)

#Join existing Game Room
@socketio.on('start_game')
def on_game_start(data):
    roomCode = data['roomCode']

    # Start GameInstance object and replace the game's Lobby in the gameRooms hashmap
    gameRooms[roomCode] = gameRooms[roomCode].startGame()

    locationStack = locationList
    cardLocationStack = cardLocationList
    cardCharacterStack = cardCharacterList
    cardWeaponStack = cardWeaponList
    caseFile = CaseFile(
        cardCharacterStack[random.randint(0,len(cardCharacterStack)-1)],
        cardWeaponStack[random.randint(0,len(cardWeaponStack)-1)],
        cardLocationStack[random.randint(0,len(cardLocationStack)-1)]
    )
    gameRooms[roomCode].caseFile = caseFile    

    #Make sure Miss Scarlet goes first
    for i in range(len(gameRooms[roomCode].players)):
        if not i == 0 and gameRooms[roomCode].players[i].character == "Miss Scarlet":
            gameRooms[roomCode].players[0], gameRooms[roomCode].players[i] = gameRooms[roomCode].players[i], gameRooms[roomCode].players[0]
            break

    for player in gameRooms[roomCode].players:
        print(player.character)

    cards = cardLocationStack + cardCharacterStack + cardWeaponStack
    random.shuffle(cards)
    i = 0
    #Shuffle cards and deal to players
    while i < len(cards):
        for player in gameRooms[roomCode].players:
            player.addPlayerCard(cards[i])
            i += 1
            if i >= len(cards):
                break
    
    # post game session information to database
    setGameSessionDetails(roomCode, caseFile)

    socketio.emit("start_game_all", {'url': url_for('testzone')}, to=roomCode)
    time.sleep(1)

    socketio.emit("your_turn", {'text':"It is your turn!"}, to=gameRooms[roomCode].players[gameRooms[roomCode].turnIndex].sid)

    for player in gameRooms[roomCode].players:
        if (player.sid != gameRooms[roomCode].players[0].sid):
            socketio.emit("turn_notification", {'text':"It is " + gameRooms[roomCode].players[gameRooms[roomCode].turnIndex].name+"'s turn!"}, to=player.sid)



@socketio.on('init_game')
def init_game():
    username = session['username']
    roomCode = session['roomCode']

    #new sessionID joins room
    join_room(roomCode)

    #Update SessionID for player
    gameRooms[roomCode].playersDict[username].updateSessionID(request.sid)

    gameInstance = gameRooms[roomCode]
    caseFile = gameInstance.caseFile

    player = gameRooms[roomCode].playersDict[username]

    socketio.emit("playerinfo", {'playername': player.name, 'character': player.getPlayerCharacter()}, to=request.sid)
    playerCards = player.getPlayerCards()

    # post player information to the database
    setPlayerInfo(player, roomCode)

    for card in playerCards:
        socketio.emit("playercard", {'cardtype': card.cardType, 'cardname': card.cardName}, to=request.sid)

    match player.getPlayerCharacter():
        case "Miss Scarlet":
            startLocation = 'ScarletStart'
        case "Col. Mustard":
            startLocation = 'MustardStart'
        case "Mrs. White":
            startLocation = 'WhiteStart'
        case "Mr. Green":
            startLocation = 'GreenStart'
        case "Mrs. Peacock":
            startLocation = 'PeacockStart'
        case "Prof. Plum":
            startLocation = 'PlumStart'

    gameInstance.setPlayerStartLocation(player.sid, startLocation)
    setPlayerLocation(roomCode, player.sid, startLocation)

    
@socketio.on('backdoor')
def backdoor(data):
    roomCode = session['roomCode']
    caseWeapon = gameRooms[roomCode].caseFile.weapon
    caseSuspect = gameRooms[roomCode].caseFile.suspect
    caseRoom = gameRooms[roomCode].caseFile.room
    socketio.emit('message_from_server', {'text': caseWeapon.cardName + ", " + caseSuspect.cardName + ", " + caseRoom.cardName})
    
@socketio.on('select_character')
def select_character(data):
    user_id = session['user_id']
    character = data['character']
    username = session['username']
    roomCode = session['roomCode']
    player = gameRooms[roomCode].playersDict[username]
    player.selectCharacter(character)
    characterPlayerDict[character] = player
    roomCode = data['roomCode']
    print(player.character)
    socketio.emit("disable_character", {'character': data['character']}, to=roomCode)

@socketio.on('end_turn')
def end_turn():
    user_id = session['user_id']
    username = session['username']
    roomCode = session['roomCode']
    
    gameInstance = gameRooms[roomCode]
    currPlayer = gameInstance.playersDict[username]
    
    # Process regular turn index
    i = gameInstance.turnIndex
    next_player_index = (i + 1) % len(gameInstance.players)

    # retrieve next player
    nextPlayer = gameRooms[roomCode].players[next_player_index]

    for player in gameRooms[roomCode].players:
        if (player.sid != nextPlayer.sid):
            socketio.emit("turn_notification", {'text':"It is " + gameRooms[roomCode].players[next_player_index].name+"'s turn!"}, to=player.sid)

    socketio.emit("your_turn", {'text':"It is your turn!"}, to=gameInstance.players[next_player_index].sid)
    gameInstance.turnIndex = next_player_index    
    

@application.route('/testzone')
def testzone():
    return render_template('testzone.html')

@socketio.on('connect')
def test_connect():
    socketio.emit('after connect', {'data':'Connected to Flask Socket.'})

@socketio.on('chat_message')
def chat_message(data):
    username = session['username']
    roomCode = session['roomCode']
    text = data['text']

    socketio.emit("message_from_server", {'text': username+": "+text}, to=roomCode)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('move_character')
def movecharacter(data):
    newLocation = data['location']
    character = data['character']
    roomCode = session['roomCode']
    player = gameRooms[roomCode].playersDict[session['username']]
    playername = player.name
    gameInstance = gameRooms[roomCode]

    # query database to retrieve player's current location
    currentLocation = getPlayerCurrentLocation(player.sid, roomCode)

    adjacent_locations = gameInstance.findAvailableLocations(player.sid, currentLocation)

    if newLocation not in adjacent_locations:
        socketio.emit('message_from_server', {'text': character + ' cannot move there.'}, to=gameRooms[roomCode].players[gameRooms[roomCode].turnIndex].sid)
    else:
        # query database to see if the location is occupied, and if so whether it's a hallway
        is_occupied_hallway = checkIfHallwayAndOccupied(roomCode, newLocation)
        if (is_occupied_hallway == True):
            socketio.emit('message_from_server', {'text': character + ' cannot move there.'}, to=gameRooms[roomCode].players[gameRooms[roomCode].turnIndex].sid)
        else:
            # update location in object and database, then move character and send a message to all players
            gameInstance.setPlayerLocation(player.sid, newLocation)
            setPlayerLocation(roomCode, player.sid, newLocation)
            socketio.emit('movecharacter', {'character': character, 'location': newLocation, 'username': playername}, to=roomCode)
            socketio.emit('message_from_server', {'text' : player.name + ' has moved to ' + newLocation + '.'}, to=roomCode)
            

@socketio.on('get_available_locations')
def get_available_locations(data):
    roomCode = session['roomCode']
    character = data['character']
    player = gameRooms[roomCode].playersDict[session['username']]
    gameInstance = gameRooms[roomCode]

    currentLocation = getPlayerCurrentLocation(player.sid, roomCode)

    available_locations = gameInstance.findAvailableLocations(player.sid, currentLocation)

    for location in available_locations:
        if checkIfHallwayAndOccupied(roomCode, location) == True:
            available_locations.remove(location)
        
    socketio.emit("available_locations", {'locations': available_locations}, to=player.sid)
  

@socketio.on('accusation')
def accusation(data):
    accuseWeapon = data['weapon']
    accuseSuspect = data['suspect']
    accuseRoom = data['room']
    roomCode = session['roomCode']
    gameInstance = gameRooms[roomCode]
    player = gameInstance.playersDict[session['username']]
    name = player.name

    sessionCaseFile = getCaseFile(roomCode)
    accusationCards = [accuseRoom, accuseSuspect, accuseWeapon]

    delim = ", "

    if all(card in sessionCaseFile for card in accusationCards): 
        socketio.emit('message_from_server', {'text': name + ' wins!'}, to=roomCode)
        socketio.emit('end_game', {'text': player.sid})
        setEndGameSessionDetails(roomCode, player.sid)
    else:
        # TODO: player can't make any other moves again but can still stay in the game to disprove suggestions
        #            - update properties instead of removing from gameInstance
        gameInstance.players.remove(player)
        socketio.emit('message_from_server', {'text': name + ' was incorrect. They guessed: ' + delim.join(accusationCards)}, to=roomCode)
    
@socketio.on('suggestion')
def suggestion(data):
    suggestWeapon = data['weapon']
    suggestSuspect = data['suspect']
    username = session['username']
    roomCode = session['roomCode']
    instance = gameRooms[roomCode]

    currPlayer = gameRooms[roomCode].playersDict[username]
    currPlayer.suggesting = True

    print(currPlayer)
    print(username, gameRooms[roomCode])

    gameInstance = gameRooms[roomCode]
    gameInstance.suggestionPhase = True

    suggestRoom = gameInstance.getPlayerLocation(currPlayer.sid)
    
    if suggestRoom not in suggestionLocations:
        socketio.emit('message_from_server', {'text': 'You cannot make a suggestion from there.'}, to=currPlayer.sid)
        return
    
    name = currPlayer.name

    if suggestSuspect in characterPlayerDict:
        setPlayerLocation(roomCode, characterPlayerDict[suggestSuspect].sid, suggestRoom)

    socketio.emit('move_for_suggestion', {'character': suggestSuspect, 'location': suggestRoom, 'username': username}, to=roomCode)
    
    suggestRoom = getPlayerCurrentLocation(currPlayer.sid, roomCode)

    suggestionString = "" + suggestWeapon + ", " + suggestSuspect + ", " + suggestRoom + "."

    socketio.emit('message_from_server', {'text': name + ' suggested: ' + suggestionString}, to=roomCode)
    
    # update index for suggestion turns 
    i = gameInstance.turnIndex
    next_player_index = (i + 1) % len(gameInstance.players)

    nextPlayer = gameInstance.players[next_player_index]

    if (nextPlayer.suggesting == False):
        socketio.emit("message_from_server", {'text':"It is your turn to disprove!"}, to=nextPlayer.sid)
        socketio.emit('showsuggestmodal', {'player': gameInstance.players[next_player_index].name, 'suggestSuspect' : suggestSuspect, 'suggestWeapon': suggestWeapon, 'suggestRoom': suggestRoom }, to=nextPlayer.sid)

@socketio.on('getcards')
def getcards(data):
    roomCode = session['roomCode']
    username = session['username']
    player = gameRooms[roomCode].playersDict[username]
    playerCards = player.getPlayerCards()
    playerCardNames = []

    for card in playerCards:
        playerCardNames.append(card.cardName)
    print("here")
    socketio.emit("modalcards", {'cards': playerCardNames}, to=player.sid)

@socketio.on('getcardstoshow')
def getcards(data):
    roomCode = session['roomCode']
    username = session['username']
    player = gameRooms[roomCode].playersDict[username]
    playerCards = player.getPlayerCards()
    playerCardNames = []

    for card in playerCards:
        playerCardNames.append(card.cardName)
    print("here")
    socketio.emit("cardstoshow", {'cards': playerCardNames}, to=player.sid)    

@socketio.on('suggestionreply')
def suggestionreply(data):
    roomCode = session['roomCode']
    player = gameRooms[roomCode].playersDict[session['username']]

    disproved = False
    
    name = player.name

    card = data['weapon']

    if card == None:
        card = data['suspect']
    
    if card == None:
        card = data['room']

    
    #TODO: Need to get the SID of the suggesting player!
    #This is not the most graceful way to display this as it does not account for any other combinations
    if card == None:
        returnString = name + " had no cards to show."
    else:
        returnString = name + " showed: " + card

    socketio.emit('message_from_server', {'text': returnString}, to=roomCode)

    #TODO: Need to get the SID of the suggesting player!
    previous_player_index = gameRooms[roomCode].turnIndex
    if (previous_player_index != 0):
        --previous_player_index
    
    if (disproved):
        # message only to the suggesting player
        socketio.emit('message_from_server', {'text': returnString}, to=gameRooms[roomCode].players[previous_player_index].sid)

        # notify all other players (without showing the card itself)
        socketio.emit('message_from_server', {'text': name + ' showed ' + '!'}, to=gameRooms[roomCode].players[previous_player_index].sid)
    else:
        socketio.emit('message_from_server', {'text': name + ' could not disprove!'}, to=roomCode)

        # checks if the game is in its suggestion phase, if so move to that index

        gameInstance = gameRooms[roomCode]

        if (gameInstance.suggestionPhase) :
            i = gameInstance.suggestionTurnIndex
            next_player_index = (i + 1) % len(gameInstance.players)
            nextPlayer = gameInstance.players[next_player_index]

            # If it gets back to the suggesting player, then that means no one was able to disprove.
            if (nextPlayer.suggesting == True):
                socketio.emit('message_from_server', {'text' : 'No one was able to disprove!'}, to=gameRooms[roomCode])

                nextPlayer.suggesting = False
                gameInstance.suggestionPhase = False
                return
            else :
                socketio.emit("message_from_server", {'text':"It is your turn to disprove!"}, to=nextPlayer.sid)
                socketio.emit('showsuggestmodal', {'player': gameInstance.players[next_player_index].name}, to=nextPlayer.sid)
                gameInstance.suggestionTurnIndex = next_player_index
                return      
        
    #probably add a closemodal() or something to close all modals that are still open

## Server to Database:
# Request and update data according to gameplay
## Database to Server:
# Return requested data and success status of an update request

# Getters
def getPlayerCurrentLocation(player_id, roomCode):
        with conn.cursor() as cur:
            
            query = "SELECT locations.location_name FROM locations \
                INNER JOIN player_location_map ON locations.location_name = player_location_map.location_name \
                WHERE player_location_map.player_id = %s AND player_location_map.session_id = %s"
            
            values = [player_id, roomCode]

            try:
                cur.execute(query, values)
                curr_location = cur.fetchone()[0]
            except(Exception, psycopg.Error) as error:
                print("Error: ", error)
            
            return curr_location
        
#Returns an array of card names which will be an array of strings. Will be in location, character, weapon order.
def getCaseFile(roomCode):
    with conn.cursor() as cur:
        query = "SELECT case_file FROM game_session WHERE session_id = %s"

        values = [roomCode]

        result = ""
        try:
            cur.execute(query, values)
            result = cur.fetchone()[0]
        except(Exception, psycopg.Error) as error:
            print("Error: ", error)

        return result

# Setters
def setGameSessionDetails(roomCode,caseFile):
    with conn.cursor() as cur:
        now = datetime.datetime.now()
        curr_time = now.strftime('%Y-%m-%d %H:%M:%S')
        
        caseFileCards = [ 
            caseFile.room.cardName,
            caseFile.suspect.cardName, 
            caseFile.weapon.cardName
        ]

        query = "INSERT INTO game_session(session_id, is_active, start_time, num_players, case_file) VALUES (%s, %s, %s, %s, %s);"
        values = (roomCode, 't', curr_time, len(gameRooms[roomCode].players), caseFileCards)
        
        # Insert relevant game info into game_session table
        # note: we build the query string and values separately for safety reasons 
        try:
            cur.execute(query, values)
        except(Exception, psycopg.Error) as error:
            print("Error: ", error)
        
        conn.commit()
        socketio.emit("message_from_server", {'text': 'Success'})
        
def setEndGameSessionDetails(roomCode, playerID):
    # Updates the game session's active status and adds the end time and which player won the game
    with conn.cursor() as cur:
        now = datetime.datetime.now()
        curr_time = now.strftime('%Y-%m-%d %H:%M:%S')

        query = "UPDATE game_session SET is_active = %s, end_time = %s, player_won = %s WHERE session_id = %s;"

        values = ('f', curr_time, playerID, roomCode)

        try:
            cur.execute(query, values)
        except (Exception, psycopg.Error) as error:
            print("Error: ", error)
        
        conn.commit()
        socketio.emit("message_from_server", {'text': 'Success'})

def setPlayerInfo(player, roomCode):
    # Posts player info to the database
    with conn.cursor() as cur:
        gameInstance = gameRooms[roomCode]

        values = []
        values.append(player.sid)
        values.append(player.name)
        values.append(player.character)
        values.append(roomCode) 

        query = "INSERT INTO players(player_id, player_name, character_name, session_id)VALUES(%s, %s, %s, %s)"

        try:
            cur.execute(query, values)
        except (Exception, psycopg.Error) as error:
            print("Error: ", error)

        conn.commit()
 
def setPlayerLocation(roomCode, player_id, location):
    with conn.cursor() as cur:
        # Does an update (instead of insert) if the player_id already exists in the table
        query = "INSERT INTO player_location_map (location_name, player_id, session_id) VALUES (%s, %s, %s) ON CONFLICT (player_id) DO UPDATE SET location_name = excluded.location_name;"

        values = [location, player_id, roomCode]

        try:
            cur.execute(query, values)
        except (Exception, psycopg.Error) as error:
            print("Error ", error)
        
        conn.commit()

# This function queries the database to see if the location a player is moving to is an occupied hallway
def checkIfHallwayAndOccupied(roomCode, location):
    with conn.cursor() as cur:
        query = "SELECT locations.is_restricted FROM locations \
        INNER JOIN player_location_map ON locations.location_name = player_location_map.location_name \
        WHERE player_location_map.location_name = %s AND player_location_map.session_id = %s;"

        values = [location, roomCode]

        result = False

        # psycopg raises an exception when no records are found, and that case implies that the location wasn't listed 
        # on the player_location_map table at all (which means no players are located there)
        # So, we have result be False (i.e. not an occupied hallway) by default
        try:
            cur.execute(query, values)
            temp = cur.fetchone()[0]
            result = temp

        except (Exception, psycopg.Error) as error:
            print("Error ", error)
        
        return result


####################################################



# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """    
    socketio.run(application, port=8000, debug=True)
