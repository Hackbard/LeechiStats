__author__ = "Benjamin Klein"
__maintainer__ = "Benjamin Klein"
__email__ = "hackbard23@gmail.com"
__copyright__ = "Copyright 2018"
__license__ = "GNU GPL v3"
__version__ = "0.0.1"

import requests
from bs4 import BeautifulSoup
import os
import errno
import json
import datetime

# Fetcher
class Fetcher():
    REQUEST_HEADERS = {
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.8,de-DE;q=0.6',
        'origin': 'https://google.com',
        'referer': 'https://benjamin-klein.name/',
        'user-agent': 'leetchiStats spider 0.0.1'
    }

    def __init__(self):
        self.params = {

        }
        self.targets = []

    def setTargets(self, targets):
        self.targets = targets

    def execute(self):
        for target in self.targets:
            self.doWork(target)

    def doWork(self, target):
        name, url = target.split("|")
        response = self.get(url)

        if not response:
            print("GOT ERROR " + target)
            return False

        details = {
            'money': 0,
            'counter': 0,
            'days_to_go': 0,
            'fetched_at': datetime.datetime.now().__str__()
        }

        soup = BeautifulSoup(response.text, 'html.parser')
        print("Read {url}".format(url=target))
        sidebar = soup.select_one('#stickySidebar')
        details['money'] = sidebar.select_one('h1.o-article-status__heading.c-header__heading').text
        details['money'] = details['money'].replace("\n", "")
        details['money'] = details['money'].replace("€", "")
        details['money'] = details['money'].replace(".", "")
        details['money'] = details['money'].replace(",", ".")
        details['money'] = details['money'].strip()
        details['money'] = float(details['money'])

        details['counter'] = sidebar.select_one('.c-status__column.c-contribution.has-border .c-status__counter').text
        details['counter'] = int(details['counter'])

        details['days_to_go'] = sidebar.select_one('.c-status__column .c-status__counter').text
        details['days_to_go'] = int(details['days_to_go'])
        self.writeStats(details, name)

    def writeStats(self, details, name):
        filename = "data/{name}.jsondumps".format(name=name)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filename, "a+") as f:
            f.write(json.dumps(details) + "\n")

        return True

    def get(self, url):
        try:
            return requests.get(url, params=self.params, headers=self.REQUEST_HEADERS)
        except:
            return False
