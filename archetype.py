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
            self.main = PD.DataFrame()
            self.side = PD.DataFrame()
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
                            cnum  = card[:c]
                            cname = card[c+1:]
                            mb.append((cname,cnum))
                    self.main = PD.DataFrame(data=mb, columns=['Card','#'])
                    sb = []
                    for card in s:
                        if(card != ''):
                            c = card.find(" ")
                            cnum  = card[:c]
                            cname = card[c+1:]
                            sb.append((cname,cnum))
                    self.side = PD.DataFrame(data=sb, columns=['Card','#'])                
            else:
                print("not a .txt!")
        elif isinstance(data, list):
            print("List file!")
        else:
            raise TypeError("Incompatible data type passed: expected (.txt,.p) or list of cards")
            
    def __str__(self):
        toreturn = "Deck: "+self.name+"\n"
        #iterate over decklist
        for x in self.main.iterrows():
            toreturn += x[1]['#'] + "x " + x[1]['Card'] + "\n"
        toreturn += "Sideboard:\n"
        for x in self.side.iterrows():
            toreturn += x[1]['#'] + "x " + x[1]['Card'] + "\n"
        return toreturn
    
    def diff(self, otherDeck):
        '''returns as a DataFrame the card differences between the current
        deck and the passed deck. RIGHT NOW IT IS MAINBOARD ONLY, BUT IN THE
        FUTURE IT SHOULD ALSO LOOK AT SIDEBOARD'''
        
        pass
    
    def getMB(self):
        '''returns the mainboard as a DataFrame'''
        pass
    
    def getSB(self):
        '''returns the sideboard as a DataFrame'''
        pass
    
    def count(self, cardname: str):
        '''Returns the number of cards with name cardname in the main and sideboards'''
        pass
    
    def has(self, cardname: str):
        return (self.count(cardname) != 0)

    
d = Deck(name="Winner Deck",data="blah.txt")     
print(d)      
            