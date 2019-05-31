'''
Created on Dec 16, 2017

@author: Oribow
'''
import ply.lex as lex
import ply.yacc as yacc
import data.StrUtil as StrUtil
from data.StrUtil import tStr, toIndex
from ply.lex import Token
from data import Items, Ranks, ItemTemplates

class ConstFilter (object):
    
    def __init__(self, const = True):
        self.const = const
    
    def isValidItem (self, aItem):
        return self.const

class ItemFilterJoin (object):
    
    #Joins
    AND, OR, N_EQUALS, EQUALS, IMPLIES = range(5)
    
    def __init__(self, leftFilter, join, rightFilter):
        self.leftFilter = leftFilter
        self.join = join
        self.rightFilter= rightFilter
        
    def isValidItem (self, aItem):
        rightMustTrue = False
        
        left = self.leftFilter.isValidItem(aItem)
        if self.join == self.AND:
            if left == False:
                return False
            else:
                rightMustTrue = True
        elif self.join == self.OR:
            if left == False:
                rightMustTrue = True
            else:
                return True
        elif self.join == self.N_EQUALS:
            if left == False:
                rightMustTrue = True
            else:
                rightMustTrue = False
        elif self.join == self.EQUALS:
            if left == False:
                rightMustTrue = False
            else:
                rightMustTrue = True
        elif self.join == self.IMPLIES:
            if left == False:
                return True
            else:
                rightMustTrue = True
        return self.rightFilter.isValidItem(aItem) == rightMustTrue            
    
class ExistsFilter (object):
    
    def __init__(self, attrId, hasToExist):
        self.attrId = attrId
        self.hasToExist = hasToExist
        
    def isValidItem(self, aItem):
        if self.attrId in aItem.item.getAttrsForTable():
            if self.hasToExist:
                return True
            else:
                return False
        else:
            if self.hasToExist:
                return False
            else:
                return True
            
class NumCompFilter (object):
    GREATER_THEN, LESSER_THEN, EQUALS, EQ_LESSER_THEN, EQ_GREATER_THEN, N_EQUALS = range(6)
    
    def __init__(self, attrId, opId, const, subAttr = None):
        self.attrId = attrId
        self.opId = opId
        self.const = const
        self.subAttr = subAttr
        
    def isValidItem(self, aItem):
        value = aItem.item.getData (self.attrId, ItemTemplates.SORTING_ROLE)
        if self.subAttr != None:
            value = value.__dict__[self.subAttr]
            
        if value == None:
            return False
        
        if self.opId == self.GREATER_THEN:
            return value > self.const
        
        if self.opId == self.LESSER_THEN:
            return value < self.const
        
        if self.opId == self.EQUALS:
            return value == self.const
        
        if self.opId == self.EQ_LESSER_THEN:
            return value <= self.const
        
        if self.opId == self.EQ_GREATER_THEN:
            return value >= self.const
        
        if self.opId == self.N_EQUALS:
            return value != self.const
        
class StrCompFilter (object):
    STARTS_WITH, ENDS_WITH, CONTAINS = range(3)
    
    def __init__(self, attrId, opId, const, subAttr = None):
        self.attrId = attrId
        self.opId = opId
        self.const = const
        self.subAttr = subAttr
        
    def isValidItem(self, aItem):
        value = aItem.item.getData (self.attrId, ItemTemplates.DISPLAY_ROLE)
        if self.subAttr != None:
            value = value.__dict__[self.subAttr]
        
        value = tStr(value)
        
        if value == None:
            return False
        
        if self.opId == self.STARTS_WITH:
            return value.startswith(self.const)
        
        if self.opId == self.ENDS_WITH:
            return value.endswith(self.const)
        
        if self.opId == self.CONTAINS:
            return self.const in value

def createStrUtilRegex (prefix):
    r = r"("
    for k, v in StrUtil.__dict__.items():
        
        if k.startswith(prefix):
            r += tStr(v)+"|"
    if r != "":
        r = r[:-1]
    r+=")"
    print (r)
    return r

"""
NO!
def toStrUtilIndex (prefix, string):
    for k, v in StrUtil.__dict__.iteritems():
        if k.startswith(prefix):
            if tStr(v) == string:
                return v
    print "Couldn't match "+string
    return -1
"""
#------Start of Lex def------------
literals = ("(", ")")

tokens = (
    "J_AND", "J_OR", "J_N_EQUALS", "J_EQUALS", "J_IMPLIES", #joins
    "HAS", "HAS_NOT", #attr exists
    "ATTR_CLASS", "ATTR_NAME", "ATTR_RANK", "ATTR_DESCRIPTION", "ATTR_VALUE",#attributes
    "LESSER", "GREATER", "EQ_LESSER", "EQ_GREATER", "EQUAL", "N_EQUAL", #number compare
    "STARTS_WITH", "ENDS_WITH", "CONTAINS", #string compare
    "NUMBER","CLASS", "RANK", "STRING", #values
    "LPAREN","RPAREN"
    )

#values
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

@Token(createStrUtilRegex("ITEM_CLASS_"))
def t_CLASS (t):
    i = StrUtil.toIndex(t.value)
    if i == -1:
        t_error(t)
    else:
        t.value = i
        return t
    
@Token(createStrUtilRegex("RANK_"))
def t_RANK (t):
    i = StrUtil.toIndex(t.value)
    for r in Ranks.ranks:
        if r.name == i:
            t.value = r.rankIndex
            return t
    print ("No match for "+t.value)
    return t

def t_STRING (t):
    r"\"\w+\""   
    t.value = t.value[1:]
    t.value = t.value[:-1]
    return t 

#joins
t_J_AND = r"and"
t_J_OR = r"or"
t_J_N_EQUALS= r"not\sequals"
t_J_EQUALS = r"equals"
t_J_IMPLIES = r"implies|=>"

#exists
t_HAS = r"has"
t_HAS_NOT = r"has not"

#attributes
t_ATTR_CLASS = r"class"
t_ATTR_NAME = r"name"
t_ATTR_RANK = r"rank"
t_ATTR_DESCRIPTION = r"description"
t_ATTR_VALUE = r"value"

#number compare
t_LESSER = r"<"
t_GREATER = r">"
t_EQ_LESSER = r"<="
t_EQ_GREATER = r">="
t_EQUAL = r"="
t_N_EQUAL = r"!="

#string compare
t_STARTS_WITH = r"starts\swith"
t_ENDS_WITH = r"ends\swith"
t_CONTAINS = r"contains"

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
#------End of Lex def------------------
#------Start of Grammar def------------

def p_statement (t):
    """statement : expression join statement"""
    t[0] = ItemFilterJoin(t[1], t[2], t[3])
        
def p_statement_group(t):
    "statement : LPAREN statement RPAREN"
    t[0] = t[2]
        
def p_statement_expr (t):
    """statement : expression"""
    t[0] = t[1]
        
def p_expression_exists (t):
    "expression : exist_comp attribute"
    t[0] = ExistsFilter(t[2], t[1])
    
def p_expression_attrclass_class (t):
    "expression : ATTR_CLASS equal_comp CLASS"
    t[0] = NumCompFilter(StrUtil.ITEM_ATTR_CLASS, t[2], t[3])

def p_expression_attrrank_rank (t):
    "expression : ATTR_RANK num_comp RANK"
    t[0] = NumCompFilter(StrUtil.ITEM_ATTR_RANK, t[2], t[3], "rankIndex")

def p_expression_num_attr (t):
    "expression : num_attribute num_comp NUMBER"
    t[0] = NumCompFilter(t[1], t[2], t[3])
    
def p_expression_str_attr (t):
    "expression : str_attribute str_comp STRING"
    t[0] = StrCompFilter(t[1], t[2], t[3])

#all attributes
def p_attribute (t):
    """attribute : num_attribute
                 | str_attribute
                 | enum_attribute"""
    t[0] = t[1]    
    
#enum attributes
def p_attribute_class (t):
    "enum_attribute : ATTR_CLASS"
    t[0] = StrUtil.ITEM_ATTR_CLASS
    
def p_attribute_rank (t):
    "enum_attribute : ATTR_RANK"
    t[0] = StrUtil.ITEM_ATTR_RANK

#number attributes    
def p_attribute_value (t):
    "num_attribute : ATTR_VALUE" 
    t[0] = StrUtil.ITEM_ATTR_VALUE  

#string attributes
def p_attribute_name (t):
    "str_attribute : ATTR_NAME" 
    t[0] = StrUtil.ITEM_ATTR_NAME  
    
def p_attribute_des (t):
    "str_attribute : ATTR_DESCRIPTION" 
    t[0] = StrUtil.ITEM_ATTR_NAME  
    
#equal compare
def p_equal_comp_equal (t):
    "equal_comp : EQUAL"
    t[0] = NumCompFilter.EQUALS
    
def p_equal_comp_n_equal (t):
    "equal_comp : N_EQUAL"
    t[0] = NumCompFilter.N_EQUALS
    
#number compare
def p_comp_equals (t):
    "num_comp : equal_comp"
    t[0] = t[1]
    
def p_comp_lesser (t):
    "num_comp : LESSER"
    t[0] = NumCompFilter.LESSER_THEN
    
def p_comp_greater (t):
    "num_comp : GREATER"
    t[0] = NumCompFilter.GREATER_THEN
    
def p_comp_eq_greater (t):
    "num_comp : EQ_GREATER"
    t[0] = NumCompFilter.EQ_GREATER_THEN
    
def p_comp_eq_lesser (t):
    "num_comp : EQ_LESSER"
    t[0] = NumCompFilter.EQ_LESSER_THEN
    
#string compare
def p_comp_starts_with (t):
    "str_comp : STARTS_WITH"
    t[0] = StrCompFilter.STARTS_WITH
    
def p_comp_ends_with (t):
    "str_comp : ENDS_WITH"
    t[0] = StrCompFilter.ENDS_WITH
    
def p_comp_contains (t):
    "str_comp : CONTAINS"
    t[0] = StrCompFilter.CONTAINS

#existance compare
def p_exists_has(t):
    "exist_comp : HAS"
    t[0] = True
        
def p_exists_has_not(t):
    "exist_comp : HAS_NOT"
    t[0] = False
        
#joins
def p_join_and (t):
    "join : J_AND"
    t[0] = ItemFilterJoin.AND

def p_join_or (t):
    "join : J_OR"
    t[0] = ItemFilterJoin.OR
    
def p_join_xor (t):
    "join : J_N_EQUALS"
    t[0] = ItemFilterJoin.N_EQUALS
    
def p_join_implies (t):
    "join : J_IMPLIES"
    t[0] = ItemFilterJoin.IMPLIES
    
def p_join_equals (t):
    "join : J_EQUALS"
    t[0] = ItemFilterJoin.EQUALS

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")

#------End of Grammar def------------------

lexer = lex.lex()
parser = yacc.yacc()


