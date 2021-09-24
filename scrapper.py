import re
import enum
import logging
import os
from time import sleep
from collections import defaultdict
from bs4 import BeautifulSoup
from friendlybot import FriendlyBot
from reporting import report_counts
from colors import bcolors as bg

PAGE=50 # number of links to get per request
PAGE_COUNT=5 # number of pages

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logging.basicConfig(level=LOGLEVEL)

logging.info(f'Examining the last {PAGE * PAGE_COUNT} posts...')

with open('alllisted.txt') as fh:
    ALL_STONKS = fh.read().split(',')


SUBREDDIT = 'wallstreetbets'

requests = FriendlyBot(speed_limit=1)

mentioned_stonks = defaultdict(int)


def main():

    after = None

    for _ in range(PAGE_COUNT):
        after = examine_links(mentioned_stonks, PAGE, after)

    sleep(1)
    report_counts(mentioned_stonks)


def examine_links(counter, count=25, after=None):
    """
    counter should be a defaultdict with int generator.
    counter will be updated with counts found in each page
    """

    params = {'count': PAGE}
    if after:
        params['after'] = after

    posts = requests.request(
            'GET',
            f'https://old.reddit.com/r/{SUBREDDIT}',
            params=params
            )

    soup = BeautifulSoup(posts.content, 'html.parser')

    links = soup.select('a.title')

    count_total = 0
    count_new = 0

    for title in [link.text for link in links]:
        words = title.split()
        for word in words:
            letters = re.sub(r'[^a-zA-Z]', '', word)
            if letters in ALL_STONKS:
                count_total += 1
                mentioned_stonks[letters] += 1
                count_new += 1 if mentioned_stonks[letters] == 1 else 0
    
    print(f'{bg.OKCYAN}Found {count_total} total stonk matches in this page {bg.ENDC}')
    if count_new:
        print(f'{bg.OKCYAN}({count_new} new stonks){bg.ENDC}')

    anchor = links[-1].findParent(class_='thing').get('id').split('_', 1)[-1]

    return anchor


if __name__ == '__main__':
    main()

