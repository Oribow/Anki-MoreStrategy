from morestrategy_too.AmountList  import AmountList

#modifier
MOD_SINGULAR = 0
MOD_PLURAL = 1

#items
ITEM_MUG = 8
ITEM_DES_MUG = 9

ITEM_SWEET_SOUR_SOUP = 22
ITEM_DES_SWEET_SOUR_SOUP = 23

ITEM_MYSTERY_EGG = 25
ITEM_DES_MYSTERY_EGG = 26

ITEM_WOODEN_BOX = 28
ITEM_DES_WOODEN_BOX = 29

ITEM_MUG_IN_WOODEN_BOX = 30
ITEM_DES_MUG_IN_WOODEN_BOX = 33

ITEM_KLINKER = 35
ITEM_KLINKER_DES = 36

ITEM_JAEGER_FRAME_BRONZE = 38
ITEM_JAEGER_FRAME_BRONZE_DES = 39

#Item Attribute names
ITEM_ATTR_AMOUNT = 34
ITEM_ATTR_CLASS = 12
ITEM_ATTR_NAME = 13
ITEM_ATTR_RANK = 14
ITEM_ATTR_DESCRIPTION = 15
ITEM_ATTR_VALUE = 16
ITEM_ATTR_RARITY = 47
ITEM_ATTR_IMG_PATH = 17
ITEM_ATTR_REQ_ITEMS = 18
ITEM_ATTR_RES_ITEMS = 19
ITEM_ATTR_STAT_EFFECTS = 20

#item class names. Values are also used to sort the classes!
ITEM_CLASS_BASIC = 21
ITEM_CLASS_RECIPE = 24
ITEM_CLASS_LOOTBOX = 27
ITEM_CLASS_JAEGER_FRAME = 40

#item funcs
ITEM_FUNC_SELL = 1
ITEM_FUNC_SELL_ALL = 32
ITEM_FUNC_MAKE = 3 #make a recipe
ITEM_FUNC_OPEN = 4 #open lootbox

#ranks
RANK_COMMON = 10
RANK_LUXURY = 11

#quests
QUEST_ACTIVE = 45
QUEST_COMPLETED = 46

QUEST_MORE_MUGS_TITLE = 41
QUEST_MORE_MUGS_DESCRIPTION = 43
QUEST_MORE_MUGS_TASKS_1_DESCRIPTION = 44

en_strs = {
    #items
    ITEM_MUG: "Mug",
    ITEM_DES_MUG: "A common, but still beautifully crafted mug.",
    
    ITEM_SWEET_SOUR_SOUP: "Sweet Sour Soup",
    ITEM_DES_SWEET_SOUR_SOUP: "Chinese sweet and sour soup, tastes delicious!",
   
    ITEM_MYSTERY_EGG: "Mystery Egg",
    ITEM_DES_MYSTERY_EGG: "What in the world could be inside this egg?",
    
    ITEM_WOODEN_BOX: "Wooden Box",
    ITEM_DES_WOODEN_BOX: "Not very fancy, but fullfills its purpose",
    
    ITEM_MUG_IN_WOODEN_BOX: "Mug in Wooden Box",
    ITEM_DES_MUG_IN_WOODEN_BOX: "A common Mug in a Wooden Box",
    
    ITEM_KLINKER: "Klinker",
    ITEM_KLINKER_DES:"A Klinker",

    ITEM_JAEGER_FRAME_BRONZE: "Bronze Frame",
    ITEM_JAEGER_FRAME_BRONZE_DES: "A Jaeger frame made out of bronze",
    
    #ranks
    RANK_COMMON:"Common",
    RANK_LUXURY:"Luxury",
    #item.attributes names
    ITEM_ATTR_AMOUNT: "Amount",
    ITEM_ATTR_CLASS: "Class",
    ITEM_ATTR_NAME: "Name",
    ITEM_ATTR_RANK: "Rank",
    ITEM_ATTR_DESCRIPTION: "Description",
    ITEM_ATTR_VALUE: "Value",
    ITEM_ATTR_RARITY: "Rarity",
    ITEM_ATTR_IMG_PATH: "Image Path",
    ITEM_ATTR_REQ_ITEMS: {MOD_SINGULAR: "Required Item", MOD_PLURAL: "Required Items"},
    ITEM_ATTR_RES_ITEMS: {MOD_SINGULAR: "Resulting Item", MOD_PLURAL: "Resulting Items"},
    ITEM_ATTR_STAT_EFFECTS: "Stats-Effects",
    #item class names
    ITEM_CLASS_BASIC: "Basic",
    ITEM_CLASS_RECIPE: "Recipe",
    ITEM_CLASS_LOOTBOX: "LootBox",
    ITEM_CLASS_JAEGER_FRAME: "Jaeger Frame",
    #item funcs
    ITEM_FUNC_SELL: "Sell",
    ITEM_FUNC_MAKE: "Make",
    ITEM_FUNC_OPEN: "Open",
    ITEM_FUNC_SELL_ALL: "Sell All",
    #quests
    QUEST_ACTIVE: "Active",
    QUEST_COMPLETED: "Completed",
    QUEST_MORE_MUGS_DESCRIPTION: "I need a Birthday present for my Sister. I think 6 Mugs would do the trick! Could you collect them for me please?",
    QUEST_MORE_MUGS_TITLE: "Birthday Mugs",
    QUEST_MORE_MUGS_TASKS_1_DESCRIPTION: "Collect 6 Mugs"

    }

strs = en_strs

def tStr (index, modifier = MOD_SINGULAR):
    if type(index) == str:
        return index
    if type (index) == AmountList:
        return fAmountList(index)
    if type (index) == list and len(index) == 2:
        modifier = index[1]
        index = index[0]
    if type(index) != int:
        try:
            index = index.name
        except:
            return str(index)
    
    if type(index) == list:
        index = index[0]
        modifier = index[1]
        
    s = strs[index]
    if type(s) == dict:
        s = s[modifier]
    return s

def toIndex (string):
    i = next((k for k, v in strs.iteritems() if v == string), -1)
    if i == -1:
        print ("Couldn't match string "+str)
    return i

def fMoneyStr (money):
    return str(money) + "$"

def fAmountList (aList):
    s = ""
    for i in aList:
        s+=tStr(i.item)+" x"+str(i.amount)+", "
    s = s[:-2]
    return s

#getRightModus
def getModus (index, array):
    s = strs[index]
    if type(s) == dict:
        if len(array) > 1:
            return [index, MOD_PLURAL]
        else:
            return [index, MOD_SINGULAR]
    return index
    