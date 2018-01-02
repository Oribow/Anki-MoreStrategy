from PyQt4 import uic
from PyQt4.Qt import QWidget, QFrame, QTableView, QLabel, QPushButton, QTextEdit, \
    QMainWindow
from PyQt4.QtCore import *

import morestrategy.Minions
import morestrategy.Minions
from morestrategy.Minions import MinionStats
from morestrategy_too import ImageViewerQt
from morestrategy_too.Util import *


class IteratorTableModel (QAbstractTableModel):

    def __init__ (self, attributeDecoder, entities, headerNames):
        QAbstractTableModel.__init__(self)
        self.attributeDecoder = attributeDecoder
        self.entities = entities
        self.headerNames = headerNames
        
    def rowCount(self, index=QModelIndex()):
        return len(self.entities)
    
    def columnCount(self, index=QModelIndex()):
        return len(self.headerNames)
    
    def aItemList(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
         (0 > index.row() < len(self.entities)):
            return QVariant()
        
        entity = self.entities[index.row()]
        if role == Qt.DisplayRole:
            return self.attributeDecoder(entity, index.column())
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))
        
        return QVariant()
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignHCenter | Qt.AlignVCenter))
        elif role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headerNames[section]
            elif orientation == Qt.Vertical:
                return QVariant(section + 1)
        return QVariant()
     
class LootBoxInspector (object):
    
    def __init__ (self, inspectorWidget):
        self.inspectorWidget = inspectorWidget
        self.graphicViewer = inspectorWidget.findChild(ImageViewerQt, "insp_img_graphicsView")
        self.rankLabel = inspectorWidget.findChild(QLabel, "insp_rank_label")
        self.nameLabel = inspectorWidget.findChild(QLabel, "insp_name_label")
        self.descriptionTextEdit = inspectorWidget.findChild(QTextEdit, "insp_description_textedit")
        self.sellValueLabel = self.inspectorWidget.findChild(QLabel, "insp_additional_info_value_4")
        self.inspect()
        
    def inspect (self, target = None):
        if target == None:
            self.rankLabel.setText("Rank")
            self.nameLabel.setText("Name")
            self.descriptionTextEdit.setText("Description")
            self.graphicViewer.clearImage()
        else:
            self.rankLabel.setText(inspectedAItem.rank.name)
            self.nameLabel.setText(target.name)
            self.descriptionTextEdit.setText(target.description)
            if target.notifyImgRes != None and target.notifyImgRes != "":
                self.graphicViewer.loadImageFromFile(resPathToAbs(target.notifyImgRes))
            self.sellValueLabel.setText(str(target.unitValue)+"$")
            
class ItemInspector (object):
    
    def __init__ (self, inspectorWidget):
        self.inspectorWidget = inspectorWidget
        self.graphicViewer = self.inspectorWidget.findChild(ImageViewerQt, "insp_img_graphicsView_2")
        self.rankLabel = self.inspectorWidget.findChild(QLabel, "insp_rank_label_2")
        self.nameLabel = self.inspectorWidget.findChild(QLabel, "insp_name_label_2")
        self.descriptionTextEdit = self.inspectorWidget.findChild(QTextEdit, "insp_description_textedit_2")
        self.ingredientsLabel = self.inspectorWidget.findChild(QLabel, "insp_ingre_label_2")
        self.slotsValueLabel = self.inspectorWidget.findChild(QLabel, "insp_additional_info_value")
        self.slotsLabel = self.inspectorWidget.findChild(QLabel, "insp_additional_info_label")
        self.sellValueLabel = self.inspectorWidget.findChild(QLabel, "insp_additional_info_value_3")
        self.inspect()

    def inspect (self, target = None):
        if target == None:
            self.rankLabel.setText("Rank")
            self.nameLabel.setText("Name")
            self.descriptionTextEdit.setText("Description")
            self.graphicViewer.clearImage()
        else:
            self.rankLabel.setText(inspectedAItem.rank.name)
            self.nameLabel.setText(target.name)
            self.descriptionTextEdit.setText(target.description)
            self.ingredientsLabel.setText(strForAmountLists(target.ingredients))
            if target.imgResPath != None and target.imgResPath != "":
                self.graphicViewer.loadImageFromFile(resPathToAbs(target.imgResPath))
            self.slotsValueLabel.setText(inspectedAItem.itemBody.getSlotValueString())
            self.slotsLabel.setText(inspectedAItem.itemBody.getSlotLabelString())
            self.sellValueLabel.setText(str(target.unitValue)+"$")
                      
class IngredientsInspector (object):
    
    def __init__ (self, inspectorWidget):
        self.inspectorWidget = inspectorWidget
        self.graphicViewer = self.inspectorWidget.findChild(ImageViewerQt, "insp_img_graphicsView_3")
        self.rankLabel = self.inspectorWidget.findChild(QLabel, "insp_rank_label_3")
        self.nameLabel = self.inspectorWidget.findChild(QLabel, "insp_name_label_3")
        self.descriptionTextEdit = self.inspectorWidget.findChild(QTextEdit, "insp_description_textedit_3")
        self.sellValueLabel = self.inspectorWidget.findChild(QLabel, "insp_additional_info_value_2")
        self.inspect()

    def inspect (self, target = None):
        if target == None:
            self.rankLabel.setText("Rank")
            self.nameLabel.setText("Name")
            self.descriptionTextEdit.setText("Description")
            self.graphicViewer.clearImage()
        else:
            self.rankLabel.setText(inspectedAItem.rank.name)
            self.nameLabel.setText(target.name)
            self.descriptionTextEdit.setText(target.description)
            if target.imgResPath != None and target.imgResPath != "":
                self.graphicViewer.loadImageFromFile(resPathToAbs(target.imgResPath))
            self.sellValueLabel.setText(str(target.unitValue)+"$")

class RecipeInspector (object):
    
    def __init__ (self, inspectorWidget):
        self.inspectorWidget = inspectorWidget
        self.rankLabel = self.inspectorWidget.findChild(QLabel, "insp_rank_label_4")
        self.nameLabel = self.inspectorWidget.findChild(QLabel, "insp_name_label_4")
        self.sellValueLabel = self.inspectorWidget.findChild(QLabel, "insp_additional_info_value_5")
        self.resultValueLabel = self.inspectorWidget.findChild(QLabel, "insp_result_label")
        self.requireValueLabel = self.inspectorWidget.findChild(QLabel, "insp_required_label")
        self.inspect()

    def inspect (self, target = None):
        if target == None:
            self.rankLabel.setText("Rank")
            self.nameLabel.setText("Name")
        else:
            self.rankLabel.setText(inspectedAItem.rank.name)
            self.nameLabel.setText(target.name)
            self.sellValueLabel.setText(str(target.unitValue)+"$")
            self.requireValueLabel.setText(strForAmountLists(target.reqItems)+", "+strForAmountLists(target.reqIngre))
            self.resultValueLabel.setText(strForAmountLists(target.resultItems))

class MinionsInspector (object):
    
    def __init__ (self, inspectorWidget):
        self.inspectorWidget = inspectorWidget
        self.nameLabel = self.inspectorWidget.findChild(QLabel, "insp_name_label_5")
        self.healthLabel = self.inspectorWidget.findChild(QLabel, "insp_health_label")
        self.attackLabel = self.inspectorWidget.findChild(QLabel, "insp_attack_label")
        self.defenseLabel = self.inspectorWidget.findChild(QLabel, "insp_defensiv_label")
        self.agilityLabel = self.inspectorWidget.findChild(QLabel, "insp_agility_label")
        self.bodyLabel = self.inspectorWidget.findChild(QLabel, "insp_body_label")
        self.health = self.inspectorWidget.findChild(QLabel, "insp_health_label")
        self.health = self.inspectorWidget.findChild(QLabel, "insp_health_label")
        self.health = self.inspectorWidget.findChild(QLabel, "insp_health_label")
        self.inspect()

    def inspect (self, target = None):
        if target == None:
            self.nameLabel.setText("Name")
            self.healthLabel.setText("")
            self.attackLabel.setText("")
            self.defenseLabel.setText("")
            self.agilityLabel.setText("")
        else:
            self.nameLabel.setText(target.name)
            #stats
            self.healthLabel.setText(target.getPrettyStatStr(MinionStats.HEALTH))
            self.attackLabel.setText(target.getPrettyStatStr(MinionStats.ATTACK))
            self.defenseLabel.setText(target.getPrettyStatStr(MinionStats.DEFENSE))
            self.agilityLabel.setText(target.getPrettyStatStr(MinionStats.AGILITY))
            
            #skeleton 
            body = inspectedAItem.skeleton.getSkeletonPart(morestrategy.Minions.Skeleton_Body)
            self.bodyLabel.setText()


class MainWindow (QMainWindow):
    
    def __init__ (self, game, actor):
        QMainWindow.__init__(self)
        uic.loadUi(relPathToAbs("UI/morestrategy_main.ui"), self)
        self.game = game
        self.actor = actor
        
        self.lootBoxTab = LootBoxTab(self.findChild(QWidget, 'lootbox_tab'), actor, game)
        self.itemTab = ItemTab(self.findChild(QWidget, 'item_tab'), actor, game)
        self.ingreTab = IngredientsTab(self.findChild(QWidget, 'ingredient_tab'), actor, game)
        self.resTab = RecipeTab(self.findChild(QWidget, 'recipes_tab'), actor, game)
        self.minTab = MinionTab(self.findChild(QWidget, 'minion_tab'), actor, game)
        
        self.cActorName = self.findChild(QLabel, 'c_actor_name')
        self.cActorMoney = self.findChild(QLabel, 'c_actor_money')
        
        self.cActorName.setText(actor.name)
        self.updateCActorsMoneyLabel(actor, 0)
        game.actorsMoneyChanged.connect(self.updateCActorsMoneyLabel)
        
        self.show()
        
    def updateCActorsMoneyLabel (self, actor, change):
        if actor == self.actor:
            self.cActorMoney.setText(str(actor.money)+"$")

class GenericTab (object):
    AMOUNT, NAME, RANK, VALUE = range(4)
    expectDataChange = False
    
    def __init__ (self, tabHostWidget, targetList, headerNames, inspector):
        self.tabWidget = tabHostWidget
        self.tableView = tabHostWidget.findChild(QTableView)
        self.tableView.currentChanged = self.itemTableViewSelectionChanged
        self.targetList = targetList
        self.inspector = inspector
        self.columnCount = len(headerNames)
        self.setupButtons()
        
        self.model = IteratorTableModel(self.attributeDecoder, targetList, headerNames)
        self.tableView.setModel(self.model)
        resizeColumns(self.tableView, len(headerNames)) 
    
    def setupButtons (self):
        pass
    
    def modelDataChanged (self, actor):
        if actor == self.actor:
            if self.expectDataChange:
                index = self.tableView.selectionModel().currentIndex()
                strIndex = QModelIndex(index)
                endIndex = self.model.index(index.row(), self.columnCount)
                self.model.dataChanged.emit(strIndex, endIndex)
            else:
                self.model.reset()
    
    def itemTableViewSelectionChanged (self, selected, deselected):
        self.inspector.inspect(self.getCurrentSelected()[0])
        QTableView.currentChanged(self.tableView, selected, deselected)
    
    def getCurrentSelected (self):
        index = self.tableView.selectionModel().currentIndex()
        if not index.isValid():
            return None
        return self.targetList[index.row()]
    
    def attributeDecoder (self, thing, column):
        if column == self.AMOUNT:
            return thing[1]
        if column == self.NAME:
            return thing[0].name
        if column == self.RANK:
            return thing[0].rank.name
        if column == self.VALUE:
            return thing[0].unitValue
        return QVariant()

class LootBoxTab (GenericTab):
    AMOUNT, NAME, RANK, VALUE = range(4)
    
    def __init__ (self, tabHostWidget, actor, game):
        self.actor = actor
        self.game = game
        
        inspector = LootBoxInspector(tabHostWidget.findChild(QFrame, "lootbox_inspector"))
        GenericTab.__init__(self, tabHostWidget, actor.ownedLootBoxes, ["Amount", "Name", "Rank", "Value"], inspector)
        game.actorsLootBoxesChanged.connect(self.modelDataChanged)
        
    def setupButtons (self):
        openLootBoxBt = self.tabWidget.findChild(QPushButton, "open_lootbox_button")
        sellLootBoxBt = self.tabWidget.findChild(QPushButton, "sell_lootbox_button")
        openLootBoxBt.clicked.connect(self.openLootBoxClicked)
        sellLootBoxBt.clicked.connect(self.sellLootBoxClicked)
     
    def openLootBoxClicked (self):
        box = self.getCurrentSelected()
        if box == None:
            return
        
        newItems = self.game.openActorsLootBox(self.actor, box[0])
        newItems = unsortedToAmountList(newItems)
        showMessage(strForAmountLists(newItems))
        
        
    def sellLootBoxClicked (self):
        self.expectDataChange = True
        box = self.getCurrentSelected()
        if box == None:
            return
        
        self.game.sellSingleActorsThing(self.actor, self.actor.ownedLootBoxes, box[0])
        
        self.expectDataChange = False
    
class ItemTab (GenericTab):
    AMOUNT, NAME, RANK, CLASS, VALUE = range(5)
    
    def __init__ (self, tabHostWidget, actor, game):
        self.actor = actor
        self.game = game
        
        inspector = ItemInspector(tabHostWidget.findChild(QFrame, "item_inspector"))
        GenericTab.__init__(self, tabHostWidget, actor.ownedItems, ["Amount", "Name", "Rank", "Class", "Value"], inspector)
        game.actorsItemsChanged.connect(self.modelDataChanged)
            
    def attributeDecoder (self, amountItem, column):
        if column == self.AMOUNT:
            return amountItem[1]
        if column == self.NAME:
            return amountItem[0].name
        if column == self.RANK:
            return amountItem[0].rank.name
        if column == self.CLASS:
            return next(x for x in self.game.gameData.itemClassNames if x[0] == amountItem[0].iClass)[1]
        if column == self.VALUE:
            return amountItem[0].unitValue
        
        return QVariant()
    
    def setupButtons (self):
        recycleItemBt = self.tabWidget.findChild(QPushButton, "recycle_item_button")
        sellItemBt = self.tabWidget.findChild(QPushButton, "sell_item_button")
        useItemBt = self.tabWidget.findChild(QPushButton, "use_item_button")
        
        recycleItemBt.clicked.connect(self.recycleItemClicked)
        sellItemBt.clicked.connect(self.sellItemClicked)
        useItemBt.clicked.connect(self.useItemClicked)

    def useItemClicked (self):
        pass
        
    def recycleItemClicked (self):
        self.expectDataChange = True
        item = self.getCurrentSelected()
        if item == None:
            return
        newIngre = self.game.recycleActorsItem(self.actor, item[0])
        showMessage(strForAmountLists(newIngre))
        
        self.expectDataChange = False
        
    def sellItemClicked (self):
        self.expectDataChange = True
        item = self.getCurrentSelected()
        if item == None:
            return
        self.game.sellSingleActorsThing(self.actor, self.actor.ownedItems, item[0])
        
        self.expectDataChange = False
      
class IngredientsTab (GenericTab):
    AMOUNT, NAME, RANK, VALUE = range(4)
    
    def __init__ (self, tabHostWidget, actor, game):
        self.actor = actor  
        self.game = game
              
        inspector = IngredientsInspector(tabHostWidget.findChild(QFrame, "ingre_inspector"))
        GenericTab.__init__(self, tabHostWidget, actor.ownedIngrediences, ["Amount", "Name", "Rank", "Value"], inspector)
        game.actorsIngresChanged.connect(self.modelDataChanged)
        
    def setupButtons (self):
        sellIngreBt = self.tabWidget.findChild(QPushButton, "sell_item_button_2")
        
        sellIngreBt.clicked.connect(self.sellIngredientsClicked)
    
    def sellIngredientsClicked (self):
        self.expectDataChange = True
        item = self.getCurrentSelected()
        if item == None:
            return
        self.game.sellSingleActorsThing(self.actor, self.actor.ownedIngrediences, item[0])
        
        self.expectDataChange = False

class RecipeTab (GenericTab):
    AMOUNT, NAME, RANK, VALUE = range(4)
    
    def __init__ (self, tabHostWidget, actor, game):
        self.actor = actor
        self.game = game
        
        inspector = RecipeInspector(tabHostWidget.findChild(QFrame, "recipe_inspector"))
        GenericTab.__init__(self, tabHostWidget, actor.ownedRecipes, ["Amount", "Name", "Rank", "Value"], inspector)
        game.actorsRecipesChanged.connect(self.modelDataChanged)

    def setupButtons (self):
        sellItemBt = self.tabWidget.findChild(QPushButton, "sell_item_button_3")
        makeItemBt = self.tabWidget.findChild(QPushButton, "make_recipe_button")
        
        sellItemBt.clicked.connect(self.sellItemClicked)
        makeItemBt.clicked.connect(self.makeItem)

    def sellItemClicked (self):
        self.expectDataChange = True
        item = self.getCurrentSelected()
        if item == None:
            return
        self.game.sellSingleActorsThing(self.actor, self.actor.ownedRecipes, item[0])
        
        self.expectDataChange = False
        
    def makeItem (self):
        self.expectDataChange = True
        item = self.getCurrentSelected()[0]
        r = self.game.makeActorsRecipe(self.actor, item)
        if r:
            showMessage("Made "+strForAmountLists(item.resultItems))
        self.expectDataChange = False

class MinionTab (GenericTab):
    NAME, HEALTH, ATTACK, DEFENSE, AGILITY  = range(5)
    
    def __init__ (self, tabHostWidget, actor, game):
        self.actor = actor
        self.game = game
        
        inspector = MinionsInspector(tabHostWidget.findChild(QFrame, "minion_inspector"))
        GenericTab.__init__(self, tabHostWidget, actor.ownedMinions, ["Name", "Health", "Attack", "Defense", "Agility"], inspector)
        game.actorsMinionChanged.connect(self.modelDataChanged)

    def attributeDecoder (self, item, column):
        if column == self.NAME:
            return item.name
        if column == self.HEALTH:
            return item.getPrettyStatStr(MinionStats.HEALTH)
        if column == self.ATTACK:
            return item.getPrettyStatStr(MinionStats.ATTACK)
        if column == self.DEFENSE:
            return item.getPrettyStatStr(MinionStats.DEFENSE)
        if column == self.AGILITY:
            return item.getPrettyStatStr(MinionStats.AGILITY)
        return QVariant()
    
    def itemTableViewSelectionChanged (self, selected, deselected):
        self.inspector.inspect(self.getCurrentSelected())
        QTableView.currentChanged(self.tableView, selected, deselected)
   
def resizeColumns(tableView, columnCount):
    for c in range(columnCount):
        tableView.resizeColumnToContents(c)                
   
   
   
        