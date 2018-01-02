'''
Created on Dec 14, 2017

@author: Oribow
'''
from data.StrUtil import tStr
from data.AssetUtil import resPathToAbs
from PyQt4.Qt import QLabel, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, \
    QFormLayout, QSizePolicy, QPixmap
from PyQt4.QtCore import Qt
from morestrategy_too.AmountList import AmountList


class QItemInspector(object):

    def __init__(self, parentWidget, actor):
        self.graphicsViewWd = parentWidget
        self.layoutDefiner = LayoutDefinition(parentWidget, self.buttonClicked)
        self.actor = actor
        self.inspectedAItem = None

        actor.ownedItems.aItemChanged.connect(self.actorsItemsChanged)
        self.clear()

    def inspect(self, aItem=None):
        if aItem == None or not aItem.isValid():
            self.inspectedAItem = aItem
            self.layoutDefiner.clear()

        elif aItem == self.inspectedAItem:
            return

        else:
            self.layoutDefiner.startNewDefinition()
            aItem.item.onInspectorGUI(self.layoutDefiner)
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

    def clear(self):
        self.layoutDefiner.clear()

    def buttonClicked(self, func):
        func(self.inspectedAItem, self.actor)


class LayoutDefinition(object):

    def __init__(self, rootContainer, buttonClickedSlot):
        self.rootContainer = rootContainer
        self.buttonClickedSlot = buttonClickedSlot

    def startNewDefinition(self):
        self.compCache = []
        self.containerStack = [self.rootContainer.layout()]
        self.buildComponentCache()

    def clear(self):
        self.buildComponentCache()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def buildComponentCache(self):
        self.compCache = dict()
        # since that doesn't work, just delete all
        self.clearLayout(self.rootContainer.layout())
        return

        children = self.rootContainer.findChildren(QWidget)
        deleteHolder = QWidget()
        for c in children:
            t = type(c)
            if t != QLabel and t != QPushButton:
                print c
                c.setParent(deleteHolder)
            else:
                c.setParent(self.rootContainer)
                if t in self.compCache:
                    self.compCache[t].append(c)
                else:
                    self.compCache[t] = [c]

    def addHeadline(self, str):
        label = self.getWidget(QLabel)
        label.setText(tStr(str))
        f = label.font()
        f.setPointSize(30)
        label.setFont(f)
        self.containerStack[-1].addWidget(label)

    def addRank(self, rank):
        label = self.getWidget(QLabel)
        label.setText(tStr(rank.name))
        self.containerStack[-1].addWidget(label)

    def addDescription(self, str):
        label = self.getWidget(QLabel)
        label.setText(tStr(str))
        label.setWordWrap(True)
        self.containerStack[-1].addWidget(label)

    def addImg(self, path):
        imgView = self.getWidget(QLabel)
        imgView.setPixmap(QPixmap(resPathToAbs(path)))
        imgView.setFixedSize(50, 50)
        imgView.setScaledContents(True)
        self.containerStack[-1].addWidget(imgView)

    def addLabels(self, strs, addDoublePoint=True):
        self.beginFormLayout()

        for i in range(len(strs)):
            s = tStr(strs[i][0])
            if addDoublePoint:
                s += ":"
            label = self.getWidget(QLabel)
            label.setText(s)
            field = self.getWidget(QLabel)
            field.setText(tStr(strs[i][1]))
            self.containerStack[-1].addRow(label, field)

        self.endFormLayout()

    def addButton(self, str, func):
        bt = self.getWidget(QPushButton)
        bt.setText(tStr(str))
        # self.buttonClickedSlot(func)
        bt.clicked.connect((lambda f: lambda: self.buttonClickedSlot(f))(func))
        self.containerStack[-1].addWidget(bt)

    # 0 means as much space as possible
    def addVSpace(self, space=0):
        if space != 0:
            self.containerStack[-1].addSpacing(space)
        else:
            self.containerStack[-1].addStretch(1)

    def beginHorizontal(self):
        widget = QWidget()
        h = QHBoxLayout()
        widget.setLayout(h)
        self.containerStack[-1].addWidget(widget)
        self.containerStack.append(h)

    def endHorizontal(self):
        h = self.containerStack.pop()
        if type(h) != QHBoxLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")

    def beginVertical(self):
        widget = QWidget()
        v = QVBoxLayout()
        widget.setLayout(v)
        self.containerStack[-1].addWidget(widget)
        self.containerStack.append(v)

    def endVertical(self):
        v = self.containerStack.pop()
        if type(v) != QVBoxLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")

    def beginFormLayout(self):
        widget = QWidget()
        f = QFormLayout()
        widget.setLayout(f)
        self.containerStack[-1].addWidget(widget)
        self.containerStack.append(f)

    def endFormLayout(self):
        f = self.containerStack.pop()
        if type(f) != QFormLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")

    def addHeader(self, rank, headline, imgPath):
        self.beginHorizontal()
        self.beginVertical()
        self.addRank(rank)
        self.addHeadline(headline)
        self.endVertical()
        self.addImg(imgPath)
        self.endHorizontal()

    def addActionButtons(self, item):
        self.addVSpace()
        self.beginHorizontal()
        funcs = item.getExtraFunctionality()
        for k, v in funcs.iteritems():
            self.addButton(k, v)
        self.endHorizontal()

    def getWidget(self, type, *args):
        el = None
        if type in self.compCache:
            lst = self.compCache[type]
            if len(lst) == 1:
                self.compCache.pop(type, None)
            print "Reused cached comp for: " + str(type)
            el = lst.pop()
            el.show()
        else:
            print "Couldnt find {} in cache".format(type)
            el = type(*args)

        # apply defaults
        if type == QLabel:
            el.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            el.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            el.setWordWrap(False)
            f = el.font()
            f.setPointSize(11)
            el.setFont(f)
            el.setScaledContents(False)
        elif type == QHBoxLayout:
            el.setContentsMargins(0, 0, 0, 0)
        elif type == QPushButton:
            try:
                el.clicked.disconnect()
            except:
                pass
        return el
