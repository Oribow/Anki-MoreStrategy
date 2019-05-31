'''
Created on Dec 18, 2017

@author: Oribow
'''

from PyQt5.QtCore import pyqtSignal, QObject


class AmountItem(object):

    def __init__(self, item, amount):
        self.item = item
        self.amount = amount

    def copy(self):
        return AmountItem(self.item.copy(), self.amount)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    def isValid(self):
        return self.item != None and self.amount != None


# Assumes there are not two items in list with same ids!
class AmountList(QObject):
    CHANGE_AMOUNT, CHANGE_REMOVED, CHANGE_APPEND, CHANGE_COMPLETELY = range(4)

    aItemChanged = pyqtSignal(list)
    afterAItemChanged = pyqtSignal()

    def __init__(self, aItemList=None):
        QObject.__init__(self)
        self.shouldBatch = False
        self.batch = []
        if aItemList is None:
            self.aItemList = []
        elif type(aItemList) == AmountList:
            self.aItemList = aItemList.copy()
        else:
            self.aItemList = aItemList

    def __getitem__(self, key):
        return self.aItemList[key]

    def __iter__(self):
        return self.aItemList.__iter__()

    def getAItemById(self, id):
        return next((x for x in self.aItemList if x.item.id == id), None)

    def getIndexById(self, id):
        return next((x for x, y in enumerate(self.aItemList) if y.item.id == id), None)

    def append(self, otherAItem):
        i = next((x for x in self.aItemList if x.item.id == otherAItem.item.id), None)
        if i is None:
            a = otherAItem.copy()
            self.aItemList.append(a)
            self.registerChange(a, self.CHANGE_APPEND)
        else:
            i.amount += otherAItem.amount
            self.registerChange(i, self.CHANGE_AMOUNT)

    def appendItem(self, item, amount):
        self.append(AmountItem(item, amount))

    def remove(self, otherAItem):
        i = next((x for x in self.aItemList if x.item.id == otherAItem.item.id), None)
        if i == None:
            raise Exception("Can't remove something, that doesn't exist!")
        else:
            if i.amount < otherAItem.amount:
                raise Exception("Not enough of item to remove")
            else:
                i.amount -= otherAItem.amount
                if i.amount == 0:
                    self.aItemList.remove(i)
                    self.registerChange(i, self.CHANGE_REMOVED)
                else:
                    self.registerChange(i, self.CHANGE_AMOUNT)

    def setAmountOf(self, id, amount):
        i = next((x for x in self.aItemList if x.item.id == id), None)
        if i is None:
            raise Exception("Can't change amount of something, that doesn't exist!")
        if amount == 0:
            self.aItemList.remove(i)
            self.registerChange(i, self.CHANGE_REMOVED)
            return
        i.amount = amount
        self.registerChange(i, self.CHANGE_AMOUNT)

    def addAmountList(self, otherList):
        map(self.append, otherList)

    def removeAmountList(self, otherList):
        map(self.remove, otherList)

    def __len__(self):
        return len(self.aItemList)

    def __contains__(self, other):
        return self.aItemList.__contains__(other)

    def isItemIn(self, aItem):
        i = next((x for x in self.aItemList if x.item.id == aItem.item.id), None)
        if i != None and i.amount >= aItem.amount:
            return True
        return False

    def isListIn(self, otherList):
        for i in otherList:
            if not self.isItemIn(i):
                return False
        return True

    def copy(self):
        aItems = []
        for aItem in self.aItemList:
            aItems.append(aItem.copy())
        return AmountList(aItems)

    def startBatch(self):
        self.shouldBatch = True

    def endBatch(self):
        self.shouldBatch = False
        if len(self.batch) == 0:
            return
        self.aItemChanged.emit(self.batch)
        self.afterAItemChanged.emit()
        self.batch = []

    def clearBatch(self):
        self.shouldBatch = False
        self.batch = []
        self.aItemChanged.emit([self.CHANGE_COMPLETELY])
        self.afterAItemChanged.emit()

    def registerChange(self, aItem, changeCode):
        if self.shouldBatch:
            if changeCode == self.CHANGE_REMOVED:
                cleanedBatch = self.batch
                self.batch = []
                for b in cleanedBatch:
                    if b[0].item.id != aItem.item.id:
                        self.batch.append(b)
            self.batch.append((aItem, changeCode))
        else:
            self.aItemChanged.emit([(aItem, changeCode)])
            self.afterAItemChanged.emit()

    def __getstate__(self):
        return (self.aItemList, )

    def __setstate__(self, state):
        self.aItemList = state

    def __reduce__(self):
        tupl = (self.__class__, self.__getstate__())
        return tupl


def fromList(list):
    aList = AmountList()
    for i in list:
        aList.append(AmountItem(i[1], i[0]))
    return aList


def copyInPlace(orgList, cpList):
    cpList.aItemList = []
    for aItem in orgList:
        cpList.aItemList.append(aItem.copy())
