#!/usr/bin/env python
#
# extract_wiki_data.py
# José Devezas <joseluisdevezas@gmail.com>
# 2023-03-16

import re
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} FANDOM_SEASON_URL [MAX_EPISODE]")
    sys.exit(1)

url = sys.argv[1]
max_episode = int(sys.argv[2]) if len(sys.argv) >= 3 else None

data = requests.get(url)

soup = BeautifulSoup(data.content, "html5lib")

table = soup.select_one("#Voting_History").parent.find_next_sibling("table")
vote_trs = table.find_next("th", string=re.compile(r"\bVote\b")).parent.find_next_siblings("tr")

votes = {}

for tr in vote_trs:
    tds = tr.select("td")

    if len(tds) < 2:
        continue

    voter_td = tds[1]
    voted_tds = tds[2:]

    voter = voter_td.text.strip()
    voted = [td.text.strip() for td in voted_tds]

    print(voter, voted)
