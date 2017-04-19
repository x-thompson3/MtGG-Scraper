# -*- coding: utf-8 -*-
"""
@author: Xander Thompson

MtG Goldfish Decklist class:
    - Each Decklist object represents an Modern format archetype.
    - Decklist specifications:
        - name, date, mainboard, sideboard, 75, etc variables (pandas dataframes?)
        - in(cardname), diff(otherDeck), count(cardname), etc.
        - 
"""

import pandas as PD
import datetime as dt

class Deck():
    def __init__(self, name="", data=None):
        """Deck Constructor Method:
            Acceptable """
        if data is None:
            self.mainboard = PD.DataFrame()
            self.sideboard = PD.DataFrame()
            self.name = ""  
            self.date = dt.date.today()
        elif isinstance(data, str):
            if(data.split(".")[-1] == "txt"):
                self.name = name
                self.date = dt.date.today() # NEED TO CONVERT DATA.TXT's DATA into a DATE
                #self.date = dt.datetime.strptime(data.split(".")[0], "") 
                with open(data) as f:
                    string = f.read().split("sideboard")
                    m,s = string[0],string[1]
                    m = m.split("\n")
                    s = s.split("\n")
                    # generate a DataFrame for both main board and side board!
                    mb = []
                    for card in m:
                        if(card != ''):
                            c = card.find(" ")
                            cnum  = int(card[:c])
                            cname = card[c+1:]
                            mb.append((cname,cnum))
                    self.mainboard = PD.DataFrame(data=mb, columns=['Card','#'])
                    sb = []
                    for card in s:
                        if(card != ''):
                            c = card.find(" ")
                            cnum  = int(card[:c])
                            cname = card[c+1:]
                            sb.append((cname,cnum))
                    self.sideboard = PD.DataFrame(data=sb, columns=['Card','#'])                
            else:
                print("not a text file: "+data.split(".")[-1])
        elif isinstance(data, list):
            print("List file!")
        else:
            raise TypeError("Incompatible data type passed: expected (.txt,.p) or list of cards")
            
    def __str__(self):
        toreturn = "Deck: "+self.name+"\n"
        #iterate over decklist
        for x in self.mainboard.iterrows():
            toreturn += str(x[1]['#']) + "x " + x[1]['Card'] + "\n"
        toreturn += "Sideboard:\n"
        for x in self.sideboard.iterrows():
            toreturn += str(x[1]['#']) + "x " + x[1]['Card'] + "\n"
        return toreturn
    
    def diff(self, otherDeck):
        '''returns as a DataFrame the card differences between the current
        deck and the passed deck. RIGHT NOW IT IS MAINBOARD ONLY, BUT IN THE
        FUTURE IT SHOULD ALSO CONSIDER THE SIDEBOARD'''
        tm = self.mainboard
        om = otherDeck.getMB()
        d = tm.merge(om, on="Card", how='outer')
        print(d)
        print(d.get())
        
        
    
    def getMB(self):
        '''returns the mainboard as a DataFrame'''
        return self.mainboard
    
    def getSB(self):
        '''returns the sideboard as a DataFrame'''
        return self.sideboard
    
    def count(self, cardname: str, mo=False):
        '''Returns the number of cards with name cardname in the mainboard
        and optionally the sideboard'''
        c = 0
        if(self.has_mb):
            c += self.mainboard[self.mainboard.Card == cardname]['#'][0]
        if(mo and self.has_sb):
            c += self.sideboard[self.sideboard.Card == cardname]['#'][0]
        return c
            
    def has_mb(self, cardname: str):
        return (not self.mainboard.get(self.mainboard.Card == cardname).empty)

    def has_sb(self, cardname: str):
        return (not self.mainboard.get(self.mainboard.Card == cardname).empty)

    def has(self, cardname: str):
        return self.has_mb(cardname) and self.has_sb(cardname)
    
d = Deck(name="One Deck",data="test1d.txt")  
od = Deck(name="Other Deck", data="test2d.txt")
d.diff(od)