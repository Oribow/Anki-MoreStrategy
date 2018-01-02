'''
Created on Oct 9, 2017

@author: Oribow
'''
import datetime
import os
import pickle
import sqlite3

from morestrategy.GameObjects import *
from morestrategy.Minions import MinionStatsModifier
from morestrategy_too.Util import relPathToAbs

class DBHandler(object):

    dbFileName = "game.db"

    def openDB (self):
        self.dbConnection = sqlite3.connect(relPathToAbs(self.dbFileName))
        if self.dbConnection is None:
            return False
        else:
            return True

    def loadGameData (self, minimal = False):
        print("Start loading game data from sqlite db")
        cursor = self.dbConnection.cursor()
        gameData = GameData()
        
        #Load Ranks
        print("")
        print("Loading Ranks:")
        cursor.execute("SELECT * FROM Ranks")
        data = cursor.fetchall()
        gameData.ranks = []
        counter = 1
        for row in data:
            gameData.ranks.append(convertRowIntoRank(row, counter))
            counter += 1

        #Load Ingredients
        print("")
        print("Loading Ingredients:")
        cursor.execute("SELECT * FROM Ingredients")
        data = cursor.fetchall()
        gameData.ingredients = []
        for row in data:
            gameData.ingredients.append(convertRowIntoIngredient(row, gameData.ranks))       

        #Load Items
        print("")
        print("Loading Items:")
        cursor.execute("SELECT * FROM ItemHeads")
        data = cursor.fetchall()
        gameData.aItemList = []
        for row in data:
            gameData.aItemList.append(convertRowIntoItem(cursor, row, gameData.ingredients, gameData.ranks))

        #Load Recipes
        print("")
        print("Loading Recipes:")
        cursor.execute("SELECT * FROM Recipes")
        data = cursor.fetchall()
        gameData.recipies = []
        for row in data:
            gameData.recipies.append(convertRowIntoRecipe(row, gameData.aItemList, gameData.ingredients, gameData.ranks))

        #Load Item Class Names
        print("")
        print("Load Item Class Names:")
        cursor.execute("SELECT * FROM ItemClassNames")
        data = cursor.fetchall()
        gameData.itemClassNames = []
        for row in data:
            print (row[1])
            gameData.itemClassNames.append((row[0], row[1]))

        #Load LootBox
        print("")
        print("Loading LootBoxes:")
        cursor.execute("SELECT * FROM LootBoxes")
        data = cursor.fetchall()
        gameData.lootBoxes = []
        for row in data:
            gameData.lootBoxes.append(convertRowIntoLootbox(row, gameData.aItemList, gameData.ranks))
        
        #Load save states
        print("Loading MetaSaveStates:")
        cursor.execute("SELECT * FROM Saves")
        data = cursor.fetchall()
        gameData.metaSaveStates = []
        for row in data:
            gameData.metaSaveStates.append(convertRowIntoMetaSaveState(row))

        print("")
        print("Finished loading")
        return gameData

    def saveSaveState (self, saveState, metaSaveState):
        if saveState == None or metaSaveState == None:
            return
        
        bytes = pickle.dumps(saveState.toSerializableObject())
        cursor = self.dbConnection.cursor()
        if metaSaveState.slot == -1:
            metaSaveState.lastSaveTime = datetime.datetime.now()
            cursor.execute("INSERT INTO Saves (lastSaveTime, pickle) VALUES (?, ?)", [metaSaveState.lastSaveTime, buffer(bytes)])
            self.dbConnection.commit()
            cursor.execute("SELECT slot FROM Saves WHERE lastSaveTime = ?", [metaSaveState.lastSaveTime])
            data = cursor.fetchone()
            metaSaveState.slot = data[0]
        else:
            cursor.execute("UPDATE Saves SET lastSaveTime = ?, pickle = ? WHERE slot = ?", [datetime.datetime.now(), buffer(bytes), metaSaveState.slot])
            self.dbConnection.commit()
            
    def loadSaveState (self, metaSaveState, gameData):
        if metaSaveState.slot == -1:
            return createNewSaveState()
        
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT * FROM Saves WHERE slot = ?", [metaSaveState.slot])
        data = cursor.fetchone()
        bytes = pickle.loads(str(data[2]))
        return saveStateFromSerializedObject(bytes, gameData)
    
    def close (self):
        self.applyDBUpdates()
        self.dbConnection.close()
        
def convertRowIntoMetaSaveState (row):
    s = MetaSaveState(row[0], row[1])
    print (s)
    return s

def convertRowIntoRank (row, id):
    r = Rank(id, row[0], row[1])
    print r
    return r

def convertRowIntoItem (cursor, row, ingredients, ranks):    
    #item body
    body = loadItemBody(row[4], row[5], cursor)
    
    #ingredients
    ingreList = convertDBList(row[3], True)
    ingreList = replaceIdWithRef(ingreList, ingredients)
    print (strForAmountLists(ingreList))
    
    #stats effects
    stats = loadItemStatsEffects(row[6], cursor)
    
    #Ranks
    rank = next(x for x in ranks if x.id == row[7])

    item =  Item(row[0], row[1], row[2], ingreList, row[4], body, stats, rank, row[8], row[9])
    print(item)
    return item

def loadItemStatsEffects (statsEffectId, cursor):
    if statsEffectId == None or statsEffectId == "":
        return None
    
    cursor.execute("SELECT * FROM StatsEffects WHERE Id="+str(statsEffectId))
    row = cursor.fetchone()
    return MinionStatsModifier(row[1], row[2], row[3], row[4], row[5])

def loadItemBody (itemClass, bodyId, cursor):
    if itemClass == Item.TRASH:
        return ItemNone()
    elif itemClass == Item.BODY:
        cursor.execute("SELECT * FROM BodyItems WHERE Id = "+str(bodyId))
        row = cursor.fetchone()
        return ItemBody(row[4], row[5], row[6], row[1], row[2], row[3])
    elif itemClass == Item.HEAD:
        cursor.execute("SELECT * FROM HeadItems WHERE Id = "+str(bodyId))
        row = cursor.fetchone()
        return ItemBodyPart(row[1], row[2], row[3])
    elif itemClass == Item.ARM:
        cursor.execute("SELECT * FROM ArmItems WHERE Id = "+str(bodyId))
        row = cursor.fetchone()
        return ItemBodyPart(row[1], row[2], row[3])
    elif itemClass == Item.LEG:
        cursor.execute("SELECT * FROM LegItems WHERE Id = "+str(bodyId))
        row = cursor.fetchone()
        return ItemBodyPart(row[1], row[2], row[3])
    elif itemClass == Item.AUG:
        cursor.execute("SELECT * FROM AugmentItems WHERE Id = "+str(bodyId))
        row = cursor.fetchone()
        return ItemAdditional(row[1])
    elif itemClass == Item.WEAPON:
        cursor.execute("SELECT * FROM WeaponItems WHERE Id = "+str(bodyId))
        row = cursor.fetchone()
        return ItemAdditional(row[1])
    elif itemClass == Item.ARMOR:
        cursor.execute("SELECT * FROM ArmorItems WHERE Id = "+str(bodyId))
        row = cursor.fetchone()
        return ItemAdditional(row[1])

def convertRowIntoIngredient (row, ranks):
    #Ranks
    rank = next(x for x in ranks if x.id == row[3])
    
    ingre = Ingredient(row[0], row[1], row[2], rank, row[4], row[5])
    print(ingre)
    return ingre

def convertRowIntoLootbox (row, itemList, ranks):
    #Ranks
    rank = next(x for x in ranks if x.id == row[11])
    
    itemDropRates = convertDBList(row[10], False)
    itemDropRates = replaceIdWithRef(itemDropRates, itemList)
    lb = LootBox(row[0], row[1], row[2], row[8], row[9], row[3], row[4], row[5], row[6], row[7], itemDropRates, rank, row[12], row[13])
    print(lb)
    return lb

def convertRowIntoRecipe (row, itemList, ingredientList, ranks):
    resultItemList = convertDBList(row[3],True)
    resultItemList = replaceIdWithRef(resultItemList, itemList)
    reqItems = convertDBList(row[5], True)
    reqItems = replaceIdWithRef(reqItems, itemList)
    reqIngre = convertDBList(row[4], True)
    reqIngre = replaceIdWithRef(reqIngre, ingredientList)
    
    #Ranks
    rank = next(x for x in ranks if x.id == row[2])
    
    recipe = Recipe(row[0], row[1], rank, resultItemList, reqIngre, reqItems, row[6])
    print(recipe)
    return recipe

def convertDBList (listString, convToInt = False):
    if listString is None:
        return None
    listString = listString.replace(" ", "")
    items = listString.split(",")
    output = []
    for i in items:
        sides = i.split(":")
        for s in range(len(sides)):
            if sides[s].isdigit():
                if not convToInt:
                    sides[s] = float(sides[s])
                else:
                    sides[s] = int(sides[s])
        output.append(tuple(sides))
    return output

def replaceIdWithRef (rawList, matchingRefList):
    resultList = []
    for rawItem in rawList:
        ref = next(x for x in matchingRefList if x.id == rawItem[0])
        resultList.append((ref, rawItem[1]))
    return resultList

class GameData(object):

    ingredients = None
    ranks = None
    alignments = None
    archetypes = None
    aItemList = None
    lootBoxes = None
    saveStates = None

    def getItemById (self, id):
        for item in self.aItemList:
            if item.id == id:
                return item
        print("Couldn't find an item with id "+str(id))
    
    def getSaveState(self, slot):
        for s in self.saveStates:
            if s.slot == slot:
                return s
        print("Couldn't find a slot at "+str(slot))

















