import re
import enum
import logging
import os
from collections import defaultdict
from bs4 import BeautifulSoup
from friendlybot import FriendlyBot
from reporting import report_counts
import sys

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logging.basicConfig(level=LOGLEVEL)

logging.info('Debug logging set')

with open('alllisted.txt') as fh:
    ALL_STONKS = fh.read().split(',')


SUBREDDIT = 'wallstreetbets'

requests = FriendlyBot(speed_limit=2)

posts = requests.request(
        'GET',
        f'https://old.reddit.com/r/{SUBREDDIT}'
        )

soup = BeautifulSoup(posts.content, 'html.parser')

links = soup.select('a.title')

mentioned_stonks = defaultdict(int)

print(links)


for title in [link.text for link in links]:
    words = title.split()
    for word in words:
        letters = re.sub(r'[^a-zA-Z]', '', word)
        if letters in ALL_STONKS:
            print('found 1', letters)
            mentioned_stonks[letters] += 1

report_counts(mentioned_stonks)


