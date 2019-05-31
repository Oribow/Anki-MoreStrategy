'''
Created on Dec 14, 2017

@author: Oribow
'''
from data.StrUtil import tStr
from data.AssetUtil import resPathToAbs
from PyQt5.Qt import QLabel, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, \
    QFormLayout, QSizePolicy, QPixmap
from PyQt5.QtCore import Qt
from morestrategy_too.AmountList import AmountList
from morestrategy_too.QUIFactory import ItemInspectorUIFactory


class QItemInspector(object):

    def __init__(self, parentWidget, actor):
        self.graphicsViewWd = parentWidget
        self.uiFactory = ItemInspectorUIFactory(self.buttonClicked)
        self.actor = actor
        self.inspectedAItem = None

        actor.ownedItems.aItemChanged.connect(self.actorsItemsChanged)

    def inspect(self, aItem=None):
        if aItem == None or not aItem.isValid():
            self.inspectedAItem = aItem
            self.uiFactory.clearUI()

        elif aItem == self.inspectedAItem:
            return

        else:
            self.uiFactory.beginUI(self.graphicsViewWd)
            aItem.item.onInspectorGUI(self.uiFactory)
            self.uiFactory.endUI()
            self.inspectedAItem = aItem

    def actorsItemsChanged(self, batch):
        if self.inspectedAItem == None:
            return

        if batch[0] == AmountList.CHANGE_COMPLETELY:
            self.inspect()
            return
        for b in batch:
            code = b[1]
            aItem = b[0]
            if aItem.item.id != self.inspectedAItem.item.id:
                return
            if code == AmountList.CHANGE_REMOVED:
                self.inspect()
            elif code == AmountList.CHANGE_AMOUNT:
                self.inspect(aItem)

    def buttonClicked(self, func):
        func(self.inspectedAItem, self.actor)
