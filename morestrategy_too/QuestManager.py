from PyQt5.Qt import QWidget, QMainWindow, QLabel, QGraphicsView, QTableView, \
    QTabWidget, QStandardItemModel
from PyQt5.QtCore import Qt
from QUIFactory import QuestUIFactory
from data.StrUtil import tStr
from data.Quests import quests
from data.QuestTemplates import BaseQuest
from morestrategy_too.Game import Game
from PyQt5.QtCore import pyqtSignal, QAbstractListModel, QVariant, QObject

class QuestManager(QObject):
    activeQuestRemoved = pyqtSignal(BaseQuest)

    def __init__(self):
        QObject.__init__(self)
        Game.game.currentSaveState.registerSaveUser(self.load, self.save)

    def load(self, data):
        self.activeQuests = data.get("QuestMan.ActiveQuests", [])
        self.hotQuests = data.get("QuestMan.hotQuests", [])
        self.finishedQuests = data.get("QuestMan.finishedQuests", [])
        self.coldQuests = data.get("QuestMan.coldQuests", quests)
        if self.coldQuests == quests:
            quest = self.coldQuests.pop(0)
            self.activateQuest(quest)

    def save(self, data):
        data["QuestMan.ActiveQuests"] = self.activeQuests
        data["QuestMan.hotQuests"] = self.hotQuests
        data["QuestMan.finishedQuests"] = self.finishedQuests
        data["QuestMan.coldQuests"] = self.coldQuests

    def makeQuestHot(self, quest):
        pass

    def questCompleted(self, quest):
        quest.completed.disconnect(self.questCompleted)
        self.activeQuestRemoved.emit(quest)
        self.activeQuests.remove(quest)

    def activateQuest(self, quest):
        self.activeQuests.append(quest)
        quest.activate()
        quest.completed.connect(self.questCompleted)


class QQuestListModel(QAbstractListModel):

    def __init__(self, questMan):
        QAbstractListModel.__init__(self)
        self.questMan = questMan
        questMan.activeQuestRemoved.connect(self.activeQuestRemoved)

    def activeQuestRemoved(self, quest):
        self.reset()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.questMan.activeQuests)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        quest = self.questMan.activeQuests[index.row()]
        if role == Qt.DisplayRole:
            return tStr(quest.getListSummary())
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))
        elif role == Qt.UserRole:
            return quest
        return QVariant()


class QQuestInspector(object):

    def __init__(self, tabWd, questTreeWd):
        self.widget = tabWd
        self.summaryTab = tabWd.findChild(QWidget, "tab_summary")
        self.dialogTab = tabWd.findChild(QWidget, "dialog_scroll_contents")
        self.questTreeWd = questTreeWd
        self.currentQuest = None
        questTreeWd.selectionModel().currentChanged.connect(self.selectedQuestChanged)

    def selectedQuestChanged(self, currentIndex, prevIndex):
        treeItem = self.questTreeWd.currentItem()
        if treeItem is None:
            self.currentQuest = None
        else:
            self.currentQuest = treeItem.data(0, Qt.UserRole).toPyObject()[0]
        self.currentQuest.uiNeedsUpdate.connect(self.updateUIForCQuest)
        self.updateUIForCQuest()

    def updateUIForCQuest(self):
        uiFactory = QuestUIFactory()
        uiFactory2 = QuestUIFactory()
        uiFactory.beginUI(self.summaryTab)
        uiFactory2.beginUI(self.dialogTab)
        if self.currentQuest is not None and self.currentQuest.isActive:
            self.currentQuest.onDrawSummary(uiFactory)
            self.currentQuest.onDrawDialog(uiFactory2)

        uiFactory2.space()
        uiFactory2.endUI()
        uiFactory.endUI()
