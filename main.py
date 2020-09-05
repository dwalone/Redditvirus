'''
https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext#fig2

onset to recovery - mean = 24.7, cv = 0.35
to death - mean =18.8, cv =0.45

my recovery - 7 days = 604800 so sd = 211680 (2.45 days)
death - 5.3279... = 460334, sd = 207150 (2.40 days)

since recovery after 0 days is unatural, keep 1 day minimum for recovery/death for both

https://www.indexmundi.com/world/age_structure.html
https://ourworldindata.org/mortality-risk-covid#case-fatality-rate-of-covid-19-by-age

0-14 years: 25.29% (male 981,129,427/female 916,864,766)
15-24 years: 15.77% (male 611,245,863/female 572,115,168)
25-54 years: 41.03% (male 1,559,197,242/female 1,519,386,627)
55-64 years: 8.84% (male 324,134,030/female 339,551,038)
65 years and over: 9.06%

bump up and slightly normalise mortality rates

make copy of database, push original to github

push scraper and main

check IGNORE_USERS

run main.py

make jupyter notebooks for data analysis

wrtite sql queries and put in same folder as database

'''

from itertools import count
import sqlite3
import random
import numpy as np

conn = sqlite3.connect('virus.db')
c = conn.cursor()

users = {}

RECOVERY_TIME_MU = 604800
RECOVERY_TIME_SD = 211680
DEATH_TIME_MU = 460334
DEATH_TIME_SD = 207150

AGE_MORTALITY_ELEMENTS = [["0-14", 0.01], ["15-24", 0.02], ["25-54", 0.05], ["55-64", 0.1], ["65+",0.2]]
AGE_PROBABILITES = [0.2529, 0.1577, 0.4103, 0.0884, 0.0906]

IGNORE_USERS = ['AutoModerator', 'None', '[None']


class User:
    
    _ids = count(1)
    
    def __init__(self, name, infector, infected_utc):
        self.name = name
        
        self.id = next(self._ids)
        
        self.infector = infector
        self.infected_utc = infected_utc
        
        age_mortality = np.random.choice(elements, p=probabilities)
        self.age = age_mortality[0]
        if random.random() > age_mortality[1]:
            self.uninfected_utc = int(max(34560, random.gauss(604800, 211680))) + infected_utc
            self.outcome = 'I'
        else:
            self.uninfected_utc = int(max(34560, random.gauss(460334, 207150))) + infected_utc
            self.outcome = 'D'
        
    
        
infcount = []
utc = []        

def main():
    
    c.execute('''SELECT * FROM interactions
                 ORDER BY created_utc DESC''')
                 
    for row in c:
        
        interaction_utc = row[2]
        
        infcount.append(sum(1 for i in users.values() if i.uninfected_utc > interaction_utc))
        utc.append(interaction_utc)
        
        parentname = row[1]
        authorname = row[0]
        
        if parentname not in IGNORE_USERS and authorname not in IGNORE_USERS:
                
            parent = users.get(parentname, None)
            author = users.get(authorname, None)
            
            if parent is None and author is not None:
                
                if author.uninfected_utc > interaction_utc:
                    users[parentname] = User(parentname, authorname, interaction_utc)
                    
            elif parent is not None and author is None:
            
                if parent.uninfected_utc > interaction_utc:
                    users[authorname] = User(authorname, parentname, interaction_utc) 
                    
    c.execute('''CREATE TABLE infections (id int, name text, infector int, infected_utc int, uninfected int, age text, outcome text)''')
    conn.commit()
    conn.close()
        
        

if __name__ == "__main__":
    
