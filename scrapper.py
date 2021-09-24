import re
import enum
from collections import defaultdict
import requests
from bs4 import BeautifulSoup

with open('alllisted.txt') as fh:
    ALL_STONKS = fh.read().split(',')


SUBREDDIT = 'wallstreetbets'

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

print(mentioned_stonks)
