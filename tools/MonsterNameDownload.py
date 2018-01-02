'''
Created on Dec 9, 2017

@author: Oribow
'''

import urllib
import html5lib
import sys
from morestrategy_too import Util
from time import sleep

def downloadHTMLFile (url, hasToStartWith):
    print ("Download from "+url)
    website = urllib.urlopen(url)
    t = website.read()
    dom = html5lib.parse(t, treebuilder="dom")
    lis = dom.getElementsByTagName("li")
    resultList = []
    for l in lis:
        if len(l.childNodes) > 0:
            ll = l.childNodes[0]
            if len(ll.childNodes) > 0:
                lll = ll.childNodes[0]
                if lll.nodeValue == None:
                    continue
                if lll.nodeValue.startswith("Lists"):
                    break
                nv = lll.nodeValue
                if "(" in lll.nodeValue:
                    nv = lll.nodeValue[:lll.nodeValue.find("(") - 1]
                    print "----->"+nv
                
                resultList.append(nv)
                print(lll.nodeValue)
    return resultList

def downloadAlphaSites (baseUrl):
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    result = []
    for a in alpha:
        a = a.upper()
        try:
            result.append(downloadHTMLFile(baseUrl + a + ")", a))
            print ("Finished "+a+". Will now wait for 5 sec")
            
        except ZeroDivisionError:
            e = sys.exc_info()[0]
            print "There was an exception!"
            print e
        sleep(5)
    return result

def printToFile (fileName):
    f = open(fileName, "w")
    lines = downloadAlphaSites("https://en.wikipedia.org/wiki/List_of_legendary_creatures_(")
    for ll in lines:
        for l in ll:
            if l != None and l != u"":
                f.write((l+u"\n").encode('utf8'))
    f.close()
  
printToFile(Util.resPathToAbs("Monster_Names.txt"))