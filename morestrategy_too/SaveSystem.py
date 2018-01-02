'''
Created on Dec 19, 2017

@author: Oribow
'''
from PyQt4.QtCore import pyqtSignal
import pickle
from data.AssetUtil import savePathToAbs, savePath
from morestrategy_too.GameData import Actor
from morestrategy_too.AmountList import AmountList
from PyQt4.Qt import QObject
from os.path import isfile, join
import os
from datetime import datetime


def getUnusedSaveFileName(baseName):
    suffix = 0
    while os.path.isfile(baseName + str(suffix) + ".sav"):
        suffix += 1

    return baseName + str(suffix) + ".sav"


def loadAllSaves():
    files = [f for f in os.listdir(savePath) if isfile(join(savePath, f)) and f.endswith(".sav")]
    saves = []
    for f in files:
        saves.append(SavingSystem(f))
    return saves


class SavingSystem(QObject):
    onSave = pyqtSignal(dict)
    onLoad = pyqtSignal(dict)

    def __init__(self, fileName=getUnusedSaveFileName("save_")):
        QObject.__init__(self)
        self.fileName = fileName
        self.cachedSaveData = None
        self.registerSaveUser(self.loadMe, self.saveMe)

    def loadMe(self, data):
        meta = data.get("SavingSystem.Meta", [])
        if len(meta) == 0:
            self.slot = -1
            self.lastSaveTime = datetime.now()
        else:
            self.slot = meta[0]
            self.lastSaveTime = meta[1]

    def saveMe(self, data):
        meta = [
            self.slot,
            self.lastSaveTime
        ]
        data["SavingSystem.Meta"] = meta

    def registerSaveUser(self, loadSlot, saveSlot):
        if self.cachedSaveData != None:
            loadSlot(self.cachedSaveData)
        self.onLoad.connect(loadSlot)
        self.onSave.connect(saveSlot)

    def save(self):
        with open(savePathToAbs(self.fileName), "wb+") as f:
            saveData = {}
            self.onSave.emit(saveData)
            pickle.dump(saveData, f)
            print "Saved!"

    def load(self):
        saveData = {}
        try:
            with open(savePathToAbs(self.fileName), "rb") as f:
                saveData = pickle.load(f)
        except:
            print "Error while loading"

        self.onLoad.emit(saveData)
        print "Loaded!"
        self.cachedSaveData = saveData

    def discardDataCache(self):
        self.cachedSaveData = None
