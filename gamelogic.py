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
            'Study': {'adjacent_units': ['Hall1', 'Hall3', 'Kitchen']},
            'Hall1': {'adjacent_units': ['Study', 'Hall']},
            'Hall': {'adjacent_units': ['Hall1', 'Hall4', 'Hall2']},
            'Hall2': {'adjacent_units': ['Hall', 'Lounge']},
            'Lounge': {'adjacent_units': ['Hall2', 'Hall5', 'Conservatory']},
            'Hall3': {'adjacent_units': ['Study', 'Library']},
            'Hall4': {'adjacent_units': ['Hall', 'Billiard']},
            'Hall5': {'adjacent_units': ['Lounge', 'Dining']},
            'Library': {'adjacent_units': ['Hall3', 'Hall6', 'Hall8']},
            'Hall6': {'adjacent_units': ['Library', 'Billiard']},
            'Billiard': {'adjacent_units': ['Hall4', 'Hall6', 'Hall7', 'Hall9']},
            'Hall7': {'adjacent_units': ['Billiard', 'Dining']},
            'Dining': {'adjacent_units': ['Hall5', 'Hall7', 'Hall10']},
            'Hall8': {'adjacent_units': ['Library', 'Conservatory']},
            'Hall9': {'adjacent_units': ['Billiard', 'Ballroom']},
            'Hall10': {'adjacent_units': ['Dining', 'Kitchen']},
            'Conservatory': {'adjacent_units': ['Lounge', 'Hall8', 'Hall11']},
            'Hall11': {'adjacent_units': ['Conservatory', 'Ballroom']},
            'Ballroom': {'adjacent_units': ['Hall9', 'Hall11', 'Hall12']},
            'Hall12': {'adjacent_units': ['Ballroom', 'Kitchen']},
            'Kitchen': {'adjacent_units': ['Study', 'Hall10', 'Hall12']},
            'ScarletStart': {'adjacent_units': ['Hall2']},
            'MustardStart': {'adjacent_units': ['Hall5']},
            'WhiteStart': {'adjacent_units': ['Hall12']},
            'GreenStart': {'adjacent_units': ['Hall11']},
            'PeacockStart': {'adjacent_units': ['Hall8']},
            'PlumStart': {'adjacent_units': ['Hall3']}
            }
        return board
    
    def findAvailableLocations(self, sessionID, location):
        board = self.getLocationList()

        adjacent_units = board.get(self.playerLocations[sessionID]).get('adjacent_units', [])
        adjacent_locations = []

        if adjacent_units:
            for unit in adjacent_units:
                unit_info = board.get(unit, {})
                if unit_info:
                    adjacent_locations.append((unit))

        # call self.getPlayerLocation and retrieve player location
        potential_locations = adjacent_units
        # self.find_available_locations(board, self.playerLocations[sessionID])
        return potential_locations
        if location in potential_locations :
            self.playerLocations[sessionID] = location
            return 1
        else :
            # TODO: Pop up to let user know they can't move there?
            return 0
        pass

    def setPlayerLocation(self, sessionID, location):
        self.playerLocations[sessionID] = location
        
    def getPlayerLocation(self, playerID):
        return self.playerLocations[playerID]

    def setPlayerStartLocation(self, playerID, location):
        self.playerLocations[playerID] = location