import random
from morestrategy_too.Game import Game
from data.Ranks import RankHolder as Ranks


class Environment(object):

    def __init__(self, name, dropPerCard):
        self.name = name
        self.dropPerCard = dropPerCard

    def getRankAt(self, x):
        return Ranks.common


class AdventureConfig(object):
    quantityMultiplier = 0.3

    # quantityQuality (0-1) 0 = no Quality, 1 = no Quantity
    def __init__(self, rewardAt100, environment, quantityQuality):
        self.rewardAt100 = rewardAt100
        self.environment = environment
        self.dropPerCard = environment.dropPerCard + (1 - quantityQuality) * self.quantityMultiplier
        self.quantityQuality = quantityQuality

    def dropAmountForStudying(self, cardAmount):
        items = Game.game.gameData.playerActor.ownedItems
        items.startBatch()
        for i in range(cardAmount):
            rand = random.randrange(0, 1)
            if rand <= self.dropPerCard:
                self.dropItem()
        items.endBatch()

    def dropItem(self):
        rank = self.environment.getRankAt(x)

    def getRandItemByRank()


def getItemsForStudying():


def getRandRankAt(x):
    sum = 0
    for r in ranks:
        sum += r.getRankProbAt(x)
    rand = random.randrange(0, sum, 0.01)
    for r in ranks:
        rand -= r.getRankProbAt(x)
        if rand <= 0:
            return r
    raise Exception()


def dropAmountForStudying(cardAmount):
