from morestrategy_too.Game import Game

gameData = Game.game.gameData
# register/unregister slots

# slot needs to take a batch
def cPlayerActorsItemsChanged(slot):
    gameData.playerActor.ownedItems.aItemsChanged.connect(slot)


def dPlayerActorsItemsChanged(slot):
    gameData.playerActor.ownedItems.aItemsChanged.disconnect(slot)


def composerCreatedItem(slot):
    pass
