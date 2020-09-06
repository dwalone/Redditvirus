import sqlite3
import os.path
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time
import ffmpeg

db_name = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sql', 'virus.db'))
conn = sqlite3.connect(db_name)
c = conn.cursor()
c.execute("SELECT * from infected_count")
data = c.fetchall()

x = np.array([float(i[0]) for i in data])[0::10000]
y = np.array([i[1] for i in data])[0::10000]

dates=[dt.datetime.fromtimestamp(ts) for ts in x]

fig, (ax, ax1) = plt.subplots(2)
fig.set_figheight(10)
fig.set_figwidth(10)
fig.patch.set_facecolor('#1b2531')
xfmt = md.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(xfmt)

line, = ax.plot(dates, y, color='#e57502')
ax.set_xlabel('Date')
ax.set_ylabel('Count')
plt.setp(ax.get_xticklabels(), rotation=25)
ax.set_xticks(np.arange(dates[0], max(dates), dt.timedelta(days=5)))
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


for n in range(len(y)):
    xstrip = x[:n+1]
    line.set_data(dates[:n+1], y[:n+1])
    
    c.execute('''
          SELECT infector, COUNT(*) AS cnt FROM infections 
          WHERE infected_utc < ?
          GROUP BY infector 
          ORDER BY cnt DESC 
          LIMIT 8
          ''', (int(max(xstrip)),))
          
    tem = c.fetchall()
    
    val1 = ["Name","Infected"] 
    val2 = [[i[0], i[1]] for i in tem]
    
    if len(val2) == 0:
        val2 = [['None', 'None']]
        
    ax1.set_axis_off() 
    table = ax1.table( 
        
        cellText = val2,    
        colLabels = val1, 
        colColours = ['#1b2531', '#1b2531'],
        cellLoc ='center', 
        cellColours = [['#1b2531']*2]*len(val2),
        edges = 'open',
        loc ='upper center') 
    
    for i in range(len(val2)+1):
        for j in range(2):
            if i == 0:
                table[(i, j)].get_text().set_color('#e57502')    
            else:
                if j==0:
                    table[(i, j)].get_text().set_color('#ecac7f')
                if j==1:
                    table[(i, j)].get_text().set_color('#e3f4f8')
                
    table.set_fontsize(13)
    table.scale(0.6,1.5)       
    
    fig.tight_layout()
    fig.canvas.draw()
    fig.savefig('pics/Frame%05d.png' %n)
    ax1.cla()
    if n % 100 == 0:
        print(n)

'''        
(
    ffmpeg
    .input('/home/rutt/Documents/redditvirus/scripts/pics/*.png', pattern_type='glob', framerate=25)
    .output('movie.mp4')
    .run()
)
'''    
