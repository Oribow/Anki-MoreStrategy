from random import choice
from data.AssetUtil import resPathToAbs
from PyQt5.QtWidgets import QMessageBox

def showMessage (text):
    msgBox = QMessageBox( )
    msgBox.setIcon( QMessageBox.Information )
    msgBox.setText( text )

    msgBox.addButton( QMessageBox.Close )

    msgBox.setDefaultButton( QMessageBox.Close ) 
    msgBox.exec_()
    
monsterNames = []
def getRandomMonsterName ():
    if len(monsterNames) == 0:
        #No cached Version of names available, so we have to load one from file
        with open(resPathToAbs("Monster_Names.txt")) as f:
            for line in f:
                if line.endswith("\n"):
                    line = line[:-1]
                monsterNames.append(line)
    return choice(monsterNames)
    


