'''
Created on Nov 18, 2017

@author: Oribow
'''

class APos (object):
    def __init__ (self, layer = 0, orientation = 0, distToCenter = 0):
        self.layer = layer
        self.orientation = orientation
        self.distToCenter = distToCenter

    def copy (self):
        return APos(self.layer, self.orientation, self.distToCenter)
    
class TravelRoute (object):
    def __init__(self, targetLayerDepth, startPos, endPos):
        self.targetLayerDepth = targetLayerDepth
        self.startPos = startPos
        self.endPos = endPos
        
    def flipDirection (self, sourceLayerDepth):
        return TravelRoute(sourceLayerDepth, self.endPos, self.startPos)
    
class Path (object):
    def __init__(self, apositions):
        self.apositions = apositions
        
def moveAlongPath (movingActor, path):
    pass
