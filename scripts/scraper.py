import praw
from psaw import PushshiftAPI
import datetime as dt
import keys
import sqlite3
import os.path

reddit = praw.Reddit(client_id = keys.client_id,
                     client_secret = keys.client_secret,
                     user_agent = keys.user_agent,
                     username = keys.username,
                     password = keys.password)

db_name = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sql', 'virus.db'))
conn = sqlite3.connect(db_name)
c = conn.cursor()

#c.execute('''CREATE TABLE interactions (author text, parent text, created_utc int, link_id text)''')

api = PushshiftAPI(reddit)

start_epoch=int(dt.datetime(2020, 3, 1).timestamp())
end_epoch=int(dt.datetime(2020, 4, 1).timestamp())
gen = api.search_comments(after=start_epoch, before=end_epoch, subreddit='coronavirus')


count = 0
while True:
    count += 1
    temp = [next(gen) for i in range(100)]
    temp1 = [i.parent_id for i in temp]
    try:
        for i, comment in enumerate(reddit.info(temp1)):
            c.execute('''INSERT INTO interactions VALUES (?, ?, ?, ?)''', (str(temp[i].author), str(comment.author), int(temp[i].created_utc), str(temp[i].link_id)))
            conn.commit()
    except Exception as e:
        print(e)
        break
    
    print(count)
    
conn.commit()
conn.close()