#Abstract
class Player (object):
    def __init__(self, givenName):
        self.givenName = givenName
        
    #Abstract
    def doTurn (self, world):
        raise Exception("Not definied!")

    def handleFight(self, fightSzenario):
        pass

class HumanPlayer (Player):

    def doTurn (self, world):
        pass

    def handleFight(self, fightSzenario):
        print "Choose your Target"

        index = 0
        for f in fightSzenario.fighters:
            if f == fightSzenario.currentFighter:
                print index + ": [-"+f.factionId+"-]"+f.givenName
            else:
                print index + ": ["+f.factionId+"]"+f.givenName
            index += 1
        
        #inp = rawInput()

    
    