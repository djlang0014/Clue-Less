from gameinfo import *

class Lobby:
    def __init__(self):
        self.players = []
        pass

    def startGame(self):
        #This will have to make a new game instance object
        pass

    def removePlayer(self, player):
        self.players.remove(player)

    def joinLobby(self, player):
        self.players.append(player)

class GameInstance():
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
