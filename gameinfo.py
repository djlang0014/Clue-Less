from gamelogic import *

class Location:
    def __init__(self, locName, type, maxOccupants = 1, accessibleLocs = None, charactersPresent = []):
        self.locName = locName
        self.type = type
        self.maxOccupants = maxOccupants
        self.accessibleLocs = accessibleLocs
        self.charactersPresent = charactersPresent
    
    def setCharacterPresent(self, character):
        self.charactersPresent.append(character)

    def removeCharacterPresent(self, character):
        self.charactersPresent.remove(character)

    def checkBoard(self):
        pass

    def updateBoard(self):
        pass

class Player:
    def __init__(self, name, playerID):
        self.name = name
        self.playerID = playerID
        self.character = None
        self.cards = [] #Cards will be set in driver code
        self.maySuggest = True
        self.mayEndTurn = False

    #This will be overloaded 
    def sendAction(self):
        pass

    def selectCharacter(self, character):
        #I switched to having character set here as it makes more sense codewise
        self.character = character

    def sendMessage(self, Player, message):
        #This will send the message to a specified player
        pass

    def getPlayerCards(self):
        #This will return the cards the player has
        pass

class Card:
    def __init__(self, cardType, cardName, cardID):
        self.cardType = cardType
        self.cardName = cardName
        self.cardID = cardID
        self.cardOwner = None

    def setCardOwner(self, player):
        self.cardOwner = player

class DBAccess:
    def __init__(self, db):
        self.db = db

    def getCardList(self):
        #This will get the list of cards from the database
        pass

    def getLocationList(self):
        #This will get the list of locations from the database
        pass

class CaseFile:
    def __init__(self):
        self.suspect = None
        self.weapon = None
        self.room = None

    def generateCaseFile(self, GameInstance):
        #This will generate the case file for the game
        pass

    def checkAccusation(self, suspect, weapon, room):
        #This will check the accusation against the case file
        #returns True/False for right/wrong
        pass