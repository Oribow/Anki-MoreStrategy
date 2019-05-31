from data.ItemTemplates import *
from data.StrUtil import *
from data.Ranks import RankHolder as Ranks

class ItemHolder (object):
    mug = BaseItem(0, ITEM_MUG, ITEM_CLASS_BASIC, ITEM_DES_MUG, Ranks.common, 5, 0, "coffe_mug.gif")
    sweet_sour_soup = BaseItem(1, ITEM_SWEET_SOUR_SOUP, ITEM_CLASS_BASIC, ITEM_DES_SWEET_SOUR_SOUP, Ranks.common, 10, 0, "soup.png")
    
    #recipes
    mystery_egg_recipe = Recipe(2, ITEM_MYSTERY_EGG, ITEM_CLASS_RECIPE, ITEM_DES_MYSTERY_EGG, Ranks.luxury, 15, 0, "egg.png", [[1, mug]], [[1, sweet_sour_soup]])
    
    #lootboxes
    wooden_box = LootBox(3, ITEM_WOODEN_BOX, ITEM_CLASS_LOOTBOX, ITEM_DES_WOODEN_BOX, Ranks.common, 34, 0, "Wooden_Chest.png", 2, 4, -3, -0.5, 3, 0, 0, [[mug, 100]])
    
    #composable
    mug_of_wooden_box = Recipe(4, ITEM_MUG_IN_WOODEN_BOX, ITEM_CLASS_RECIPE, ITEM_DES_MUG_IN_WOODEN_BOX, Ranks.luxury, 23, 0, "Wooden_Chest.png", [[2, mug], [1, wooden_box]], [[1, sweet_sour_soup]])
    klinker = Recipe(5, ITEM_KLINKER, ITEM_CLASS_RECIPE, ITEM_KLINKER_DES, Ranks.luxury, 12, 0, "Wooden_Chest.png", [[1, mug]], [[1, sweet_sour_soup]])

    #jaeger frames
    bronze_jaeger_frame = JeagerFrame(6, ITEM_JAEGER_FRAME_BRONZE, ITEM_CLASS_JAEGER_FRAME, ITEM_JAEGER_FRAME_BRONZE_DES, Ranks.luxury, 354, 0, "egg.png", [[1, mug]], [mug, wooden_box, sweet_sour_soup, mystery_egg_recipe])


#do some magic and store all items in a list:
items = []
for k, v in ItemHolder.__dict__.items():
    if k.startswith("_"):
        continue
    items.append(v)
