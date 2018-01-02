from PyQt4 import uic
from PyQt4.QtCore import Qt
from data.AssetUtil import uiPathToAbs, resPathToAbs
from PyQt4.Qt import QWidget, QLabel, QTimeLine, QPixmap


queuedNotifys = []

def emitNotify (notify):
    queuedNotifys.append(notify)
    if len(queuedNotifys) == 1:
        queuedNotifys[0].start(notificationClosed)
    
def notificationClosed ():
    del queuedNotifys[0]
    if len(queuedNotifys) > 0:
        queuedNotifys[0].start(notificationClosed)

class LootBoxNotify (QWidget):
    fadeInTime = 0
    fadeOutTime = 1
    showTime = 3
    
    def __init__ (self, lootBox):
        QWidget.__init__(self)
        self.lootBox = lootBox

    def start (self, closeCallback):
        self.closeCallback = closeCallback
        uic.loadUi(uiPathToAbs("lootbox_popup.ui"), self)
        self.findChild(QLabel, "name").setText(self.lootBox.name)
        self.findChild(QLabel, "rank").setText("common")
        self.findChild(QLabel, 'img').setPixmap(QPixmap(resPathToAbs(self.lootBox.notifyImgRes)))
        rgb = self.lootBox.rank.notifyColor.getRgb()
        self.setStyleSheet("background-color:rgb({}, {}, {})".format(rgb[0], rgb[1], rgb[2]))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.closeMe)
        self.timeline.setDuration((self.fadeInTime + self.fadeOutTime + self.showTime)*1000)
        self.timeline.start()
        self.setWindowOpacity(0)
        self.show()
        
    def animate (self, value):
        value *= (self.fadeInTime + self.fadeOutTime + self.showTime)
        if value < self.fadeInTime:
            opacity = value / self.fadeInTime
        elif value < self.fadeInTime + self.showTime:
            opacity = 1
        else:
            opacity = 1 - ((value-(self.fadeInTime + self.showTime)) / self.fadeOutTime)
        self.setWindowOpacity(opacity)
        self.repaint()
        
    def closeMe (self):
        self.closeCallback()
        self.close()
        
        
        
        
        
        
        
        
        
        
        