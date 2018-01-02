from data.StrUtil import tStr
from data.AssetUtil import resPathToAbs
from PyQt4.Qt import QLabel, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, \
    QFormLayout, QSizePolicy, QPixmap
from PyQt4.QtCore import Qt


class QUIFactory(object):
    CompTypesToCache = [QLabel, QPushButton]

    def beginUI(self, rootWidget):
        self.rootWidget = rootWidget
        self.compCache = []
        self.containerStack = [self.rootWidget.layout()]
        self.fillCompCache()

    def clearUI(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def fillCompCache(self):
        self.compCache = dict()
        # since that doesn't work, just delete all
        self.clearUI(self.rootWidget.layout())
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

    def image(self, pathToImg, **options):
        imgView = self.__mkImage(pathToImg, options)
        self.containerStack[-1].addWidget(imgView)

    def __mkImage(self, pathToImg, options):
        imgView = self.makeWidget(QLabel)
        imgView.setPixmap(QPixmap(resPathToAbs(pathToImg)))
        imgView.setFixedSize(options.get("width", 50), options.get("height", 50))
        imgView.setScaledContents(options.get("scaledContents", True))
        return imgView

    def button(self, text, **options):
        bt = self.__mkButton(text, options)
        self.containerStack[-1].addWidget(bt)

    def __mkButton(self, text, options):
        bt = self.makeWidget(QPushButton, tStr(text))

        clickedSlot = options.get("clickedSlot", None)
        if clickedSlot is not None:
            bt.clicked.connect(clickedSlot)
        return bt

    def label(self, text, **options):
        label = self.__mkLabel(text, options)
        self.containerStack[-1].addWidget(label)

    def __mkLabel(self, text, options):
        label = self.makeWidget(QLabel, tStr(text))

        label.setWordWrap(options.get("wordWrap", True))
        label.setAlignment(options.get("alignment", Qt.AlignLeft | Qt.AlignVCenter))
        label.setSizePolicy(options.get("sizePolicy", QSizePolicy.Preferred, QSizePolicy.Preferred))
        f = label.font()
        f.setPointSize(options.get("fontSize"), 11)
        label.setFont(f)
        label.setScaledContents(options.get("scaledContents"), True)
        return label

    def labels(self, texts, addColon = True):
        self.__beginFormLayout()
        for i in range(len(texts)):
            s = tStr(texts[i][0])
            if addColon:
                s += ":"
            name = self.__mkLabel(s)
            field = self.__mkLabel(tStr(texts[i][1]))
            self.containerStack[-1].addRow(name, field)
        self.__endFormLayout()

    # 0 means as much space as possible
    def space(self, space=0):
        if space != 0:
            self.containerStack[-1].addSpacing(space)
        else:
            self.containerStack[-1].addStretch(1)

    def beginHorizontal(self, **options):
        widget = QWidget()
        h = QHBoxLayout()
        h.setContentsMargins(*options.get("contentMargin", (0, 0, 0, 0)))
        widget.setLayout(h)
        self.containerStack[-1].addWidget(widget)
        self.containerStack.append(h)

    def endHorizontal(self):
        h = self.containerStack.pop()
        if type(h) != QHBoxLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")

    def beginVertical(self, **options):
        widget = QWidget()
        v = QVBoxLayout()
        v.setContentsMargins(*options.get("contentMargin", (0, 0, 0, 0)))
        widget.setLayout(v)
        self.containerStack[-1].addWidget(widget)
        self.containerStack.append(v)

    def endVertical(self):
        v = self.containerStack.pop()
        if type(v) != QVBoxLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")

    def __beginFormLayout(self):
        widget = QWidget()
        f = QFormLayout()
        widget.setLayout(f)
        self.containerStack[-1].addWidget(widget)
        self.containerStack.append(f)

    def __endFormLayout(self):
        f = self.containerStack.pop()
        if type(f) != QFormLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")

    def makeWidget(self, wdType, *args):
        widget = None
        if wdType in self.compCache:
            lst = self.compCache[wdType]
            if len(lst) == 1:
                self.compCache.pop(wdType, None)
            print "Reused cached comp for: " + str(wdType)
            widget = lst.pop()
            widget.show()
        else:
            print "Couldnt find {} in cache".format(wdType)
            widget = wdType(*args)
        return widget


class ItemInspectorUIFactory(QUIFactory):

    def __init__(self, extraFuncClickedSlot):
        self.extraFuncClickedSlot = extraFuncClickedSlot

    def header(self, rank, headline, imgPath):
        self.beginHorizontal()
        self.beginVertical()
        self.addRank(rank)
        self.addHeadline(headline)
        self.endVertical()
        self.addImg(imgPath)
        self.endHorizontal()

    def extraFuncButtons(self, item):
        self.beginHorizontal()
        funcs = item.getExtraFunctionality()
        for k, v in funcs.iteritems():
            self.button(k, lambda v=v: self.extraFuncClickedSlot(v))
        self.endHorizontal()

    def description(self, text):
        self.label(text)

    def rank(self, rank):
        self.label(rank.name)

    def headline(self, text):
        self.label(text, fontSize=30)