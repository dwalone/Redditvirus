import sqlite3
import os.path
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time

db_name = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sql', 'virus.db'))
conn = sqlite3.connect(db_name)
c = conn.cursor()
c.execute("SELECT * from infected_count")
data = c.fetchall()

x = np.array([float(i[0]) for i in data])[0::1000]
y = np.array([i[1] for i in data])[0::1000]

dates=[dt.datetime.fromtimestamp(ts) for ts in x]

fig, (ax, ax1) = plt.subplots(2)
fig.patch.set_facecolor('#1b2531')
xfmt = md.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(xfmt)

line, = ax.plot(dates, y, color='#e57502')
ax.set_xlabel('Date')
ax.set_ylabel('Count')
plt.setp(ax.get_xticklabels(), rotation=25)
ax.set_xticks(np.arange(dates[0], max(dates), dt.timedelta(days=7)))
ax.set_yticks(np.arange(y[0]-1, 70000, 10000))
ax.axis(xmin = dates[0], ymin = y[0]-1)
ax.set_facecolor('#1b2531')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_color('#3f424f')
ax.spines['left'].set_color('#3f424f')
ax.xaxis.label.set_color('#e57502')
ax.tick_params(axis='x', colors='#c4c7c8')
ax.yaxis.label.set_color('#e57502')
ax.tick_params(axis='y', colors='#c4c7c8')
ax.yaxis.grid(color = '#272f3e')
line.set_data(dates, y)


c.execute('''
          SELECT infector, COUNT(*) AS cnt FROM infections 
          GROUP BY infector 
          ORDER BY cnt DESC 
          LIMIT 10
          ''')
          
tem = c.fetchall()

val1 = ["Name","Infected"] 
val3 = [[i[0], i[1]] for i in tem]
ax1.set_axis_off() 
table = ax1.table( 
    cellText = val3,    
    colLabels = val1, 
    cellLoc ='center',  
    loc ='best')         





fig.tight_layout()
fig.canvas.draw()

'''
for n in range(len(y)):
    line.set_data(dates[:n], y[:n])
    fig.canvas.draw()
    fig.savefig('pics/Frame%05d.png' %n)
    if n % 100 == 0:
        print(n)
'''
    
