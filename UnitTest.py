'''
Created on Sep 29, 2017

@author: Oribow
'''
import sys
from random import choice

from PyQt4.QtGui import QApplication

from morestrategy.GameObjects import Actor
from morestrategy.Minions import *
from morestrategy.UI import MainWindow
from morestrategy_too.Game import Game


def getItemByClass (items, iClass):
    for i in items:
        if i.iClass == iClass:
            return i
    
def testMainUI ():
    app = QApplication([])
    game = loadOrCreateGame()
    #giveRandomStuff(5, game.gameData.recipies, game.currentSaveState.actors[0].ownedRecipes)
    testMinionCreation(game, game.currentSaveState.actors[0])
    mainWin = MainWindow(game, game.currentSaveState.actors[0])
    ret = app.exec_()
    game.saveMountedSaveState()
    sys.exit(ret)
    
def testItemGain ():
    app = QApplication([])
    game = Game()
    print("")
    if len(game.gameData.metaSaveStates) < 1:
        save = game.createNewSaveState()
    else:
        save = game.gameData.metaSaveStates[0]
    
    game.mountSaveState(save)
    game.logGameState()
    
    actor = Actor("Felix", game.gameData.ranks[0], 0, [], [], [])
    actor.studyingDropRate = 5
    game.addNewActor(actor)
    game.logGameState()
    game.applyActorsStudying(actor, 100)
    while len(actor.ownedLootBoxes) != 0:
        l = actor.ownedLootBoxes[0]
        for i in range(l[1]):
            game.openActorsLootBox(actor, l[0])
    #game.logGameState()ownedRecipes
    while len(actor.ownedItems) != 0:
        l = actor.ownedItems[0]
        for i in range(l[1]):
            game.recycleActorsItem(actor, l[0])
    game.logGameState()
    game.saveMountedSaveState()
    
    app.exec_()

def testMinionCreation (game, actor):
    #game.logGameState()
    body = getItemByClass(game.gameData.items, Item.BODY)
    head = getItemByClass(game.gameData.items, Item.HEAD)
    arm = getItemByClass(game.gameData.items, Item.ARM)
    leg = getItemByClass(game.gameData.items, Item.LEG)
    weapon = getItemByClass(game.gameData.items, Item.WEAPON)
    aug = getItemByClass(game.gameData.items, Item.AUG)
    armor = getItemByClass(game.gameData.items, Item.ARMOR)
    
    body = convertItemToMinionComp(body)
    head = convertItemToMinionComp(head)
    arm = convertItemToMinionComp(arm)
    leg = convertItemToMinionComp(leg)
    weapon = convertItemToMinionComp(weapon)
    aug = convertItemToMinionComp(aug)
    armor = convertItemToMinionComp(armor)
    
    arm.armor.append(armor)
    head.augments.append(aug)
    arm.weapons.append(weapon)
    
    body.arms.append(arm)
    body.legs.append(leg)
    body.heads.append(head)

    minionA = createMinion(body)
    minionB = createMinion(body)
    print ("A: "+str(minionA))
    print ("B: "+str(minionB))
    
    actor.ownedMinions += [minionA, minionB]
    
    #print ("Fight!")
    #letMinionFightMinion(minionA, minionB)


def loadOrCreateGame ():
    game = Game()
    print("")
    if len(game.gameData.metaSaveStates) < 1:
        save = game.createNewSaveState()
    else:
        save = game.gameData.metaSaveStates[0]
    
    game.mountSaveState(save)
    game.logGameState()
    if len(game.currentSaveState.actors) == 0:
        actor = Actor("Felix", game.gameData.ranks[0], 0, [], [], [], [], [])
        actor.studyingDropRate = 5
        game.addNewActor(actor)
        game.logGameState()
        game.applyActorsStudying(actor, 100)
        while len(actor.ownedLootBoxes) != 0:
            l = actor.ownedLootBoxes[0]
            for i in range(l[1]):
                game.openActorsLootBox(actor, l[0])
        #game.logGameState()
        while len(actor.ownedItems) != 0:
            l = actor.ownedItems[0]
            for i in range(l[1]):
                game.recycleActorsItem(actor, l[0])
        game.logGameState()
        game.applyActorsStudying(actor, 100)
        while len(actor.ownedLootBoxes) != 0:
            l = actor.ownedLootBoxes[0]
            for i in range(l[1]):
                game.openActorsLootBox(actor, l[0])
        game.applyActorsStudying(actor, 100)
        #actor.ownedRecipes.append([game.gameData.recipies[0], 1])
    return game

def giveRandomStuff (amount, stuff, targetList):
    if len(stuff) == 0:
        print("Nothing to randomly give!")
        return
    
    newItems = []
    for a in range(amount):
        newItems.append(choice(stuff))
        print str(newItems[len(newItems) -1])
    giveUnsortedStuffToActor(targetList, newItems)

def printSomeRndMonsterNames ():
    for i in range(20):
        print getRandomMonsterName()

if __name__ == '__main__':
    printSomeRndMonsterNames()
    testMainUI()
    


