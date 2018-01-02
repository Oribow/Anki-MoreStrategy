import data.ItemExtraFunctions as ItemExtraFunctions
from data.StrUtil import fMoneyStr, fAmountList, getModus
from data import StrUtil
from data.StrUtil import tStr
from morestrategy_too.AmountList import AmountList, fromList
from data.DynamicItemTemplates import *

# class ids
TRASH, RECIPE, AUGMENTATION, WEAPON, ARMOR = range(5)
DISPLAY_ROLE, SORTING_ROLE, DATA_ROLE = range(3)


class BaseItem(object):

    @staticmethod
    def getAttrsForTable():
        return [StrUtil.ITEM_ATTR_CLASS,
                StrUtil.ITEM_ATTR_NAME,
                StrUtil.ITEM_ATTR_RANK,
                StrUtil.ITEM_ATTR_VALUE]

    def __init__(self, id, name, className, description, rank, value, imgPath):
        self.id = id
        self.name = name
        self.description = description
        self.rank = rank
        self.value = value
        self.imgPath = imgPath
        self.className = className

    # Can this item be shown in a ui inspector
    def getData(self, attrStrId, role):
        if role == DISPLAY_ROLE:
            if attrStrId == StrUtil.ITEM_ATTR_CLASS:
                return tStr(self.className)
            elif attrStrId == StrUtil.ITEM_ATTR_NAME:
                return tStr(self.name)
            elif attrStrId == StrUtil.ITEM_ATTR_RANK:
                return tStr(self.rank.name)
            elif attrStrId == StrUtil.ITEM_ATTR_VALUE:
                return StrUtil.fMoneyStr(self.value)
        elif role == SORTING_ROLE:
            if attrStrId == StrUtil.ITEM_ATTR_CLASS:
                return self.className
            elif attrStrId == StrUtil.ITEM_ATTR_NAME:
                return tStr(self.name)
            elif attrStrId == StrUtil.ITEM_ATTR_RANK:
                return self.rank.rankIndex
            elif attrStrId == StrUtil.ITEM_ATTR_VALUE:
                return self.value
        elif role == DATA_ROLE:
            if attrStrId == StrUtil.ITEM_ATTR_CLASS:
                return self.className
            elif attrStrId == StrUtil.ITEM_ATTR_NAME:
                return self.name
            elif attrStrId == StrUtil.ITEM_ATTR_RANK:
                return self.rank
            elif attrStrId == StrUtil.ITEM_ATTR_VALUE:
                return self.value
        return None

    def canBeInspected(self):
        return True

    # Is used to display buttons
    def getExtraFunctionality(self):
        return {StrUtil.ITEM_FUNC_SELL: ItemExtraFunctions.sell}

    # Fills up the inspector with data
    def onInspectorGUI(self, uiFactory):
        uiFactory.header(self.rank, self.name, self.imgPath)
        uiFactory.description(self.description)
        uiFactory.space(5)
        labels = []
        self.collectLabelsForInspector(labels)
        uiFactory.labels(labels)
        uiFactory.space()
        uiFactory.extraFuncButtons(self)

    # for easier rewrite
    def collectLabelsForInspector(self, labels):
        labels.append([StrUtil.ITEM_ATTR_VALUE, fMoneyStr(self.value)])

    def onComposerDraw(self, uiFactory, amount, min, max):
        uiFactory.label(tStr(self.name))
        uiFactory.image(self.imgPath)
        if min == max:
            if min == -1:
                uiFactory.spinBox(amount, 1, 9999999999)
            else:
                uiFactory.beginHorizontal()
                uiFactory.spinBox(amount, 1, max)
                uiFactory.label("/{}".format(max))
                uiFactory.endHorizontal()
        else:
            uiFactory.beginHorizontal()
            uiFactory.spinBox(1, max)
            uiFactory.label("({}-{})".format(min, max))
            uiFactory.endHorizontal()

    def __str__(self):
        return "{} \"{}\" ".format(str(type(self)), tStr(self.name))

    def copy(self):
        return self


class LootBox(BaseItem):

    def __init__(self, id, name, className, description, rank, value, imgPath,
                 minItemDrop, maxItemDrop, probFuncFalloff, probFuncOrign, probFuncHeight,
                 probFuncCutOffLeft, probFuncCutOffRight, itemDropProbList):
        BaseItem.__init__(self, id, name, className, description, rank, value, imgPath)
        self.minItemDrop = minItemDrop
        self.maxItemDrop = maxItemDrop
        self.probFuncFalloff = probFuncFalloff
        self.probFuncOrign = probFuncOrign
        self.probFuncHeight = probFuncHeight
        self.probFuncCutOffLeft = probFuncCutOffLeft
        self.probFuncCutOffRight = probFuncCutOffRight
        self.itemDropProbList = itemDropProbList

    def getExtraFunctionality(self):
        dic = BaseItem.getExtraFunctionality(self)
        dic[StrUtil.ITEM_FUNC_OPEN] = ItemExtraFunctions.openLootBox
        return dic

    def getDropProbabilityAt(self, x):
        if self.probFuncCutOffLeft != 0:
            x = max(x, self.probFuncCutOffLeft)
        if self.probFuncCutOffRight != 0:
            x = min(x, self.probFuncCutOffRight)
        return max(0, self.probFuncFalloff * pow(x + self.probFuncOrign, 2) + self.probFuncHeight)

    def getItemByChance(self, rand):
        for i in self.itemDropProbList:
            rand -= i[1]
            if rand <= 0:
                return i[0]


class ComposeableItem(BaseItem):

    def __init__(self, id, name, className, description, rank, value, imgPath):
        BaseItem.__init__(self, id, name, className, description, rank, value, imgPath)
        self.canBeRoot = False
        self.allowAutoFill = False

    def getChildCount(self, childAItems):
        raise NotImplemented()

    def isItemAcceptableChild(self, otherChildAItems, aItem):
        raise NotImplemented()

    def minAmountOfItem(self, otherChildAItems, aItem):
        raise NotImplemented()

    def maxAmountOfItem(self, otherChildAItems, aItem):
        raise NotImplemented()

    def isCompositionAcceptable(self, childAItems):
        raise NotImplemented()

    def createComposition(self, childAItems, aList):
        raise NotImplemented()


class Recipe(ComposeableItem):

    def __init__(self, id, name, className, description, rank, value, imgPath,
                 requiredAItems, resultingAItems):
        ComposeableItem.__init__(self, id, name, className, description, rank, value, imgPath)
        if type(requiredAItems) == list:
            requiredAItems = fromList(requiredAItems)
        if type(resultingAItems) == list:
            resultingAItems = fromList(resultingAItems)
        self.requiredAItems = requiredAItems
        self.resultingAItems = resultingAItems
        self.canBeRoot = True
        self.allowAutoFill = True

    def getChildCount(self, childAItems):
        return len(self.requiredAItems)

    def isItemAcceptableChild(self, otherChildAItems, aItem):
        i2 = next((x for x in otherChildAItems if x.item.id == aItem.item.id), None)
        if i2 != None:
            return
        i = next((x for x in self.requiredAItems if x.item.id == aItem.item.id), None)
        if i == None:
            return False  # not in recipe
        return True

    def minAmountOfItem(self, otherChildAItems, aItem):
        i = next(x for x in self.requiredAItems if x.item.id == aItem.item.id)
        return i.amount

    def maxAmountOfItem(self, otherChildAItems, aItem):
        i = next(x for x in self.requiredAItems if x.item.id == aItem.item.id)
        return i.amount

    def isCompositionAcceptable(self, childAItems):
        for c in childAItems:
            if c is None:
                return False
            i = next((x for x in self.requiredAItems if x.item.id == c.item.id), None)
            if i == None:
                return False
            if i.amount != c.amount:
                return False
        return True

    def createComposition(self, childAItems, aList):
        aList.addAmountList(self.resultingAItems)


class JeagerFrame(ComposeableItem):

    def __init__(self, id, name, className, description, rank, value, imgPath,
                 requiredTypes, allowedTypes):
        ComposeableItem.__init__(self, id, name, className, description, rank, value, imgPath)
        if type(requiredTypes) == list:
            requiredTypes = fromList(requiredTypes)
        self.requiredTypes = requiredTypes  # Alist with type, amount. Valid frame needs atleast the amount of type
        self.allowedTypes = allowedTypes  # List with items, that are acceptable children.
        self.canBeRoot = True

    def getChildCount(self, childAItems):
        return len(childAItems) + 1

    def isItemAcceptableChild(self, otherChildAItems, aItem):
        return True

    def minAmountOfItem(self, otherChildAItems, aItem):
        return 1

    def maxAmountOfItem(self, otherChildAItems, aItem):
        return True

    def isCompositionAcceptable(self, childAItems):
        return False

    def createComposition(self, childAItems, aList):
        return None
