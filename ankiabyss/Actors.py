from Combat import chooseWeakestOpponent

class Actor (object):

    def __init__ (self, apos, playerOwner, health, initiative, factionId):
        self.playerOwner = playerOwner
        self.apos = apos
        self.maxHP = health
        self.currentHP = health
        self.initiative = initiative
        self.factionId = factionId
        
    #getters
    def getInitiative (self):
        return self.initiative
    
    def getHealth (self):
        return self.currentHP
    
    #attributes
    def isDead (self):
        return self.currentHP == 0
    
    #relationships
    def isHostileTo (self, otherActor):
        return self.factionId != otherActor.factionId
            
    #methods
    def handleFight (self, fightSzenario):
        self.playerOwner.handleFight(fightSzenario)
    
    #Events
    def beginFight (self):
        pass
    
    def canFightThisRound (self):
        return not self.isDead()

    def recieveDamage (self, damage):
        self.currentHP -= damage
        if self.currentHP < 0:
            self.currentHP = 0

class Monster (Actor):
    def __init__(self, health, initiative, factionId, givenName, attackPower):
        Actor(None, None, health, initiative, factionId)
        self.givenName = givenName
        self.attackPower = attackPower

    def handleFight (self, fightSzenario):
        opp = chooseWeakestOpponent(fightSzenario, self)
        if opp == None:
            print "Monster ("+self.givenName+") couldn't select an opponent"
            return
        opp.recieveDamage(self.attackPower)

    
class Jaeger (Actor):
    def __init__(self, health, initiative, factionId, givenName, attackPower):
        Actor(None, None, health, initiative, factionId)
        self.givenName = givenName
        self.attackPower = attackPower