from Players import HumanPlayer
from Actors import Jaeger
from Combat import FightSzenario
from Actors import Monster

class Game (object):
    def __init__ (self, players, world):
        self.players = players
        self.world = world
        self.nextPlayerIndex = 0
        
    def nextTurn (self):
        self.players[self.nextPlayerIndex].doTurn(self.world)
        self.nextPlayerIndex = (self.nextPlayerIndex + 1) % len(self.players)
        
    def testFight (self):
        player = HumanPlayer
        jaeger = Jaeger(100, 33, 0, "Jaeger", 12)
        smurg = Monster(100, 20, 1, "Smurg", 5)
        fight = FightSzenario([smurg, jaeger])
        fight.startFight(self.fightEnded)
        
    def fightEnded(self):
        print ("Fight ended")