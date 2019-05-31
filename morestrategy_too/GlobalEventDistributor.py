from morestrategy_too.Game import Game


# register/unregister slots

# slot needs to take a batch
def cPlayerActorsItemsChanged(slot):
    Game.game.gameData.playerActor.ownedItems.aItemChanged.connect(slot)


def dPlayerActorsItemsChanged(slot):
    Game.game.gameData.playerActor.ownedItems.aItemChanged.disconnect(slot)


def composerCreatedItem(slot):
    pass


def cAfterPlayerActorsItemsChanged(slot):
    Game.game.gameData.playerActor.ownedItems.afterAItemChanged.connect(slot)


def dAfterPlayerActorsItemsChanged(slot):
    Game.game.gameData.playerActor.ownedItems.afterAItemChanged.disconnect(slot)
