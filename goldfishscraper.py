# -*- coding: utf-8 -*-
"""
@author: Xander Thompson

MTG Goldfish Web Scraping:
    - Read the webpage data of https://www.mtggoldfish.com/metagame/modern/full#paper
    - Somehow parse the webpage data and store locally: (Archetype Name, Meta%, Deck$)
    - If there are past data files, display/log the change in: Meta%, Deck Price
"""

import datetime as dt
import urllib.request as UReq
from bs4 import BeautifulSoup as BS
import pandas as PD
import os

def parseToList(myurl="https://www.mtggoldfish.com/metagame/modern/full#paper"):
    """If MtG Goldfish changes their site layout, this will
    all become obselete and need to be reconfigured.
    
    This function parses the HTML of the ModernMeta Page and returns a list
    of tuples of the form (deck_name,num_decks,meta_perc,cost)"""
    print("Scraping data of top 25 decks . . . ", end='')
    a = UReq.urlopen(myurl).read()
    
    arch = []
    urls = []
    #open in BS and look for archetype tiles
    soup = BS(a, 'html.parser')
    decks = soup.find_all('div', attrs={'class':"archetype-tile-description"})
    deck_stats = soup.find_all('div', attrs={'class':"archetype-tile-statistics"})
    
    for i in range(min(len(decks), 25)):
        x = decks[i]
        y = deck_stats[i]
        
        #determine archetype title
        title = x.find('span', attrs={'class':"deck-price-paper"})
        deck_url = title.find('a').get('href')
        deck_url = 'http://www.mtggoldfish.com' + deck_url
        title = title.text.replace('\n',"").replace("/","")
        urls.append((title,deck_url))
        
        #determine archetype stats
        temp = y.find_all('tr')[1]
        perc = temp.find('td', attrs={'class':"percentage"}).text.replace('\n', "")
        cost = temp.find('span', attrs={'class':"deck-price-paper"}).text.replace('\n', "").replace("$\\xc2\\xa0", "").replace(",","")
        
        #save archetype info to arch
        arch.append((title,perc,cost))
        
    print(" done")
    return PD.DataFrame(data=arch,columns=['Deck','%','$']), PD.DataFrame(data=urls,columns=['Deck','Link'])

def getDecklists(urls):
    '''follow the url from urls and capture the decklist for EACH archetype'''
    print('Downloading all decklists ', end="")
    decklists = []
    
    today = "./data/"+str(dt.date.today())
    if(not os.path.exists("./data")):
        os.mkdir("./data")
    if(not os.path.isdir(today)):
        os.mkdir(today)
        
    for i in urls.iterrows():
        print('.',end='')
        u = i[1].get('Link')
        name = i[1].get('Deck')
        response = UReq.urlopen(u).read()
        soup = BS(response, 'html.parser')
        dl = soup.find('input',attrs={'id':"deck_input_deck"}).get('value')
        #print('\n',name,'\n',dl,sep='')
        #decklists.append((name,dl))
        f = open(today+'/'+name+'.txt','w')
        f.write(dl)
        f.close()
        print(' done')
    return PD.DataFrame(data=decklists, columns=['Deck','List'])

def print_a(arch: list):
    """Display the date and the contents of arch"""
    print('print_a called')
    pass

def saveArchFT(d: dt.date, arch: PD.DataFrame):
    """save to a file the date and the contents of arch"""
    f = open('data.txt', 'a')
    f.write("######\n")
    for a in arch:
        f.write("{}\t{}\t{}\t{}\n".format(a[0],a[1],a[2]))
    f.close()
    
def openArchFT(fname):
    pass
    
def saveArchFP(d:dt.date, arch: PD.DataFrame):
    arch.to_pickle(str(d))
    print(arch)
    
def openArchFP(fname):
    pass

def begin():
    """Runs the other methods to scrape and parse the Web Data,
    then updates the data to record the new data"""
    today = dt.date.today()
    arch,urls = parseToList()
    decklists = getDecklists(urls)
    #saveArchFT(today, arch)
    print('= all done =')
    #print(arch)
    #print(urls)
    #input(">")
    
    
if __name__ == '__main__':
    begin()     