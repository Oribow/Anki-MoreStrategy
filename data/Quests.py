from data.QuestTemplates import *
from data.StrUtil import *
from data.Items import *
from morestrategy_too.AmountList import AmountItem
from data.Ranks import RankHolder as Ranks


class QuestHolder(object):
    mug = BaseQuest([QuestStage(QUEST_MORE_MUGS_TITLE, QUEST_MORE_MUGS_DESCRIPTION,
                                [CollectXTask(AmountItem(ItemHolder.mug, 6))], [[ItemHolder.sweet_sour_soup, 2]])])


# do some magic and store all items in a list:
quests = []
for k, v in QuestHolder.__dict__.iteritems():
    if k.startswith("_"):
        continue
    quests.append(v)
