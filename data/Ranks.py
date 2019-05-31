'''
Created on Dec 14, 2017

@author: Oribow
'''
from data.StrUtil import *
import random


class Rank(object):

    def __init__(self, name, rankIndex):
        self.id = name
        self.name = name
        self.rankIndex = rankIndex  # higher is better!


class RankHolder(object):
    common = Rank(RANK_COMMON, 0)
    luxury = Rank(RANK_LUXURY, 1)


# do some magic and store all ranks in a list:
ranks = []
for k, v in RankHolder.__dict__.items():
    if k.startswith("_"):
        continue
    ranks.append(v)
