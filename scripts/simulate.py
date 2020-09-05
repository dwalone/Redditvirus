from itertools import count
import sqlite3
import random
import numpy as np
import os.path

db_name = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sql', 'virus.db'))
conn = sqlite3.connect(db_name)
c = conn.cursor()

USERS = {}
RECOVERY_TIME_MU = 604800
RECOVERY_TIME_SD = 211680
DEATH_TIME_MU = 460334
DEATH_TIME_SD = 207150
AGE_ELEMENTS = ["0-14", "15-24", "25-54", "55-64", "65+"]
AGE_PROBABILITES = [0.2529, 0.1577, 0.4103, 0.0884, 0.0907] #65+ bumped from 0.0906 -> 0.0907 so probabilities sum to 1
AGE_MORTALITY = {
                 "0-14" : 0.01,
                 "15-24" : 0.02,
                 "25-54" : 0.05,
                 "55-64" : 0.1,
                 "65+" : 0.2
                 }

IGNORE_USERS = ['AutoModerator', 'None']

class user:
    
    _ids = count(1)
    
    def __init__(self, name, infector, infected_utc):
        self.name = name
        
        self.id = next(self._ids)
        
        self.infector = infector
        self.infected_utc = infected_utc

        self.age = np.random.choice(AGE_ELEMENTS, p=AGE_PROBABILITES)
        if random.random() > AGE_MORTALITY[self.age]:
            self.uninfected_utc = int(max(34560, random.gauss(604800, 211680))) + infected_utc
            self.outcome = 'I'
        else:
            self.uninfected_utc = int(max(34560, random.gauss(460334, 207150))) + infected_utc
            self.outcome = 'D'
            
def initialinf():        
    c.execute('''
              SELECT * FROM interactions
              ORDER BY created_utc ASC
              LIMIT 1
              ''')     
              
    row = c.fetchone()              
    USERS[row[0]] = user(row[0], row[0], row[2])
            
infcount = []
utc = []        

def main():    
    count = 0    
    initialinf()   
    
    c.execute('''SELECT * FROM interactions
                 ORDER BY created_utc ASC''')
                 
    for row in c:
        
        interaction_utc = row[2]        
        infcount.append(sum(1 for i in USERS.values() if i.uninfected_utc > interaction_utc))
        utc.append(interaction_utc)
        
        parentname = row[1]
        authorname = row[0]
        
        if parentname not in IGNORE_USERS and authorname not in IGNORE_USERS:
                
            parent = USERS.get(parentname, None)
            author = USERS.get(authorname, None)
            
            if parent is None and author is not None:
                
                if author.uninfected_utc > interaction_utc:
                    USERS[parentname] = user(parentname, authorname, interaction_utc)
                    
            elif parent is not None and author is None:
            
                if parent.uninfected_utc > interaction_utc:
                    USERS[authorname] = user(authorname, parentname, interaction_utc) 
        count += 1        
        if count % 10000 == 0:
            print(count)
                    
    c.execute('''CREATE TABLE infections (id int, name text, infector text, infected_utc int, uninfected int, age text, outcome text)''')
    for i in USERS.values():
        datapoint = (int(i.id), str(i.name), str(i.infector), int(i.infected_utc), int(i.uninfected_utc), str(i.age), str(i.outcome))
        c.execute('''INSERT INTO infections VALUES (?, ?, ?, ?, ?, ?, ?)'''
                  , datapoint)
        
    c.execute('''CREATE TABLE infected_count (utc int, inf_count int)''')
    for (i, j) in zip(utc, infcount):
        datapoint = (int(i), int(j))
        c.execute('''INSERT INTO infected_count VALUES (?, ?)'''
                  , datapoint) 
    
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    main()