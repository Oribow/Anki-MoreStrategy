'''
Created on Dec 14, 2017

@author: Oribow
'''
from PyQt4.Qt import QApplication
from data import Items
from data.AssetUtil import uiPathToAbs
from PyQt4 import uic
from morestrategy_too.Game import Game
from morestrategy_too.GameData import Actor
from data.Ranks import RankHolder as Ranks
from morestrategy_too.AmountList import AmountList, AmountItem
import os
from data.AssetUtil import savePath
from morestrategy_too.QGameWindow import QGameWindow


def clearAllSaves ():
    filelist = [ f for f in os.listdir(savePath) if f.endswith(".sav") ]
    for f in filelist:
        os.remove(os.path.join(savePath, f))

#clearAllSaves()
app = QApplication([])
game = Game()
if len(game.saves) == 0:
    save = game.createNewSaveState()
else:
    save = game.saves[0]
game.mountSaveState(save)

if len(game.gameData.actors) == 0:
    game.gameData.actors.append(Actor("Felix", Ranks.common, 0, AmountList()))
    #game.gameData.playerActor = game.gameData.actors[0]
    
actor = game.gameData.actors[0]
game.gameData.playerActor = actor
actor.applyStudying(100)
game.logGameState()
#if len(actor.ownedItems) == 0:
for i in Items.items:
    actor.ownedItems.append(AmountItem(i, 1))

mainWindow = QGameWindow("morestrategy_main.ui")

save.discardDataCache()
mainWindow.show()
app.exec_()

#game.saveMountedSaveState()



