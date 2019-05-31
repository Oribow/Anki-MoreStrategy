from morestrategy_too.QItemCollectionSelector import QItemCollectionSelector
from morestrategy_too.QRefilaLineEdit import QRefilaLineEdit
from morestrategy_too.QRefilaFavoriteManager import QRefilaFavoriteManager
from morestrategy_too.QItemInspector import QItemInspector
from morestrategy_too.QComposer import QComposer
from morestrategy_too.GameData import Actor
from morestrategy_too.AmountList import AmountList
from morestrategy_too.Game import Game
from morestrategy_too.QuestManager import *
from data import StrUtil
from PyQt5.Qt import QFrame, QTableView, QLineEdit, QPushButton, QListWidget, QAbstractItemView, \
    QListView, QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import QObject, pyqtSignal

class QTab(QObject):
    tabBecameVisible = pyqtSignal()
    tabBecameHidden = pyqtSignal()

    def __init__(self, tabHost, tabWd):
        QObject.__init__(self)
        self.widget = tabWd
        self.tabIndex = tabHost.indexOf(tabWd)
        self.isActiveTab = tabHost.currentIndex() == self.tabIndex
        tabHost.currentChanged.connect(self.onTabChanged)

    def onTabChanged(self, index):
        if self.tabIndex != index:
            if self.isActiveTab:
                self.isActiveTab = False
                self.tabBecameHidden.emit()
        elif not self.isActiveTab:
            self.isActiveTab = True
            self.tabBecameVisible.emit()


class CollectionViewTab(QTab):

    def __init__(self, tabHost, tabWd):
        QTab.__init__(self, tabHost, tabWd)
        actor = Game.game.gameData.playerActor
        # inspector
        inspWidget = self.widget.findChild(QFrame, "inspector")
        self.inspector = QItemInspector(inspWidget, actor)
        # item collection viewer
        table = self.widget.findChild(QTableView, "item_table")
        self.collectionSelector = QItemCollectionSelector(table, actor, True)
        self.collectionSelector.selectedChanged.connect(self.inspector.inspect)
        # line edit
        line_edit = self.widget.findChild(QLineEdit, "filter_line_edit")
        self.refilaLineEdit = QRefilaLineEdit(self.collectionSelector, line_edit)
        # favs
        favRefilaListWidget = self.widget.findChild(QListWidget, "favorites")
        makeFavBt = self.widget.findChild(QPushButton, "make_favorite_bt")
        self.favMan = QRefilaFavoriteManager("collTab.FavMan", line_edit, favRefilaListWidget, makeFavBt)


class ComposerTab(QTab):

    def __init__(self, tabHost, tabWd):
        QTab.__init__(self, tabHost, tabWd)

        actor = Game.game.gameData.playerActor
        proxyActor = Actor("#proxy", None, None, AmountList(actor.ownedItems))
        # item collection viewer
        composerTable = self.widget.findChild(QTableView, 'tableView2')
        self.collectionSelector = QItemCollectionSelector(composerTable, proxyActor, False)
        self.collectionSelector.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.collectionSelector.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        # composer
        self.composer = QComposer(self, tabWd, self.collectionSelector, actor, proxyActor)


class QuestTab(QTab):

    def __init__(self, tabHost, tabWd):
        QTab.__init__(self, tabHost, tabWd)

        self.questMan = QuestManager()
        questTreeWd = tabWd.findChild(QTreeWidget, "quest_list")
        self.setupQuestTree(self.questMan, questTreeWd)
        self.questInsp = QQuestInspector(tabWd, questTreeWd)

    def setupQuestTree(self, questMan, treeWd):
        activeRoot = QTreeWidgetItem(treeWd, [StrUtil.tStr(StrUtil.QUEST_ACTIVE)])
        for q in questMan.activeQuests:
            item = QTreeWidgetItem(activeRoot, [StrUtil.tStr(q.getTitle())])
            item.setData(0, Qt.UserRole, (q,))
        completedRoot = QTreeWidgetItem(treeWd, [StrUtil.tStr(StrUtil.QUEST_COMPLETED)])
        for q in questMan.finishedQuests:
            item = QTreeWidgetItem(completedRoot, [StrUtil.tStr(q.getTitle())])
            item.setData(0, Qt.UserRole, (q,))
        treeWd.expandItem(activeRoot)
