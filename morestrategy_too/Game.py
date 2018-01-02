from morestrategy_too.SaveSystem import SavingSystem, loadAllSaves
from morestrategy_too.GameData import GameData


class Game(object):

    def __init__(self):
        self.saves = loadAllSaves()
        self.currentSaveState = None
        Game.game = self

    def createNewSaveState(self):
        print ("Creating new Save State")
        newSave = SavingSystem()
        self.saves.append(newSave)
        return newSave

    def saveMountedSaveState(self):
        self.currentSaveState.save()

    def mountSaveState(self, save):
        print "Mounting MetaSaveState: " + str(save)
        self.currentSaveState = save
        self.gameData = GameData(save)
        self.currentSaveState.load()

    def addNewActor(self, actor):
        print ("Added new Actor: " + str(actor))
        self.gameData.actors.append(actor)

        # only works with 1 item a time!

    """
    def recycleActorsItem(self, actor, item):
        DropManager.giveStuffToActor(actor.ownedIngrediences, item.ingredients)
        DropManager.takeUnsortedStuffFromActor(actor.ownedItems, [item])
        self.actorsItemsChanged.emit(actor)
        self.actorsIngresChanged.emit(actor)
        print("Recycled \""+item.name+"\", gained "+strForAmountLists(item.ingredients))
        return item.ingredients
    
    def makeActorsRecipe(self, actor, recipe):
        print "Requested to make "+str(recipe)
        if not DropManager.isStuffInList(recipe.reqItems, actor.ownedItems):
            return False
        
        print "Required Items... OK"
        if not DropManager.isStuffInList(recipe.reqIngre, actor.ownedIngrediences):
            return False
        
        print "Required Ingres... OK"
        
        DropManager.takeStuffFromActor(actor.ownedItems, recipe.reqItems)
        DropManager.takeStuffFromActor(actor.ownedIngrediences, recipe.reqIngre)
        DropManager.takeUnsortedStuffFromActor(actor.ownedRecipes, [recipe])
        
        DropManager.giveStuffToActor(actor.ownedItems, recipe.resultItems)
        self.actorsItemsChanged.emit(actor)
        self.actorsIngresChanged.emit(actor)
        self.actorsRecipesChanged.emit(actor)
        print "Created and gave: "+strForAmountLists(recipe.resultItems)
        return True
    """

    def logGameState(self):
        if self.currentSaveState == None:
            print ("No Save State mounted!")
            return

        for a in self.gameData.actors:
            print(str(a))
