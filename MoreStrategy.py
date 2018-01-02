from morestrategy_too.Game import Game
from morestrategy.GameObjects import Actor

def showAnswer ():
    game.applyActorsStudying(actor, 1)

addHook("showAnswer", showAnswer)

game = Game()
print("")
if len(game.gameData.metaSaveStates) < 1:
    save = game.createNewSaveState()
    game.mountSaveState(save)
    actor = Actor("Felix", 0, [], [], [])
    actor.studyingDropRate = 100
    game.addNewActor(actor)
else:
    save = game.gameData.metaSaveStates[0]
    game.mountSaveState(save)
    actor = game.currentSaveState.actors[0]