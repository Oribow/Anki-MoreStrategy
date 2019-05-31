from PyQt5.QtCore import pyqtSignal, Qt, QObject
from morestrategy_too import GlobalEventDistributor as gEvDistr
from morestrategy_too.Game import Game
from morestrategy_too.AmountList import AmountList, fromList
from data.StrUtil import tStr


class BaseQuest(QObject):
    completed = pyqtSignal(QObject)
    uiNeedsUpdate = pyqtSignal()

    def __init__(self, stages):
        QObject.__init__(self)
        self.stages = stages
        self.isActive = False

    def activate(self):
        self.currentStage = 0
        self.activateCurrentStage()
        self.isActive = True

    def stageWasCompleted(self):
        self.currentStage += 1
        if self.currentStage >= len(self.stages):
            self.completed.emit(self)
            self.deactivate()
            self.uiNeedsUpdate.emit()
        else:
            self.activateCurrentStage()

    def stageProgressChanged(self):
        self.uiNeedsUpdate.emit()

    def activateCurrentStage(self):
        self.stages[self.currentStage].completed.connect(self.stageWasCompleted)
        self.stages[self.currentStage].progressChanged.connect(self.stageProgressChanged)
        self.stages[self.currentStage].activate()

    def deactivate(self):
        self.isActive = False

    def makeHot(self):
        pass

    def onDrawSummary(self, uiFactory):
        self.stages[self.currentStage].onDrawSummary(uiFactory)

    def onDrawDialog(self, uiFactory):
        for i in range(self.currentStage + 1):
            self.stages[i].onDrawDialog(uiFactory)

    def getListSummary(self):
        return self.stages[self.currentStage].getListSummary()

    def getTitle(self):
        return self.stages[self.currentStage].getTitle()

class QuestStage(QObject):
    completed = pyqtSignal()
    progressChanged = pyqtSignal(int)  # progress in percent
    dialogsChanged = pyqtSignal()

    def __init__(self, title, description, tasks, rewards, dialogs):
        QObject.__init__(self)
        self.title = title
        self.description = description
        self.tasks = tasks
        self.isActive = False
        self.dialogs = dialogs
        self.activeDialogs = []
        self.taskCompletitionChangedFlag = False
        if type(rewards) == list:
            rewards = fromList(rewards)
        self.rewards = rewards

    def activate(self):
        self.finishedTasks = 0
        self.overallTaskProgress = 0
        self.isCompleted = False
        self.isActive = True
        for task in self.tasks:
            task.completionChanged.connect(self.taskCompletionChanged)
            task.progressChanged.connect(self.taskProgressChanged)
            task.activate(self)
        self.checkDialogTrigger()

    def taskCompletionChanged(self, task):
        self.taskCompletitionChangedFlag = True
        if task.isCompleted:
            self.finishedTasks += 1
            if not task.remainsHot:
                task.deactivate()
        else:
            self.finishedTasks -= 1
        self.checkDialogTrigger()

    def checkForCompletion(self):
        if not self.isActive:
            return
        if not self.taskCompletitionChangedFlag:
            return
        else:
            self.taskCompletitionChangedFlag = False

        self.checkDialogTrigger()

        if self.finishedTasks == len(self.tasks):
            self.isCompleted = True
            self.deactivate()
            self.completed.emit()
            self.checkDialogTrigger()

    def taskProgressChanged(self, task, oldProgress):
        self.overallTaskProgress -= oldProgress
        self.overallTaskProgress += task.progressInPercent
        self.progressChanged.emit(self.overallTaskProgress / len(self.tasks))
        self.checkDialogTrigger()

    def deactivate(self):
        self.isActive = False
        for task in self.tasks:
            task.deactivate()

    def onDrawSummary(self, uiFactory):
        uiFactory.title(self.title)
        uiFactory.space(5)
        uiFactory.label(self.description)
        uiFactory.tasks(self.tasks)

    def onDrawDialog(self, uiFactory):
        for d in self.activeDialogs:
            d.drawDialog(uiFactory)

    def getListSummary(self):
        return self.title

    def getQuestProgress(self):
        return self.overallTaskProgress / len(self.tasks)

    def checkDialogTrigger(self):
        aD = []
        for d in self.dialogs:
            if d.becomesActive(self):
                aD.append(d)
        for d in aD:
            self.dialogs.remove(d)
            self.activeDialogs.append(d)
        if len(aD) != 0:
            self.dialogsChanged.emit()

    def getTitle(self):
        return self.title

# single task
class QuestTask(QObject):
    completionChanged = pyqtSignal(QObject)  # emit when task is completed
    progressChanged = pyqtSignal(QObject, int)  # task, prev progress in percent

    def __init__(self, description, remainsHot):
        QObject.__init__(self)
        self.description = description
        self.isCompleted = False
        self.remainsHot = remainsHot
        self.isActive = False
        self.progressInPercent = 0

    def activate(self):
        self.isActive = True

    def deactivate(self):
        self.isActive = False

    def getTaskString(self):
        pass


class CollectXTask(QuestTask):

    def __init__(self, description, requiredAItem, remainsHot=False):
        QuestTask.__init__(self, description, remainsHot)
        self.requiredAItem = requiredAItem
        self.remainsHot = remainsHot

    def activate(self, questStage):
        if self.isActive:
            return
        QuestTask.activate(self)
        gEvDistr.cPlayerActorsItemsChanged(self.playersItemsChanged)
        gEvDistr.cAfterPlayerActorsItemsChanged(self.afterPlayersItemsChanged)
        self.questStage = questStage
        self.prevAmountActorHas = 0
        self.isCompleted = False
        self.playersItemsChanged([AmountList.CHANGE_COMPLETELY])
        self.checkForEvents()

    def deactivate(self):
        if not self.isActive:
            return
        QuestTask.deactivate(self)
        gEvDistr.dPlayerActorsItemsChanged(self.playersItemsChanged)
        gEvDistr.dAfterPlayerActorsItemsChanged(self.afterPlayersItemsChanged)

    def playersItemsChanged(self, batch):
        if batch[0] == AmountList.CHANGE_COMPLETELY:
            i = Game.game.gameData.playerActor.ownedItems.getAItemById(self.requiredAItem.item.id)
            if i is None:
                self.calcProgress(0)
            else:
                self.calcProgress(i.amount)
        else:
            for b in batch:
                code = b[1]
                aItem = b[0]
                if aItem.item.id != self.requiredAItem.item.id:
                    continue
                if code == AmountList.CHANGE_REMOVED:
                    self.calcProgress(0)
                elif code == AmountList.CHANGE_AMOUNT or code == AmountList.CHANGE_APPEND:
                    self.calcProgress(aItem.amount)
        self.checkForEvents()

    def afterPlayersItemsChanged(self):
        self.questStage.checkForCompletion()

    def calcProgress(self, amount):
        self.amountActorHas = amount
        self.progressInPercent = (self.amountActorHas / self.requiredAItem.amount) * 100

    def checkForEvents(self):
        if self.amountActorHas >= self.requiredAItem.amount:
            self.isCompleted = True
            self.prevAmountActorHas = self.amountActorHas
            self.completionChanged.emit(self)
            self.progressChanged.emit(self, 100)
        else:
            self.isCompleted = False
            if self.amountActorHas != self.prevAmountActorHas:
                self.progressChanged.emit(self, (self.prevAmountActorHas / self.requiredAItem.amount) * 100)
                self.prevAmountActorHas = self.amountActorHas

    def getTaskString(self):
        if self.isCompleted:
            return tStr(self.description) + " (Check)"
        else:
            return tStr(self.description) + " ({}/{})".format(self.amountActorHas, self.requiredAItem.amount)


class Dialog(object):
    # Some basic Dialog triggers
    TRIG_QUEST_IS_ACTIVE, TRIG_QUEST_COMPLETED, TRIG_QUEST_PROGRESS_HIGHER_EQ_THEN = range(3)

    def __init__(self, speakers, dialog, questTrigger=TRIG_QUEST_IS_ACTIVE, addTriggerData=None):
        self.dialog = dialog  # [[speaker-id, textA, textB,...], ...]
        self.speakers = speakers
        self.questTrigger = questTrigger
        self.addTriggerData = addTriggerData

    def drawDialog(self, uiFactory):
        for d in self.dialog:
            s = next(x for x in self.speakers if x.id == d[0])
            uiFactory.dialog(s, d[1:])

    def becomesActive(self, quest):
        if self.questTrigger == self.TRIG_QUEST_IS_ACTIVE:
            if quest.isActive:
                return True
            return False
        elif self.questTrigger == self.TRIG_QUEST_COMPLETED:
            if quest.isCompleted:
                return True
            return False
        elif self.questTrigger == self.TRIG_QUEST_PROGRESS_HIGHER_EQ_THEN:
            if quest.getQuestProgress() >= self.addTriggerData:
                return True
            return False
        return False


class Speaker(object):

    def __init__(self, id, name, pathToAvatar, textAlign=Qt.AlignLeft):
        self.id = id
        self.name = name
        self.pathToAvatar = pathToAvatar
        self.textAlign = textAlign
