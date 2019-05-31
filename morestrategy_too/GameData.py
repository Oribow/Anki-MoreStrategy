'''
Created on Dec 19, 2017

@author: Oribow
'''
from data.StrUtil import tStr
from PyQt5.QtCore import pyqtSignal, QObject
import random
from data.Items import items
from data.ItemTemplates import LootBox
from morestrategy_too.AmountList import AmountItem


class GameData(object):

    def __init__(self, saver):
        saver.registerSaveUser(self.load, self.save)

    def save(self, data):
        data["GameData.Actors"] = self.actors
        data["GameData.PlayerActorIndex"] = self.actors.index(self.playerActor)

    def load(self, data):
        self.actors = data.get("GameData.Actors", [])
        index = data.get("GameData.PlayerActorIndex", -1)
        if index != -1:
            self.playerActor = self.actors[index]


class Actor(QObject):
    moneyChanged = pyqtSignal(int)

    studyingDropRate = 30

    def __init__(self, name, rank, money, ownedItems):
        QObject.__init__(self)
        self.name = name
        self.rank = rank
        self.money = money
        self.ownedItems = ownedItems

    def applyStudying(self, studiedCards):
        for iCard in range(0, studiedCards):
            if random.random() * 100 >= 100 - self.studyingDropRate:
                # drop a box
                x = 1 + random.random() - 0.5
                boxesThatMatter = []
                sum = 0
                for item in items:
                    if not issubclass(type(item), LootBox):
                        continue
                    y = item.getDropProbabilityAt(x)
                    if y > 0:
                        boxesThatMatter.append(item)
                        sum += y
                if sum == 0:
                    print("    No lootbox found at " + str(x))
                    continue
                rnd = random.random() * sum
                sum = 0
                for item in items:
                    if not issubclass(type(item), LootBox):
                        continue
                    sum += item.getDropProbabilityAt(x)
                    if sum >= rnd:
                        self.ownedItems.append(AmountItem(item, 1))
                        break

    def changeMoney(self, amount):
        self.money += amount
        self.moneyChanged.emit(amount)

    def __str__(self):
        s = self.name + "(" + str(self.rank) + "):"
        if len(self.ownedItems) == 0:
            s += "\n    No Items"
        else:
            s += ("\n    Items:")
            s += ("\n        " + tStr(self.ownedItems))
        s += "\n------------------------------------------"
        return s

    def __getstate__(self):
        return (self.name, self.rank, self.money, self.ownedItems)

    def __setstate__(self, state):
        self.name = state[0]
        self.rank = state[1]
        self.money = state[2]
        self.ownedItems = state[3]

    def __reduce__(self):
        tupl = (self.__class__, self.__getstate__())
        return tupl
