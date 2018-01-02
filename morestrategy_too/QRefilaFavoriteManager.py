'''
Created on Dec 22, 2017

@author: Oribow
'''
from PyQt4.Qt import QAbstractItemView, QMenu, pyqtSignal
from PyQt4.QtCore import Qt
from data import Refila
from morestrategy_too.Game import Game


class QRefilaFavoriteManager(object):

    def __init__(self, saverName, filter_line_edit, favListWd, makeFavBt):
        self.saverName = saverName
        self.favListWd = favListWd
        self.filter_line_edit = filter_line_edit
        favListWd.itemSelectionChanged.connect(self.selectedFavChanged)
        favListWd.itemClicked.connect(self.selectedFavChanged)
        favListWd.setContextMenuPolicy(Qt.CustomContextMenu)
        favListWd.customContextMenuRequested.connect(self.favItemShowContextMenu)
        favListWd.setDragEnabled(True)
        favListWd.setDragDropMode(QAbstractItemView.InternalMove)
        favListWd.viewport().setAcceptDrops(True);
        favListWd.setDropIndicatorShown(True)
        makeFavBt.clicked.connect(self.makeFavorite)
        Game.game.currentSaveState.registerSaveUser(self.load, self.save)

    def load(self, data):
        favs = data.get(self.saverName + ".Favs", {})
        self.favListWd.clear()
        for f in favs:
            self.favListWd.addItem(f)

    def save(self, data):
        favs = []
        for i in range(self.favListWd.count()):
            item = self.favListWd.item(i).text()
            favs.append(item)
        data[self.saverName + ".Favs"] = favs

    def selectedFavChanged(self, item=None):
        if item == None:
            item = self.favListWd.currentItem()
        if item == None:
            return
        self.filter_line_edit.setText(item.text())
        self.filter_line_edit.editingFinished.emit()

    def makeFavorite(self):
        text = str(self.filter_line_edit.text())
        if text == "":
            return
        item = self.favListWd.findItems(text, Qt.MatchExactly)
        if len(item) > 0:
            return
        try:
            if not Refila.parser.parse(text):
                return
        except:
            return

        # text is not "" and valid Refila
        self.favListWd.addItem(text)

    def removeSelectedFav(self):
        self.favListWd.takeItem(self.favRefilaListWidget.currentRow())

    def favItemShowContextMenu(self, pos):
        menu = QMenu()
        menu.addAction("Remove", self.removeSelectedFav)
        menu.exec_(self.favListWd.mapToGlobal(pos))
