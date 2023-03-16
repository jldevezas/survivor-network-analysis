#!/usr/bin/env python
#
# extract_wiki_data.py
# José Devezas <joseluisdevezas@gmail.com>
# 2023-03-16

import sys

import igraph
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def pd_adjacency(g):
    return pd.DataFrame(g.get_adjacency(attribute="weight"), index=g.vs["name"], columns=g.vs["name"])


def CON_pair(A, u, v):
    """Common Out-Neighbor score for two nodes"""
    return A.loc[[u["name"], v["name"]]].min(axis=0).sum()


def CON_single(A, u):
    """Common Out-Neighbor score for one node"""
    return np.sum(np.fromiter((CON_pair(A, u, g.vs.select(name=v_name)[0]) for v_name in A.columns), dtype=np.int32))


def CON(A, u, v=None):
    """Common Out-Neighbor score for one or two nodes"""

    if v is None:
        return CON_single(A, u)

    return CON_pair(A, u, v)


if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} FANDOM_SEASON_URL [MAX_EPISODE]")
    sys.exit(1)

url = sys.argv[1]
max_episode = int(sys.argv[2]) if len(sys.argv) >= 3 else None

data = requests.get(url)

soup = BeautifulSoup(data.content, "html5lib")

table = soup.select_one("#Voting_History").parent.find_next_sibling("table")
df = pd.read_html(str(table), header=(0, 1, 2, 3))[0]

# Extract voted out
voted_out = df.T.reset_index().T.iloc[[1, 2], 2:]
voted_out = voted_out.rename(dict(level_1="Episode", level_2="Voted Out")).T
voted_out.set_index("Episode", inplace=True)
voted_out.replace(["Mock Vote", "Tie", "Mutiny"], np.nan, inplace=True)

# Drop last row (Notes)
df = df.iloc[:-1, :]

# Drop the first column (arrows)
df.drop(columns=df.columns[0:1], inplace=True)

##
# Identify and drop all columns with Jury votes (when available)
##

jury_vote_cols = df.iloc[0].index[df.iloc[0] == "Jury Vote"]

if len(jury_vote_cols) > 0:
    jury_vote_col = jury_vote_cols[0]
else:
    jury_vote_col = None

try:
    jury_col_idx = (df.columns == jury_vote_col).tolist().index(True)
    df.drop(columns=df.columns[jury_col_idx:], inplace=True)
except ValueError:
    pass

# Set column index as "Episode" and row index as "Voter"
df = df.T.reset_index().rename(columns=dict(level_1="Episode")).set_index("Episode").T.iloc[3:]
df = df.rename(columns=dict(Episode="Voter")).set_index("Voter")

# Replace empty votes or specific actions (e.g, Eliminated) by NaN
df.replace(["—", "Eliminated", "Evacuated", "Quit", "Returned", "None", "None6", "Exempt2"], np.nan, inplace=True)

# Ignore data prior to max_episode and remove other non-numeric "episode columns" (FIXME might miss data)
if max_episode:
    ignore_episodes = [episode for episode in df.columns if not episode.isnumeric() or int(episode) > max_episode]
    df.drop(columns=ignore_episodes, inplace=True)
    voted_out.drop(index=ignore_episodes, inplace=True)

##
# Extract voting data edges
##

votes = {}

for voter, row in df.iterrows():
    votes[voter] = row.dropna().tolist()

# Build the graph
g = igraph.Graph.TupleList([(k, v, 1) for k, vs in votes.items() for v in vs], directed=True, edge_attrs=["weight"])
# print(g)

# Collapse multiple edges into a single weighted edge
g.simplify(combine_edges="sum")
# print(g.es[0])

# Get names of voted out contestants
voted_out_names = voted_out.iloc[:, 0].dropna().tolist()

##
# Run the ranking analysis
##

names = []
scores = []
A = pd_adjacency(g)

for v in g.vs:
    names.append(v["name"])
    scores.append(CON(A, v))

ranking = pd.DataFrame(dict(name=names, score=scores)).sort_values(by="score", ascending=False)
ranking = ranking[~ranking.name.isin(voted_out_names)]
ranking.reset_index(drop=True, inplace=True)
ranking.index.rename("rank", inplace=True)
ranking.index += 1

print(ranking)
