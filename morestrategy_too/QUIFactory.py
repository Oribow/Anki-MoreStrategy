from data.StrUtil import tStr
from data.AssetUtil import resPathToAbs
from PyQt5.Qt import QLabel, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, \
    QFormLayout, QSizePolicy, QPixmap, QSpinBox, QLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt


class QUIFactory(object):
    CompTypesToCache = [QLabel, QPushButton, QSpinBox]

    def beginUI(self, rootWidget):
        self.rootWidget = rootWidget
        self.compCache = []
        self.layoutStack = [self.rootWidget.layout()]
        self.fillCompCache()

    def endUI(self):
        self.rootWidget.updateGeometry()
        self.rootWidget = None
        self.compCache = []
        self.layoutStack = []

    def clearUI(self, layout=None):
        if layout is None:
            if len(self.layoutStack) == 0:
                return
            layout = self.layoutStack[0]

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def fillCompCache(self):
        self.compCache = dict()

        if self.rootWidget is None:
            return

        self.clearUI()
        return

        children = self.rootWidget.children()
        for child in children:
            if child == self.rootWidget.layout():
                continue
            self.takeCompsFromLayout(child)
            t = type(child)
            if issubclass(t, QWidget):
                self.rootWidget.layout().removeWidget(child)
                child.hide()
            # child.setParent(None)
            if t in self.CompTypesToCache:
                if t in self.compCache:
                    self.compCache[t].append(child)
                else:
                    self.compCache[t] = [child]

    def takeCompsFromLayout(self, layoutHolder):
        children = layoutHolder.children()
        for child in children:
            if child == layoutHolder.layout():
                continue
            self.takeCompsFromLayout(child)
            t = type(child)
            if issubclass(t, QWidget):
                layoutHolder.layout().removeWidget(child)
                child.hide()
            # child.setParent(None)
            if t in self.CompTypesToCache:
                if t in self.compCache:
                    self.compCache[t].append(child)
                else:
                    self.compCache[t] = [child]
        # if layoutHolder.layout() is not None:
        #    layoutHolder.layout().setParent(None)

    def image(self, pathToImg, **options):
        imgView = self.__mkImage(pathToImg, options)
        self.layoutStack[-1].addWidget(imgView)

    def __mkImage(self, pathToImg, options={}):
        imgView = self.makeWidget(QLabel)
        imgView.setAlignment(options.get("alignment", Qt.AlignLeft | Qt.AlignVCenter))
        imgView.setPixmap(QPixmap(resPathToAbs(pathToImg)))
        imgView.setFixedSize(options.get("width", 50), options.get("height", 50))
        imgView.setScaledContents(options.get("scaledContents", True))
        return imgView

    def button(self, text, **options):
        bt = self.__mkButton(text, options)
        self.layoutStack[-1].addWidget(bt)

    def __mkButton(self, text, options={}):
        bt = self.makeWidget(QPushButton, tStr(text))

        clickedSlot = options.get("clickedSlot", None)
        if clickedSlot is not None:
            bt.clicked.connect(clickedSlot)
        return bt

    def label(self, text, **options):
        label = self.__mkLabel(text, options)
        self.layoutStack[-1].addWidget(label)

    def __mkLabel(self, text, options={}):
        label = self.makeWidget(QLabel, tStr(text))
        label.setWordWrap(options.get("wordWrap", True))
        label.setAlignment(options.get("alignment", Qt.AlignLeft | Qt.AlignVCenter))
        label.setSizePolicy(*options.get("sizePolicy", (QSizePolicy.Preferred, QSizePolicy.Preferred)))
        label.setFrameStyle(options.get("frameStyle", QFrame.NoFrame))
        f = label.font()
        f.setPointSize(options.get("fontSize", 11))
        label.setFont(f)
        label.setScaledContents(options.get("scaledContents", True))
        elideWidth = options.get("maxTextWidth", 0)
        if elideWidth > 0:
            text = label.fontMetrics().elidedText(text, Qt.ElideRight, elideWidth)
            label.setText(text)
        return label

    def spinBox(self, value, min, max, **options):
        spBox = self.__mkSpinBox(value, min, max, options)
        self.layoutStack[-1].addWidget(spBox)

    def __mkSpinBox(self, value, min, max, options={}):
        spBox = QSpinBox()
        spBox.setValue(value)
        spBox.setMinimum(min)
        spBox.setMaximum(max)
        valueChangedSlot = options.get("valueChangedSlot", None)
        if valueChangedSlot is not None:
            spBox.valueChanged.connect(valueChangedSlot)
        return spBox

    def labels(self, texts, addColon=True):
        self.__beginFormLayout()
        for i in range(len(texts)):
            s = tStr(texts[i][0])
            if addColon:
                s += ":"
            name = self.__mkLabel(s)
            field = self.__mkLabel(tStr(texts[i][1]))
            self.layoutStack[-1].addRow(name, field)
        self.__endFormLayout()

    # 0 means as much space as possible
    def space(self, space=0):
        if space != 0:
            self.layoutStack[-1].addSpacing(space)
        else:
            self.layoutStack[-1].addStretch(1)

    def beginHorizontal(self, **options):
        widget = QWidget()
        h = QHBoxLayout()
        h.setContentsMargins(*options.get("contentMargin", (0, 0, 0, 0)))
        widget.setLayout(h)
        self.layoutStack[-1].addWidget(widget)
        self.layoutStack.append(h)

    def endHorizontal(self):
        h = self.layoutStack.pop()
        if type(h) != QHBoxLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")

    def beginVertical(self, **options):
        widget = QWidget()
        v = QVBoxLayout()
        v.setContentsMargins(*options.get("contentMargin", (0, 0, 0, 0)))
        widget.setLayout(v)
        self.layoutStack[-1].addWidget(widget)
        self.layoutStack.append(v)

    def endVertical(self):
        v = self.layoutStack.pop()
        if type(v) != QVBoxLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")

    def makeScrollArea(self, **options):
        QScrollArea(self.layoutStack[-1].parentWidget())

    def __beginFormLayout(self):
        widget = QWidget()
        f = QFormLayout()
        widget.setLayout(f)
        self.layoutStack[-1].addWidget(widget)
        self.layoutStack.append(f)

    def __endFormLayout(self):
        f = self.layoutStack.pop()
        if type(f) != QFormLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")

    def makeWidget(self, wdType, *args):
        widget = None
        if wdType in self.compCache:
            lst = self.compCache[wdType]
            if len(lst) == 1:
                self.compCache.pop(wdType)
            print ("Reused cached comp for: " + str(wdType))
            widget = lst.pop()
            widget.show()
        else:
            print ("Couldnt find {} in cache".format(wdType))
            widget = wdType(*args)
        return widget


class ItemInspectorUIFactory(QUIFactory):

    def __init__(self, extraFuncClickedSlot):
        self.extraFuncClickedSlot = extraFuncClickedSlot

    def header(self, rank, headline, imgPath):
        self.beginVertical()
        self.rank(rank)
        self.headline(headline)
        self.image(imgPath)
        self.endVertical()

    def extraFuncButtons(self, item):
        self.beginHorizontal()
        funcs = item.getExtraFunctionality()
        for k, v in funcs.items():
            self.button(k, clickedSlot=(lambda f: lambda: self.extraFuncClickedSlot(f))(v))
        self.endHorizontal()

    def description(self, text):
        self.label(text)

    def rank(self, rank):
        self.label(rank.name)

    def headline(self, text):
        self.label(text, fontSize=30)


class ComposerItemUIFactory(QUIFactory):
    V_SPACE = 4
    H_SPACE = 4

    def __init__(self, gScene):
        self.gScene = gScene

    def beginRootLayout(self, x, y, itemSize, parentGItem):
        self.itemSize = itemSize

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        widget.setLayout(layout)
        self.layoutStack = [layout]
        widget.setFixedSize(itemSize, itemSize)
        widget.setAttribute(Qt.WA_TranslucentBackground)
        proxyWidget = self.gScene.addWidget(widget)
        proxyWidget.setPos(x, y)
        parentGItem.addToGroup(proxyWidget)

        self.beginUI(widget)

    def endRootLayout(self):
        v = self.layoutStack.pop()
        if type(v) != QVBoxLayout:
            raise Exception("Tried to end layout, wrong layout on top of stack!")
        self.endUI()

    def label(self, text, **options):
        QUIFactory.label(self, text, maxTextWidth=self.itemSize - 4)

    def image(self, pathToImg, **options):
        QUIFactory.image(self, pathToImg, width=self.itemSize / 3, height=self.itemSize / 3)


class QuestUIFactory(QUIFactory):
    pass

    def title(self, text):
        self.label(text, fontSize=30)

    def tasks(self, tasks):
        self.beginVertical()
        # self.makeScrollArea()
        for t in tasks:
            self.label("\xe2   " + t.getTaskString())
        self.endVertical()

    def dialog(self, speaker, texts):
        self.beginHorizontal()
        if speaker.textAlign == Qt.AlignRight:

            self.beginVertical()
            for t in texts:
                self.label(t, alignment=speaker.textAlign | Qt.AlignVCenter, sizePolicy=(QSizePolicy.Expanding, QSizePolicy.Preferred), frameStyle=QFrame.Panel|QFrame.Sunken)
            self.space()
            self.endVertical()
            self.beginVertical()
            self.image(speaker.pathToAvatar, width=50, height=50, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.label(speaker.name, alignment=Qt.AlignHCenter | Qt.AlignTop)
            self.space()
            self.endVertical()
        else:
            self.beginVertical()
            self.image(speaker.pathToAvatar, width=50, height=50, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.label(speaker.name, alignment=Qt.AlignHCenter | Qt.AlignTop)
            self.space()
            self.endVertical()
            self.beginVertical()
            for t in texts:
                self.label(t, alignment=speaker.textAlign | Qt.AlignVCenter, sizePolicy=(QSizePolicy.Expanding, QSizePolicy.Preferred), frameStyle=QFrame.Panel|QFrame.Sunken)
            self.space()
            self.endVertical()

        self.endHorizontal()
