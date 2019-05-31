'''
Created on Dec 22, 2017

@author: Oribow
'''
from PyQt5.Qt import QCompleter
from PyQt5.QtCore import Qt
from data import Refila
from data.Refila import ItemFilterJoin

class QRefilaLineEdit (object):
    
    def __init__(self, collectionSelector, lineEdit):
        self.filter_line_edit = lineEdit
        self.collectionSelector = collectionSelector
        
        lineEdit.editingFinished.connect(self.reparseRefilaInput)
        self.completer = QCompleter(["Apple", "Terminal"])
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        lineEdit.setCompleter(self.completer)
        

    def reparseRefilaInput (self):
        text = str(self.filter_line_edit.text())
        if text == "":
            self.collectionSelector.updateFilter(None)
            return
        filter = Refila.parser.parse(text, debug=True)
        if filter == None:
            print ("Parsing failed!")

        self.collectionSelector.updateFilter(filter)
        
    
        
        
        
        