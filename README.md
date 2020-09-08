# Redditvirus

Simulating a pandemic on r/Coronavirus, based on comment thread proximity

Over 2.8 million comments scraped between 1 March 2020 -> 1 April 2020

![final](https://raw.github.com/dwalone/Redditvirus/master/final.png)

See `graph.mp4` for the full animation

### Simulation rules

If a user X replies to a post/comment made by an infected user Y, user X is now infected.

If an infected user Y replies to a post/comment made by a user X, user X is now infected.

An infected user will remain infectious for a certain period, then either recover or die. Either way, they will not be able to be re-infected.

Patient Zero assigned to the author of the first submission scraped.

### Pandemic attributes

Infectious Period per user pulled randomly from scaled normal distributions contingent on whether they recover or die, based on this study:

https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext#fig2

Each user is given a random age following a discrete distribution given by:

https://www.indexmundi.com/world/age_structure.html

Mortality/Recovery probability depending on age based on normalised mean data given by:

https://ourworldindata.org/mortality-risk-covid#case-fatality-rate-of-covid-19-by-age

### Data

`virus.db` has 3 tables: `interactions`, `infections`, `infected_count`

Input you Reddit API credentials in `keys.py`, then change epoch times and run `scraper.py` to pull your own data

Change viral attributes and run `main.py` to simulate your own pandemic

Edit and use `visualise.py` to visualise your results

### Requirements

`Python 3.x`, `praw 7.x`, `sqlite 3.x`, `psaw 0.x`, `matplotlib 3.x`, `ffmpeg-python 0.x` 



  


