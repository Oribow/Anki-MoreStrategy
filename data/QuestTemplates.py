from PyQt4.Qt import QObject
from PyQt4.QtCore import pyqtSignal
from morestrategy_too import GlobalEventDistributor as gEvDistr
from morestrategy_too.Game import Game
from morestrategy_too.AmountList import AmountList, fromList

gameData = Game.game.gameData


class BaseQuest(QObject):
    completed = pyqtSignal()

    def __init__(self, stages):
        QObject.__init__(self)
        self.stages = stages

    def activate(self):
        self.currentStage = 0
        self.activateCurrentStage()

    def stageWasCompleted(self):
        self.currentStage += 1
        if self.currentStag >= len(self.stages):
            self.completed.emit()
        else:
            self.activateCurrentStage()

    def activateCurrentStage(self):
        self.stages[self.currentStage].activate()
        self.stages[self.currentStage].stageCompleted.connect(self.stageWasCompleted)

    def deactivate(self):
        pass

    def makeHot(self):
        pass


class QuestStage(QObject):
    completed = pyqtSignal()
    progressChanged = pyqtSignal(int)  # progress in percent

    def __init__(self, title, description, tasks, rewards):
        QObject.__init__(self)
        self.title = title
        self.description = description
        self.tasks = tasks
        if type(rewards) == list:
            rewards = fromList(rewards)
        self.rewards = rewards

    def activate(self):
        for task in self.tasks:
            task.activate()
            task.completed.connect(self.taskWasCompleted)

    def taskWasCompleted(self):
        for t in self.tasks:
            if not t.isCompleted:
                return
        self.deactivate()
        self.completed.emit()

    def deactivate(self):
        for task in self.tasks:
            task.deactivate()


# single task
class QuestTask(QObject):
    completed = pyqtSignal()  # emit when task is completed
    progressChanged = pyqtSignal()  # progress in percent

    def __init__(self, description):
        QObject.__init__(self)
        self.description = description
        self.isCompleted = False

    def activate(self):
        pass

    def deactivate(self):
        pass

    def getDescription(self):
        pass

    def getProgressInPercent(self):
        pass


class CollectXTask(QuestTask):

    def __init__(self, description, requiredAItem):
        QuestTask.__init__(description)
        self.requiredAItem = requiredAItem

    def activate(self):
        gEvDistr.cPlayerActorsItemsChanged(self.playersItemsChanged)
        self.amountActorHas = 0
        self.prevAmountActorHas = 0
        self.isCompleted = False
        self.calcProgress()

    def deactivate(self):
        gEvDistr.dPlayerActorsItemsChanged(self.playersItemsChanged)

    def playersItemsChanged(self, batch):
        if batch[0] == AmountList.CHANGE_COMPLETELY:
            self.calcProgress()
            self.checkForEvents()
        else:
            for b in batch:
                code = b[1]
                aItem = b[0]
                if aItem.item.id != self.requiredAItem.item.id:
                    continue
                if code == AmountList.CHANGE_REMOVED:
                    self.amountActorHas = 0
                    self.checkForEvents()
                elif code == AmountList.CHANGE_AMOUNT or code == AmountList.CHANGE_APPEND:
                    self.amountActorHas = aItem.amount
                    self.checkForEvents()

    def calcProgress(self):
        i = gameData.playerActor.ownedItems.getAItemById(self.requiredAItem.item.id)
        if i is None:
            self.amountActorHas = 0
            self.pProgress = 0
        else:
            self.pProgress = self.onePPoint * i.amount
            self.amountActorHas = i.amount
        self.checkForEvents()

    def checkForEvents(self):
        if self.amountActorHas >= self.requiredAItem.amount:
            self.isCompleted = True
            self.taskCompleted.emit()
        else:
            self.isCompleted = False
            if self.amountActorHas != self.prevAmountActorHas:
                self.prevAmountActorHas = self.amountActorHas


    def getProgressInPercent(self):
        return (self.requiredAItem.amount / self.amountActorHas) * 100
