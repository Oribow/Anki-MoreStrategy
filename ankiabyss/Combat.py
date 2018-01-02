'''
Created on Nov 18, 2017

@author: Oribow
'''
from operator import methodcaller
from RandomUtils import coinFlip

class FightSzenario (object):

    def __init__ (self, fighters):
        self.fighters = fighters

    def startFight (self, fightEndedCallback):
        self.fightOver = False
        self.fightEndedCallback = fightEndedCallback
        self.beginNextFightTurn()
        if self.fightOver:
            return
        self.beginNextFightersTurn()

    def beginNextFightTurn (self):
        if self.isFightOver():
            self.endFight()
        else:
            self.queuedFighters = self.fighters

    def beginNextFightersTurn (self):
        self.currentFighter = getFirstFighter(self.queuedFighters)
        self.currentFighter.fightTurnBegins()

        if not self.currentFighter.canFightThisRound():
            self.endFightersTurn()
            return

        self.currentFighter.handleFight(self)        

    def endFightersTurn (self):
        self.queuedFighters.remove(self.currentFighter)
        if len(self.queuedFighters) == 0:
            self.endFightTurn()
        else:
            self.beginNextFightTurn()

    def endFightTurn (self):
        self.beginNextFightTurn()

    def isFightOver (self):
        for f in self.fighters:
            if not f.isDead():
                if f.shouldFightContinue(self):
                    return False
        return True

    def endFight (self):
        self.fightOver = True
        self.fightEndedCallback()

def getFirstFighter (fighters):
    firstFighter = None
    firstFighterIntitative = 0

    for f in fighters:
        initiativ = f.getInitiative()
        if initiativ > firstFighterIntitative or (initiativ == firstFighterIntitative and coinFlip()):
            firstFighterIntitative = initiativ
            firstFighter = f

    return firstFighter

def chooseWeakestOpponent (fightSzenario, fighter):
    weakestFighter = None
    weakestFighterHealth = -1
    for f in fightSzenario.fighters:
        if f.isDead():
            continue
        if fighter.isHostileTo (f):
            health = f.getHealth()
            if weakestFighterHealth == -1 or weakestFighter > health:
                weakestFighterHealth = health
                weakestFighter = f
    return weakestFighter