import sqlite3
import os.path
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt

db_name = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sql', 'virus.db'))
conn = sqlite3.connect(db_name)
c = conn.cursor()
c.execute("SELECT * from infected_count")
data = c.fetchall()

conn.close()

x = np.array([float(i[0]) for i in data])[0::10]
y = np.array([i[1] for i in data])[0::10]

dates=[dt.datetime.fromtimestamp(ts) for ts in x]

fig = plt.figure()
fig.patch.set_facecolor('#1b2531')
ax=plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(xfmt)

plt.plot(dates,y, color='#e57502')
ax.set_xlabel('Date')
ax.set_ylabel('Count')
plt.xticks( rotation=25 )
plt.xticks(np.arange(dates[0], max(dates), dt.timedelta(days=7)))
plt.yticks(np.arange(y[0]-1, max(y), 10000))
plt.xlim(dates[0])
plt.ylim(y[0])
plt.subplots_adjust(bottom=0.2)
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