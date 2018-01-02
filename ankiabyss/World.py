
class World (object):
    
    def __init__(self, players):
        self.players = players
        self.nextPlayerIndex = 0
        
    def nextTurn (self):
        self.players[self.nextPlayerIndex].beginTurn(self.actorFinishedTurn)
        self.nextPlayerIndex = (self.nextPlayerIndex + 1) % len(self.players)
        
    def actorFinishedTurn (self):
        pass