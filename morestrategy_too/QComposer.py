'''
Created on Dec 20, 2017

@author: Oribow
'''
from PyQt4.Qt import QGraphicsView, QGraphicsItemGroup, QGraphicsRectItem, \
    QGraphicsItem, QBrush, QGraphicsScene, QGraphicsLineItem, QPixmap, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QSlider, QGraphicsEllipseItem, \
    QSpinBox, QAbstractItemView, QItemSelectionModel, \
    QPushButton, QTableView, pyqtSignal
from PyQt4.QtCore import Qt

from data.AssetUtil import resPathToAbs
from data.ItemTemplates import ComposeableItem
from data.Refila import ConstFilter
from morestrategy_too.AmountList import AmountList, AmountItem, copyInPlace
from morestrategy_too.GameData import Actor
from morestrategy_too.QItemCollectionSelector import QItemCollectionSelector
from morestrategy_too.QUIFactory import ComposerItemUIFactory
import math

ITEM_SIZE = 100
ITEM_SIZE_HALF = ITEM_SIZE / 2
ITEM_SPACE = 10
INDICATOR_SIZE = math.sqrt(2 * ITEM_SIZE ** 2)
INDICATOR_OFFSET = ITEM_SIZE - (INDICATOR_SIZE - ITEM_SIZE) / 2


class QComposer(object):

    def __init__(self, tab, tabWd, collectionSelector, actor, proxyActor):
        self.proxyActor = proxyActor
        self.actorsItemsChanged = False

        self.scene = QGraphicsScene()
        self.scene.selectionChanged.connect(self.gItemSelectionChanged)
        self.selectionIndicator = QGraphicsEllipseItem(-100, -100, INDICATOR_SIZE, INDICATOR_SIZE)
        self.scene.addItem(self.selectionIndicator)
        TreeItem.scene = self.scene
        TreeItem.changeAmountCallback = self.changeAmount
        TreeItem.uiFactory = ComposerItemUIFactory(self.scene)

        self.collectionSelector = collectionSelector
        collectionSelector.selectedChanged.connect(self.aItemSelectionChanged)

        self.targetActor = actor
        actor.ownedItems.aItemChanged.connect(self.targetActorsItemChanged)

        self.graphicsViewWd = tabWd.findChild(QGraphicsView, 'composer_view')
        self.graphicsViewWd.setScene(self.scene)

        self.tab = tab
        tab.tabBecameVisible.connect(self.tabBecameVisible)

        tabWd.findChild(QPushButton, "make_bt").clicked.connect(self.makeClicked)
        tabWd.findChild(QPushButton, "autofill_bt").clicked.connect(self.autofillClicked)
        tabWd.findChild(QPushButton, "clear_bt").clicked.connect(self.clearClicked)

        self.gItemSelectionChanged()
        self.rootGItem = TreeItem()
        self.rootGItem.drawCached()

    def tabBecameVisible(self):
        if self.actorsItemsChanged:
            self.updateProxyActorsItems()

    def targetActorsItemChanged(self, batch):
        if not self.tab.isActiveTab:
            self.actorsItemsChanged = True
        else:
            self.updateProxyActorsItems()

    def updateProxyActorsItems(self):
        # copy inplace
        copyInPlace(self.targetActor.ownedItems, self.proxyActor.ownedItems)
        self.proxyActor.ownedItems.startBatch()
        self.applyItemUpdate(self.rootGItem)
        self.rootGItem.drawCached()
        self.proxyActor.ownedItems.clearBatch()

    def applyItemUpdate(self, gItem):
        if gItem.aItem == None:
            return
        i = self.proxyActor.ownedItems.getAItemById(gItem.aItem.item.id)
        if i == None:
            gItem.clear(None, TreeItem.CLEAR_IGNORE)
            return
        gItem.takePreferredAmountOfItem(self.proxyActor, i)
        for c in gItem.children:
            self.applyItemUpdate(c)

    def gItemSelectionChanged(self):
        gItems = self.scene.selectedItems()
        if len(gItems) == 0:
            self.collectionSelector.setConstantPreFilter(ConstFilter(False))
            self.selectionIndicator.hide()
        else:
            gItem = gItems[0]
            self.selectionIndicator.show()
            self.selectionIndicator.setPos(gItem.x + INDICATOR_OFFSET, gItem.y + INDICATOR_OFFSET)
            if gItem.aItem != None:
                m = self.collectionSelector.tableModel
                for i in range(len(m.filteredAItemList)):
                    if gItem.aItem == m.filteredAItemList[i]:
                        # self.collectionSelector.tableView.setCurrentIndex(self.collectionSelector.proxyModel.mapFromSource(m.index(i, 0)))
                        self.collectionSelector.tableView.selectionModel().select(
                            self.collectionSelector.proxyModel.mapFromSource(m.index(i, 0)),
                            QItemSelectionModel.SelectCurrent)
                        break

            self.collectionSelector.setConstantPreFilter(self.getFilterForGItem(gItem))

    def aItemSelectionChanged(self, aItem):
        if aItem == None or not aItem.isValid():
            return
        gItems = self.scene.selectedItems()
        if len(gItems) == 0:
            return
        else:
            gItem = gItems[0]
            gItem.setAItem(aItem, self.proxyActor)

    def getFilterForGItem(self, gItem):
        if gItem.parent == None:
            return RootFilter(gItem.aItem)
        else:
            return ItemFuncFilter(gItem)

    def changeAmount(self, gItem, amount):
        if amount < 1:
            return

        amount -= gItem.aItem.amount
        if amount == 0:
            return

        if amount < 0:
            if gItem.aItem.item.amount + amount < 0:
                amount = -(gItem.aItem.item.amount - 1)
            self.proxyActor.ownedItems.append(AmountItem(gItem.aItem.item, amount * -1))
            gItem.aItem.amount += amount
        else:
            i = self.proxyActor.ownedItems.getAItemById(gItem.aItem.item.id)
            if amount > i.amount:
                amount = i.amount

            self.proxyActor.ownedItems.remove(AmountItem(gItem.aItem.item, amount))
            gItem.aItem.amount += amount

    def makeClicked(self):
        if not self.rootGItem.isValidComposition():
            return
        self.targetActor.ownedItems.startBatch()
        result = AmountList()
        self.rootGItem.createComposition(result)
        self.targetActor.ownedItems.addAmountList(result)
        aItem = self.rootGItem.aItem
        self.rootGItem.clear(self.targetActor, TreeItem.CLEAR_REMOVE)
        self.targetActor.ownedItems.endBatch()
        i = self.proxyActor.ownedItems.getAItemById(aItem.item.id)
        self.rootGItem.setAItem(i, self.proxyActor)
        self.rootGItem.drawCached()

    def clearClicked(self):
        self.targetActor.ownedItems.startBatch()
        self.rootGItem.clear(self.proxyActor, TreeItem.CLEAR_RECYCLE)
        self.targetActor.ownedItems.endBatch()
        self.rootGItem.drawCached()

    def autofillClicked(self):
        if self.rootGItem.aItem is None:
            return
        self.autofill(self.rootGItem)
        self.rootGItem.drawCached()

    def autofill(self, gItem):
        if gItem.aItem == None and (gItem.parent == None or gItem.parent.aItem.item.allowAutoFill):
            filter = self.getFilterForGItem(gItem)
            vI = next((x for x in self.proxyActor.ownedItems if filter.isValidItem(x)), None)
            if vI == None:
                return
            gItem.setAItem(vI, self.proxyActor)

        for c in gItem.children:
            self.autofill(c)


class TreeItem(QGraphicsItemGroup):
    CLEAR_RECYCLE, CLEAR_REMOVE, CLEAR_IGNORE = range(3)

    scene = None
    changeAmountCallback = None
    uiFactory = None

    def __init__(self, parent=None):
        QGraphicsItemGroup.__init__(self)
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.parent = parent
        TreeItem.scene.addItem(self)
        self.aItem = None
        self.lineCache = []
        self.children = []
        # cached draw params
        self.x = 0
        self.y = 0
        self.nextDown = False

    def setAItem(self, aItem, proxyActor):
        if aItem == self.aItem:
            return
        proxyActor.ownedItems.startBatch()
        if self.aItem != None:
            self.clear(proxyActor, self.CLEAR_RECYCLE)

        if aItem != None:
            self.takePreferredAmountOfItem(proxyActor, aItem)
            # handle children
            if issubclass(type(self.aItem.item), ComposeableItem):
                reqChildCount = self.aItem.item.getChildCount(self.getChildAItems())
            else:
                reqChildCount = 0
            self.updateChildCount(reqChildCount)
        self.drawCached()
        if self.parent != None:
            self.parent.childItemChanged()
        proxyActor.ownedItems.endBatch()

    def childItemChanged(self):
        cc = self.aItem.item.getChildCount(self.getChildAItems())
        if len(self.children) != cc:
            self.updateChildCount(cc)
            self.drawCached()

    def updateChildCount(self, newChildCount):
        orgChildCount = len(self.children)
        while len(self.children) < newChildCount:
            self.children.append(TreeItem(self))
        for i in range(orgChildCount):
            self.children[i].show()
        for i in range(newChildCount, len(self.children)):
            self.children[i].hide()

    def drawCached(self):
        self.draw(self.nextDown, self.x, self.y)

    def draw(self, nextDown, x, y):
        self.nextDown = nextDown
        self.x = x
        self.y = y

        # remove old stuff
        for c in self.childItems():
            c.setParentItem(None)
        # just draw me at x, y
        self.setPos(x, y)
        # if self.isDrawingDirty:

        self.drawBase()
        if self.aItem != None:
            self.uiFactory.beginRootLayout(x, y, ITEM_SIZE, self)
            self.aItem.item.onComposerDraw(self.uiFactory, self.aItem.amount, self.getMinAmount(), self.getMaxAmount())
            self.uiFactory.endRootLayout()

        orgX = x
        orgY = y
        lastX = x
        lastY = y

        for child in self.children:
            if nextDown:
                nextX = orgX
                nextY = y + ITEM_SIZE + ITEM_SPACE
            else:
                nextX = x + ITEM_SIZE + ITEM_SPACE
                nextY = orgY

            # draw connection between children
            if nextDown:
                QGraphicsLineItem(lastX + ITEM_SIZE_HALF - orgX, lastY + ITEM_SIZE - orgY,
                                  nextX + ITEM_SIZE_HALF - orgX, nextY + ITEM_SIZE - orgY, self)
            else:
                QGraphicsLineItem(lastX + ITEM_SIZE - orgX, lastY + ITEM_SIZE_HALF - orgY, nextX - orgX,
                                  nextY + ITEM_SIZE_HALF - orgY, self)

            tmpX, tmpY = child.draw(not nextDown, nextX, nextY)
            if tmpX > x:
                x = tmpX
            if tmpY > y:
                y = tmpY
            lastX = nextX
            lastY = nextY

        return x, y

    def drawBase(self):
        rect = QGraphicsRectItem(0, 0, ITEM_SIZE, ITEM_SIZE, self)
        rect.setBrush(QBrush(Qt.green))

    def amountChanged(self, amount):
        self.changeAmountCallback(self.aItem, amount)

    def handleItemChange(self, aList):
        pass

    def getMinAmount(self):
        if self.parent == None:
            return 1
        otherChildren = self.parent.getOtherChildren(self)
        return self.parent.aItem.item.minAmountOfItem(otherChildren, self.aItem)

    def getMaxAmount(self):
        if self.parent == None:
            return -1
        otherChildren = self.parent.getOtherChildren(self)
        return self.parent.aItem.item.maxAmountOfItem(otherChildren, self.aItem)

    def getOtherChildren(self, child):
        otherChildren = []
        for c in self.children:
            if c.aItem != None and c != child:
                otherChildren.append(c)
        return otherChildren

    def getChildAItems(self):
        aItems = []
        for c in self.children:
            aItems.append(c.aItem)
        return aItems

    def isValidComposition(self):
        if self.aItem == None and self.parent != None:
            return True

        for c in self.children:
            if not c.isValidComposition():
                return False

        if issubclass(type(self.aItem.item), ComposeableItem):
            return self.aItem.item.isCompositionAcceptable(self.getChildAItems())
        else:
            return True

    def createComposition(self, aList):
        if self.aItem == None:
            return

        for c in self.children:
            c.createComposition(aList)

        if issubclass(type(self.aItem.item), ComposeableItem):
            self.aItem.item.createComposition(self.getChildAItems(), aList)

    def clear(self, actor, clearMode):
        for c in self.children:
            c.clear(actor, clearMode)
        if clearMode == self.CLEAR_RECYCLE:
            if self.aItem != None:
                actor.ownedItems.append(self.aItem)
        elif clearMode == self.CLEAR_REMOVE:
            if self.aItem != None:
                actor.ownedItems.remove(self.aItem)

        self.aItem = None
        while (len(self.children) > 0):
            self.scene.removeItem(self.children[0])
            del self.children[0]

    def takePreferredAmountOfItem(self, actor, aItem):
        myAItem = aItem.copy()

        if self.parent == None:
            myAItem.amount = 1
        else:
            otherChildren = self.parent.getOtherChildren(self)
            max = self.parent.aItem.item.maxAmountOfItem(otherChildren, aItem)
            if max > aItem.amount:
                max = aItem.amount

            myAItem.amount = max

        actor.ownedItems.remove(myAItem)
        self.aItem = myAItem


class RootFilter(object):

    def __init__(self, aItem):
        self.aItem = aItem

    def isValidItem(self, aItem):
        if not issubclass(type(aItem.item), ComposeableItem):
            return False

        if aItem.amount == 0 and aItem.item.id == self.aItem.item.id:
            return True
        return aItem.item.canBeRoot


class ItemFuncFilter(object):

    def __init__(self, treeItem):

        self.children = []
        for c in treeItem.parent.children:
            if c.aItem != None:
                self.children.append(c.aItem)
        self.aItem = treeItem.parent.aItem

    def isValidItem(self, aItem):
        if aItem.amount == 0 and aItem.item.id == self.aItem.item.id:
            return True
        return self.aItem.item.isItemAcceptableChild(self.children, aItem)
