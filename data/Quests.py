from data.QuestTemplates import *
from data.StrUtil import *
from data.Items import *
from morestrategy_too.AmountList import AmountItem
from data.Ranks import RankHolder as Ranks

speakers = [Speaker(0, "Felix", "felix_avatar.jpg", Qt.AlignRight),
            Speaker(1, "Alice", "alice_avatar.jpg")]


class QuestHolder(object):
    mug = BaseQuest([QuestStage(QUEST_MORE_MUGS_TITLE, QUEST_MORE_MUGS_DESCRIPTION,
                                [CollectXTask("Collect 6 Mugs", AmountItem(ItemHolder.mug, 6), True),
                                 CollectXTask("Collect 5 Wooden Boxes", AmountItem(ItemHolder.wooden_box, 5), True)],
                                [[2, ItemHolder.sweet_sour_soup]],
                                [Dialog(speakers, [[0, "Hi!", "Wie geht es dir?", "Whats up?"],
                                                   [1, "This is an automated response message.", "I'm fine, really!"],
                                                   [1, "With less Text"],
                                                   [0, "This is an automated response message.", "I'm fine, really!", "With", "Way", "More", "Text",">"],
                                                   [1, "This is an automated response message.", "I'm fine, really!"]])]
                                )])


# do some magic and store all items in a list:
quests = []
for k, v in QuestHolder.__dict__.items():
    if k.startswith("_"):
        continue
    quests.append(v)
