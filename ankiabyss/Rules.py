'''
Created on Nov 18, 2017

@author: Oribow
'''

class ActorStatusEffect (object):
    
    def __init__ (self, actor):
        self.actor = actor
    
    #getters
    def modifyInitiative (self, initiative):
        return initiative 
    
    def getHealth (self):
        pass
    
    #setters
    def damageOccured (self, damage):
        pass
    
    #attributes
    def isDead (self):
        pass
    
    #relationships
    def isHostileTo (self, otherActor):
        pass
    
    #Events
    def beginFight (self):
        pass
    
    def chooseOpponent(self, fighters):
        self.playerOwner.chooseOpponent(self, fighters)
    
    def fightTurnBegins (self):
        pass
    
    def doFighting (self, opponent):
        pass
    
    def canFightThisRound (self):
        pass
    
    def fightEnded(self):
        pass
    
    def removeStatusEffect(self, effect):
        pass
    
    def ownerTurnStarted (self):
        pass
    
    def nonOwnerTurnStarted (self):
        pass
    
    def killedInFight (self):
        pass

class Poison (ActorStatusEffect):  
    
    def __init__(self, actor, damagePerRound):
        ActorStatusEffect(actor)
        self.damagePerRound = damagePerRound
    
    def fightTurnBegins (self):
        self.actor.damageMe(self.damagePerRound)
    
    def ownerTurnStarted (self):
        self.actor.damageMe(self.damagePerRound)
    