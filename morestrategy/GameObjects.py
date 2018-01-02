'''
Created on Oct 17, 2017

@author: Oribow
'''

from PyQt4.Qt import QColor


class Rank (object):
    def __init__ (self, id, name, notifyColorStr):
        self.id = id
        self.name = name
        self.notifyColor = QColor.fromRgb(int(notifyColorStr, 16))
        
    def __str__(self, *args, **kwargs):
        return str(self.id)+ ": "+self.name

class LootBox (object):

    def __init__ (self, id, name, description, minItemDrop, maxItemDrop,
                 probFuncFalloff, probFuncOrign, probFuncHeight,
                 probFuncCutOffLeft, probFuncCutOffRight, itemDropProbList, rank, notifyImgRes,
                 unitValue):

        self.id = id
        self.name = name
        self.description = description
        self.minItemDrop = minItemDrop
        self.maxItemDrop = maxItemDrop
        self.probFuncFalloff = probFuncFalloff
        self.probFuncOrign = probFuncOrign
        self.probFuncHeight = probFuncHeight
        self.probFuncCutOffLeft = probFuncCutOffLeft
        self.probFuncCutOffRight = probFuncCutOffRight
        self.itemDropProbList = itemDropProbList
        self.rank = rank
        self.notifyImgRes = notifyImgRes
        self.unitValue = unitValue

    def __str__(self, *args, **kwargs):
        return "(id: "+str(self.id)+", name: \""+str(self.name)+"\")"

    def getDropProbabilityAt (self, x):
        if self.probFuncCutOffLeft != 0:
            x = max(x, self.probFuncCutOffLeft)
        if self.probFuncCutOffRight != 0:
            x = min(x, self.probFuncCutOffRight)
        return max(0, self.probFuncFalloff * pow(x + self.probFuncOrign,2)+self.probFuncHeight)

    def getItemByChance(self, rand):
        for i in self.itemDropProbList:
            rand -= i[1]
            if rand <= 0:
                return i[0]

class MetaSaveState (object):

    def __init__ (self, slot, lastSaveTime):
        self.slot = slot
        self.lastSaveTime = lastSaveTime
        
    def __str__(self, *args, **kwargs):
        return "({}, {})".format(self.slot, self.lastSaveTime)

class SaveState (object):

    def __init__ (self, actors):
        self.actors = actors
        
    def toSerializableObject (self):
        s = []
        for a in self.actors:
            s.append([
                a.name,
                a.rank.id,
            [(item[0].id, item[1]) for item in a.ownedItems],
            [(ingre[0].id, ingre[1])for ingre in a.ownedIngrediences],
            [(lb[0].id, lb[1]) for lb in a.ownedLootBoxes],
            [(re[0].id, re[1]) for re in a.ownedRecipes],
            [min for min in a.ownedMinions],
            a.money
            ])
        return s
    
def saveStateFromSerializedObject (obj, gameData):
    actors = []
    for a in obj:
        name = a[0]
        rank = next(x for x in gameData.ranks if x.id == a[1])
        money = a[7]
        items = []
        for item in a[2]:
            items.append([next(x for x in gameData.aItemList if x.id == item[0]), item[1]])
        ingres = []
        for ingre in a[3]:
            ingres.append([next(x for x in gameData.ingredients if x.id == ingre[0]), ingre[1]])
        lbs = []
        for lb in a[4]:
            lbs.append([next(x for x in gameData.lootBoxes if x.id == lb[0]), lb[1]])
        res = []
        for re in a[5]:
            res.append([next(x for x in gameData.recipies if x.id == re[0]), re[1]])
        mins = []
        for min in a[6]:
            mins.append(min)
        actors.append(Actor(name, rank, money, items, ingres, lbs, res, mins))
    return SaveState(actors)

class Actor (object):
    studyingDropRate = 0
    lootRank = 1

    def __init__ (self, name, rank, money, ownedItems, ownedIngrediences, ownedLootBoxes,
                  ownedRecipes, ownedMinions):
        self.name = name
        self.rank = rank
        self.money = money
        self.ownedItems = ownedItems #(box, amount)
        self.ownedIngrediences = ownedIngrediences #(ingredient, amount)
        self.ownedLootBoxes = ownedLootBoxes #(box, amount)
        self.ownedRecipes = ownedRecipes
        self.ownedMinions = ownedMinions

    def __str__(self, *args, **kwargs):
        s = self.name+"("+str(self.rank)+"):"
        if len(self.ownedLootBoxes) == 0:
            s+= "\n    No Lootboxes"
        else:
            s+= "\n    LootBoxes:"
            for box in self.ownedLootBoxes:
                s+= ("\n        "+str(box[0])+" x"+str(box[1]))
        if len(self.ownedItems) == 0:
            s+= "\n    No Items"
        else:
            s+=("\n    Items:")
            for item in self.ownedItems:
                s+= ("\n        "+str(item[0])+" x"+str(item[1]))
        if len(self.ownedIngrediences) == 0:
            s+= "\n    No Ingrediences"
        else:
            s+=("\n    Ingrediences:")
            for ingre in self.ownedIngrediences:
                s+= ("\n        "+str(ingre[0])+" x"+str(ingre[1]))
        s+="\n------------------------------------------"
        return s

class Item (object):
    #item Classes
    TRASH, BODY, HEAD, ARM, LEG, AUG, WEAPON, ARMOR = range (1, 9)

    def __init__ (self, id, name, description, ingredients, iClass, itemBody, statsEffect, rank, imgResPath, unitValue):
        self.id = id
        self.name = name
        self.description = description
        self.itemBody = itemBody
        self.ingredients = ingredients
        self.iClass = iClass
        self.statsEffect = statsEffect
        self.rank = rank
        self.imgResPath = imgResPath
        self.unitValue = unitValue

    def __str__(self, *args, **kwargs):
        return "(id: "+str(self.id)+", name: \""+str(self.name)+"\")"

class ItemBodyPart (object):

    def __init__(self, augSlots, weaponSlots, armorSlots):
        self.augSlots = augSlots
        self.weaponSlots = weaponSlots
        self.armorSlots = armorSlots
    
    def getSlotValueString (self):
        return "Aug {}, Weapon {}, Armor {}".format(self.augSlots, self.weaponSlots, self.armorSlots)

    def getSlotLabelString (self):
        return "Slots:"

class ItemBody (ItemBodyPart):

    def __init__ (self, augSlots, weaponSlots, armorSlots, headSlots, armSlots, legSlots):
        ItemBodyPart.__init__(self, augSlots, weaponSlots, armorSlots)
        self.headSlots = headSlots
        self.armSlots = armSlots
        self.legSlots = legSlots
        
    def getSlotValueString (self):
        return "Head {}, Arm {}, Leg {}, ".format(self.headSlots, self.armSlots, self.legSlots) + ItemBodyPart.getSlotString(self)

class ItemAdditional (object):

    def __init__(self, equipableInSlots):
        self.equipableInSlots = equipableInSlots
        
    def getSlotValueString (self):
        res = ""
        if "2" in self.equipableInSlots:
            res += "Body, "
        if "3" in self.equipableInSlots:
            res += "Head, "
        if "4" in self.equipableInSlots:
            res += "Arm, "
        if "5" in self.equipableInSlots:
            res += "Leg, "
        if res == "":
            res = "None"
        else:
            res = res[0:-2]
        return res
    
    def getSlotLabelString (self):
        return "Equip. Slots:"

class ItemNone (object):

    def __init__(self):
        pass
    
    def getSlotValueString (self):
        return ""
    
    def getSlotLabelString (self):
        return ""

class Ingredient (object):

    def __init__(self, id, name, description, rank, unitValue, imgResPath):
        self.id = id
        self.name = name
        self.description = description
        self.rank = rank
        self.unitValue = unitValue
        self.imgResPath = imgResPath

    def __str__ (self):
        return "(id: "+str(self.id)+", name: \""+str(self.name)+"\", "+str(self.unitValue)+"$)"

class Recipe (object):

    def __init__ (self, id, name, rank, resultItems, reqIngre, reqItems, unitValue):
        self.resultItems = resultItems
        self.id = id
        self.rank = rank
        self.name = name
        self.reqItems = reqItems
        self.reqIngre = reqIngre
        self.unitValue = unitValue

    def __str__(self, *args, **kwargs):
        return "("+strForAmountLists(self.resultItems)+"): reqItems: ("+strForAmountLists(self.reqItems)+"), reqIngre: ("+strForAmountLists(self.reqIngre)+")"

def createNewSaveState ():
    return SaveState([])



