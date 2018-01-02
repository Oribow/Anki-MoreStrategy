import random
from morestrategy_too.AmountList import AmountItem


def sell(aItem, actor):
    money = aItem.item.value * aItem.amount
    actor.ownedItems.remove(aItem)
    actor.changeMoney(money)


def makeRecipe(aItem, actor):
    pass


def openLootBox(aItem, actor):
    actor.startBatch()
    for i in range(aItem.amount):
        item = aItem.item
        itemCount = random.randint(item.minItemDrop, item.maxItemDrop)
        for i in range(itemCount):
            newItem = item.getItemByChance(random.random() * 100)
            actor.ownedItems.append(AmountItem(newItem, 1))

    actor.ownedItems.remove(aItem)
    actor.endBatch()
