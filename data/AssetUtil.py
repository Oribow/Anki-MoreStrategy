'''
Created on Dec 14, 2017

@author: Oribow
'''
import os

# path pointing to project folder in which UnitTest.py is located
homePath = os.path.dirname(os.path.abspath(__file__))
resPath = os.path.join(homePath, "Resources")
uiPath = os.path.join(homePath, "UI")
savePath = os.path.join(homePath, "Saves")
print ("Path: " + homePath)


def relPathToAbs(path):
    # print os.path.join(homePath, path)
    return os.path.join(homePath, path)


def resPathToAbs(path):
    # print os.path.join(resPath, path)
    return os.path.join(resPath, path)


def uiPathToAbs(path):
    # print os.path.join(uiPath, path)
    return os.path.join(uiPath, path)


def savePathToAbs(path):
    # print os.path.join(savePath, path)
    return os.path.join(savePath, path)
