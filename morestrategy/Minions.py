import random
from morestrategy_too.Util import getRandomMonsterName
from morestrategy.GameObjects import Item


Skeleton_Body = 0
Skeleton_Head = 1
Skeleton_Arm = 2
Skeleton_Leg = 3

class MinionStats(object):
    HEALTH, ATTACK, DEFENSE, AGILITY = range (4)
    
    def __init__(self, health, attack, defense, agility):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.agility = agility
    
    def __getitem__ (self, index):
        if index == 0:
            return self.health
        if index == 1:
            return self.attack
        if index == 2:
            return self.defense
        if index == 3:
            return self.agility
        
    def __setitem__ (self, index, value):
        if index == 0:
            self.health = value
        if index == 1:
            self.attack = value
        if index == 2:
            self.defense = value
        if index == 3:
            self.agility = value
            
    def __str__(self, *args, **kwargs):
        return "(Health: "+str(self.health)+", Attack: "+str(self.attack)+", Defense: "+str(self.defense)+", Agility: "+str(self.agility)+")"
        
class BasicMinionComponent (object):
    
    def __init__ (self, baseItem):
        self.baseItem = baseItem
        
    def isValid (self, rootObj = False):
        if rootObj:
            return False
        return True
    
    def iterateOverChildren (self):
        raise StopIteration  
        
class StatsOnlyComp (BasicMinionComponent):
    
    def __init__(self, baseItem):
        BasicMinionComponent.__init__(self, baseItem)
        self.statModifier = baseItem.statsEffect
        
class LeafComp (StatsOnlyComp):
    
    def __init__(self, baseItem):
        StatsOnlyComp.__init__(self, baseItem)
        ib = baseItem.itemBody
        self.augSlots = ib.augSlots
        self.weaponSlots = ib.weaponSlots
        self.armorSlots = ib.armorSlots
        self.augments = []
        self.weapons = []
        self.armor = []
    
    def isValid (self, rootObj = False):
        if rootObj:
            return False
        if len(self.augments) > self.augSlots:
            return False
        if len(self.weapons) > self.weaponSlots:
            return False
        if len(self.armor) > self.armorSlots:
            return False
        return True
    
    def iterateOverChildren (self):
        for a in self.augments:
            yield a
            for c in a.iterateOverChildren():
                yield c
        for w in self.weapons:
            yield w
            for c in w.iterateOverChildren():
                yield c
        for a in self.armor:
            yield a
            for c in a.iterateOverChildren():
                yield c
        raise StopIteration
    
class RootComp (LeafComp):
    
    def __init__(self, baseItem):
        LeafComp.__init__(self, baseItem)
        ib = baseItem.itemBody
        self.headSlots = ib.headSlots
        self.armSlots = ib.armSlots
        self.legSlots = ib.legSlots
        self.legs = []
        self.heads = []
        self.arms = []
        
    def isValid (self, rootObj = False):
        
        if not rootObj:
            return False
        
        #self valid
        if not LeafComp.isValid(self, False):
            return False
        
        #children valid
        for child in self.iterateOverChildren():
            if not child.isValid():
                return False
            
        #meta valid
        headCount = 0
        armCount = 0
        legCount = 0
        for c in self.iterateOverChildren():
            if c.baseItem.iClass == Item.HEAD:
                headCount += 1
            elif c.baseItem.iClass == Item.ARM:
                armCount += 1
            elif c.baseItem.iClass == Item.LEG:
                legCount += 1
        
        if headCount == 0:
            return False
        
        if headCount > self.headSlots:
            return False
            
        if armCount > self.armSlots:
            return False
            
        if legCount > self.legSlots:
            return False
        
        return True
        
    def iterateOverChildren (self):
        for l in self.legs:
            yield l
            for c in l.iterateOverChildren():
                yield c
        for h in self.heads:
            yield h
            for c in h.iterateOverChildren():
                yield c
        for a in self.arms:
            yield a
            for c in a.iterateOverChildren():
                yield c
                
        LeafComp.iterateOverChildren(self)
        raise StopIteration

class MinionStatsModifier (MinionStats):
    
    def __init__(self, health, attack, defense, agility, isPercentage):
        MinionStats.__init__(self, health, attack, defense, agility)
        self.isPercentage = isPercentage
    
    def modifyAllStatsOnlyAbs (self, stats):
        for i in range(4):
            if self.isPercentage[i] == "0":
                stats[i] = self[i] + stats[i]
    
    def modifyAllStatsOnlyPer (self, stats):
        for i in range(4):
            if self.isPercentage[i] == "1":
                stats[i] = stats[i] + (self[i] / 100) * stats[i]

class Minion (object):

    def __init__ (self, skeleton, stats, name = getRandomMonsterName()):
        self.name = name
        self.originalStats = stats
        self.cStats = MinionStats(stats.health, stats.attack, stats.defense, stats.agility)
        self.skeleton = skeleton
        
    def takeAHit (self, attack):
        damage = attack * attack / (self.cStats.defense + attack)
        print ("Raw Attack: "+str(attack)+", Real Damage: "+str(damage))
        self.cStats.health -= damage
        if self.cStats.health < 0:
            self.cStats.health = 0
        
    def __str__(self, *args, **kwargs):
        return str(self.originalStats)
    
    def getPrettyStatStr (self, statIndex):
        orgStat = self.originalStats[statIndex]
        cStat = self.cStats[statIndex]
            
        if orgStat != cStat:
            return str(cStat)+"/"+str(orgStat)
        return str(orgStat)

def createMinion (minionSkelet):
    if not minionSkelet.isValid(True):
        return
    
    stats = MinionStats(0,0,0,0)
    for b in minionSkelet.iterateOverChildren():
        b.statModifier.modifyAllStatsOnlyAbs(stats)
            
    for b in minionSkelet.iterateOverChildren():
        b.statModifier.modifyAllStatsOnlyPer(stats)
            
    return Minion(minionSkelet, stats)

def convertItemToMinionComp (item):
    if item.iClass == Item.TRASH:
        print ("Trash items cant become Minion parts!")
        return None
    if item.iClass == Item.BODY:
        return RootComp(item)
    if item.iClass == Item.HEAD or item.iClass == Item.ARM or item.iClass == Item.LEG:
        return LeafComp(item)
    if item.iClass == Item.AUG or item.iClass == Item.WEAPON or item.iClass == Item.ARMOR:
        return StatsOnlyComp(item)
    
    print ("Couldn't convert item to minion part. Returning None")
    
def letMinionFightMinion (minionA, minionB):
    ms = [minionA, minionB]
    if minionA.cStats.agility > minionB.cStats.agility:
        cIMin = 0
    elif minionA.cStats.agility == minionB.cStats.agility:
        cIMin = random.choice([0,1])
    else:
        cIMin = 1
    nIMin = (cIMin + 1) % 2
    while (minionA.cStats.health > 0 and minionB.cStats.health > 0):
        ms[nIMin].takeAHit(ms[cIMin].cStats.attack)
        if nIMin == 0:
            print ("B hit A with "+str(ms[cIMin].cStats.attack)+", A.health = "+str(ms[nIMin].cStats.health))
        else:
            print ("A hit B with "+str(ms[cIMin].cStats.attack)+", B.health = "+str(ms[nIMin].cStats.health))
        nIMin = cIMin
        cIMin = (cIMin + 1) % 2
    
    
    
    