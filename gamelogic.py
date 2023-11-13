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
        pass

    def removePlayer(self, player):
        self.players.remove(player)

    def addPlayer(self, player):
        self.players.append(player)

    def getNumPlayers(self):
        return len(self.players)

class GameInstance:
    def __init__(self, gameID, players):
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
        pass
    
    def changePlayerLocation(self, playerID, location):
        self.playerLocations[playerID] = location
        pass

    def getPlayerLocation(self, playerID):
        return self.playerLocations[playerID]
