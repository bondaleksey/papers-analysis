# Papers analysis

Here you can find [Telegram-bot](http://t.me/find_an_expert_bot) implenetation. It examines abstracts of expert publications and ranks them according to the words in the query. 

Work on the project consists of the following parts:
- performed [Web-scraping](https://github.com/bondaleksey/training-ML-projects/blob/main/simple-nlp/notebooks/iterate_through_authors.ipynb) of one source of open publications (Requests, BeautifulSoup4) [their data representations](https://github.com/bondaleksey/papers-analysis/blob/main/notebooks/data_types.py),
- exploratory data analysis of errors in the data set was performed (pandas, numpy) [notebooks/EDA.ipynb](https://github.com/bondaleksey/papers-analysis/blob/main/notebooks/EDA.ipynb),
- based on the abstracts of articles I developed a [model](https://github.com/bondaleksey/papers-analysis/blob/main/notebooks/model.py) for ranking authors according to the user's
request (nltk, pymorphy2, sklearn),
- [Telegram-bot](https://github.com/bondaleksey/papers-analysis/blob/main/notebooks/sfindanexpertbot.py) was implemented (pyTelegramBotAPI).
