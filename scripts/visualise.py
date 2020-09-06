import sqlite3
import os.path
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time
import ffmpeg
import matplotlib.gridspec as gridspec

db_name = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sql', 'virus.db'))
conn = sqlite3.connect(db_name)
c = conn.cursor()
c.execute("SELECT * from infected_count")
data = c.fetchall()

x = np.array([float(i[0]) for i in data])[0::100000]
y = np.array([i[1] for i in data])[0::100000]

dates=[dt.datetime.fromtimestamp(ts) for ts in x]


fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(2, 5)
ax1 = fig.add_subplot(gs[1, :2])
ax2 = fig.add_subplot(gs[1, 2:])
ax = fig.add_subplot(gs[0, :])

#fig, (ax, ax1) = plt.subplots(2)
fig.set_figheight(10)
fig.set_figwidth(10)
fig.patch.set_facecolor('#1b2531')
xfmt = md.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(xfmt)




line, = ax.plot(dates, y, color='#e57502')
linei, = ax2.plot(dates, y, color='#328c47')
lined, = ax2.plot(dates, y, color='#922d2d')

ax.set_xlabel('Date', fontsize=8)
ax.set_ylabel('Count', fontsize=8)
plt.setp(ax.get_xticklabels(), rotation=25)
ax.set_xticks(np.arange(dates[0], max(dates), dt.timedelta(days=5)))
ax.set_yticks(np.arange(0, 70000, 10000))
ax.tick_params(axis="x", labelsize=6)
ax.tick_params(axis="y", labelsize=6)
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

ax2.set_xlabel('Date', fontsize=8)
ax2.set_ylabel('Count', fontsize=8)
plt.setp(ax2.get_xticklabels(), rotation=25)
ax2.set_xticks(np.arange(dates[0], max(dates), dt.timedelta(days=5)))
ax2.set_yticks(np.arange(0, 200000, 40000))
ax2.tick_params(axis="x", labelsize=6)
ax2.tick_params(axis="y", labelsize=6)
ax2.axis(xmin = dates[0], ymin = y[0]-1)
ax2.set_facecolor('#1b2531')
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_color('#3f424f')
ax2.spines['left'].set_color('#3f424f')
ax2.xaxis.label.set_color('#e57502')
ax2.tick_params(axis='x', colors='#c4c7c8')
ax2.yaxis.label.set_color('#e57502')
ax2.tick_params(axis='y', colors='#c4c7c8')
ax2.yaxis.grid(color = '#272f3e')

immune = []
dead = []
utc = []
for n in range(len(y)):
    xstrip = x[:n+1]
    line.set_data(dates[:n+1], y[:n+1])
    
    c.execute('''
          SELECT infector, COUNT(*) AS cnt FROM infections 
          WHERE infected_utc < ?
          GROUP BY infector 
          ORDER BY cnt DESC 
          LIMIT 10
          ''', (int(max(xstrip)),))
          
    tem = c.fetchall()
    
    val1 = ["Name","Infected"] 
    val2 = [[i[0], i[1]] for i in tem]
    
    if len(val2) == 0:
        val2 = [['None', 'None']]
    
    c.execute('''
              SELECT AVG(cnt) FROM (
                  SELECT COUNT(*) AS cnt FROM infections
                  WHERE infected_utc < ?
                  GROUP BY infector
        )''', (int(max(xstrip)),))
    
    val2.append(["",""])
    try:
        val2.append([r'$R_{0}$ ~', round(c.fetchall()[0][0], 2)])
    except:
        val2.append([r'$R_{0}$ ~', "None"])
    ax1.set_axis_off() 
    table = ax1.table( 
        
        cellText = val2,    
        colLabels = val1, 
        colColours = ['#1b2531', '#1b2531'],
        cellLoc ='center', 
        cellColours = [['#1b2531']*2]*len(val2),
        edges = 'open',
        loc = 'upper center')
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.6) 
    
    for i in range(len(val2)+1):
        for j in range(2):
            if i == 0:
                table[(i, j)].get_text().set_color('#e57502')  
            elif i == len(val2):
                table[(i, j)].get_text().set_color('#fbe4d5')
                table[(i, j)].get_text().set_fontsize(14)
                
            else:
                if j==0:
                    table[(i, j)].get_text().set_color('#ecac7f')
                if j==1:
                    table[(i, j)].get_text().set_color('#e3f4f8')
                
 
    ax1.set_title("Who directly infected the most users?", color = '#fbe4d5')
    
    utc.append(dt.datetime.fromtimestamp(max(xstrip)))

    c.execute('''SELECT count(*) from infections where uninfected<? and outcome = "I"''', (int(max(xstrip)),))
      
    immune.append(c.fetchall()[0][0])
    
    c.execute('''SELECT count(*) from infections where uninfected<? and outcome = "D"''', (int(max(xstrip)),))        
    
    dead.append(c.fetchall()[0][0])
    
    linei.set_data(utc, immune)
    lined.set_data(utc, dead)
    
    fig.tight_layout()
    fig.canvas.draw()
    fig.savefig('pics/Frame%05d.png' %n)
    ax1.cla()
    if n % 10 == 0:
        print(n)

  
(
    ffmpeg
    .input('/home/rutt/Documents/redditvirus/scripts/pics/*.png', pattern_type='glob', framerate=25)
    .output('movie.mp4')
    .run()
)

