from gameinfo import *

class Lobby:
    def __init__(self, roomCode):
        """
        Initializer for a Lobby instance. Creates as new Lobby, starts a list
            of players, and saves the roomCode for the Lobby/GameInstance
        Parameters:
            roomCode (string, len=6): identifier for the Flask Room. Random
                string of numbers and lowercase letters.
        """
        self.roomCode = roomCode
        self.players = []

    def startGame(self):
        #This will have to make a new game instance object
        newGameInstance = GameInstance(self.roomCode, self.players)
        return newGameInstance

    def removePlayer(self, player):
        self.players.remove(player)

    def addPlayer(self, player):
        self.players.append(player)

    def getNumPlayers(self):
        return len(self.players)

class GameInstance:
    def __init__(self, gameID, players):
        #Right now, gameID is the roomCode that is also used for the lobbies
        #(used for Flask SocketIO rooms)
        self.gameID = gameID
        self.players = players
        self.currentPlayer = players[0]
        self.caseFile = None
        self.locations = None
        self.playerLocations = {} #PlayerID:Location
        pass

    def setCurrentPlayer(self, player):
        self.currentPlayer = player

    def endGame(self):
        #This will have to end the game and remove the game instance object
        pass

    def updateGameStatus(self):
        pass

    def setPlayerCards(self):
        #This will set the player cards for each player
        pass

    def getCardList(self):
        #This will make the list of cards for the game
        pass

    def getLocationList(self):
        #This will make the list of locations for the game
        board = {
            'Study': {'type': 'room', 'adjacent_units': ['Hall1', 'Hall3', 'Kitchen']},
            'Hall1': {'type': 'hallway', 'adjacent_units': ['Study', 'Hall']},
            'Hall': {'type': 'room', 'adjacent_units': ['Hall1', 'Hall4', 'Hall2']},
            'Hall2': {'type': 'hallway', 'adjacent_units': ['Hall', 'Lounge']},
            'Lounge': {'type': 'room', 'adjacent_units': ['Hall2', 'Hall5', 'Conservatory']},
            'Hall3': {'type': 'hallway', 'adjacent_units': ['Study', 'Library']},
            'Hall4': {'type': 'hallway', 'adjacent_units': ['Hall', 'Billiard Room']},
            'Hall5': {'type': 'hallway', 'adjacent_units': ['Lounge', 'Dining Room']},
            'Library': {'type': 'room', 'adjacent_units': ['Hall3', 'Hall6', 'Hall8']},
            'Hall6': {'type': 'hallway', 'adjacent_units': ['Library', 'Billiard Room']},
            'Billiard Room': {'type': 'room', 'adjacent_units': ['Hall4', 'Hall6', 'Hall7', 'Hall9']},
            'Hall7': {'type': 'hallway', 'adjacent_units': ['Billiard Room', 'Dining Room']},
            'Dining Room': {'type': 'room', 'adjacent_units': ['Hall5', 'Hall7', 'Hall10']},
            'Hall8': {'type': 'hallway', 'adjacent_units': ['Library', 'Conservatory']},
            'Hall9': {'type': 'hallway', 'adjacent_units': ['Billiard Room', 'Ballroom']},
            'Hall10': {'type': 'hallway', 'adjacent_units': ['Dining Room', 'Kitchen']},
            'Conservatory': {'type': 'room', 'adjacent_units': ['Lounge', 'Hall8', 'Hall11']},
            'Hall11': {'type': 'hallway', 'adjacent_units': ['Conservatory', 'Ballroom']},
            'Ballroom': {'type': 'room', 'adjacent_units': ['Hall9', 'Hall11', 'Hall12']},
            'Hall12': {'type': 'hallway', 'adjacent_units': ['Ballroom', 'Kitchen']},
            'Kitchen': {'type': 'room', 'adjacent_units': ['Study', 'Hall10', 'Hall12']},
            }
        return board
    
    def changePlayerLocation(self, playerID, location):
        board = self.getLocationList()

        # call self.getPlayerLocation and retrieve player location
        potential_locations = self.find_available_locations(board, self.playerLocations[playerID])

        # Convert to dict for easy lookup
        potential_locations = dict(potential_locations)

        if location in potential_locations :
            self.playerLocations[playerID] = location
        else :
            # TODO: Pop up to let user know they can't move there?
            return 0
        pass

    @staticmethod
    def find_available_locations(board, current_location):
        adjacent_units = board.get(current_location, {}).get('adjacent_units', [])
        adjacent_locations = []

        if adjacent_units:
            for unit in adjacent_units:
                unit_info = board.get(unit, {})
                if unit_info:
                    adjacent_locations.append((unit, unit_info.get('type')))
        
        # this creates a new list of tuples that represents all available locations (omits locations that are hallways for now)
        # Ideally would retrieve that info from database.
        # * Commented out for now, but this will still return the most adjacent rooms/hallways
        # adjacent_locations = [(location, type) for location, type in adjacent_units if type != 'hallway']
        return adjacent_locations
        
    
    def getPlayerLocation(self, playerID):
        return self.playerLocations[playerID]
