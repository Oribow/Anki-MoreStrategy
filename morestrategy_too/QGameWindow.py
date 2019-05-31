'''
Created on Dec 19, 2017

@author: Oribow
'''
from PyQt5.Qt import QWidget, QMainWindow, QLabel, QGraphicsView, QTableView, \
    QTabWidget
from PyQt5 import uic
from data.AssetUtil import uiPathToAbs
from data.StrUtil import fMoneyStr
from morestrategy_too.Game import Game
from morestrategy_too.QComposer import QComposer
from morestrategy_too.Tabs import CollectionViewTab, ComposerTab, QuestTab
from morestrategy_too.QItemCollectionSelector import QItemCollectionSelector



class QGameWindow(QMainWindow):

    def __init__(self, pathToUI):
        QMainWindow.__init__(self)
        uic.loadUi(uiPathToAbs(pathToUI), self)

        tabHost = self.findChild(QTabWidget, 'tabWidget')
        # collection viewer tab
        tabWidget = self.findChild(QWidget, 'manage_items_tab')
        self.collectionTab = CollectionViewTab(tabHost, tabWidget)
        # status bar
        self.actorMoneyLabel = self.findChild(QLabel, "c_actor_money")
        self.setupStatusbar()
        # composer tab
        tabWidget = self.findChild(QWidget, 'composer_tab')
        self.composer = ComposerTab(tabHost, tabWidget)
        # quest tab
        tabWidget = self.findChild(QWidget, "quest_tab")
        self.quests = QuestTab(tabHost, tabWidget)

    def setupStatusbar(self):
        actorName = self.findChild(QLabel, 'c_actor_name')
        actorName.setText(Game.game.gameData.playerActor.name)

        Game.game.gameData.playerActor.moneyChanged.connect(self.updateActorMoney)
        self.updateActorMoney()

    def updateActorMoney(self):
        self.actorMoneyLabel.setText(fMoneyStr(Game.game.gameData.playerActor.money))
