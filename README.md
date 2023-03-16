# Survivor TV Show Network Analysis

Purely for fun, I decided to reproduce of the work by [Bonato et al. (2019)](https://arxiv.org/abs/1909.06810), where they proposed the Common Out-Neighbor score (CON), used to determine the next voted out contestant in the Survivor TV show, based on the prior network of votes.

## Data

The data we use is directly extracted from the Fandom Wiki for Survivor, and the script takes the URL for the season, as well as an optional maximum episode number, so that you can check the accuracy of the CON centrality score by yourself.

## Setup

In order to run the script, please use Python 3.11 (should work with previous versions, but it's untested), and set it up as follows:

```bash
python -m venv env
. env/bin/activate
pip install -r requirements.txt
```
## Example

You can then run the script. For example, for Survivor AU, season 10, entitled "Heroes v Villains", you can compute the ranking scores, for current contestants, based on the voting network up to episode 15, as follows:

```bash
./compute_con_score.py "https://survivor.fandom.com/wiki/Australian_Survivor:_Heroes_v_Villains" 15
```

Should produce:

```
        name  score
rank
1     Shonee     75
2      Simon     65
3        Liz     64
4     George     59
5      Gerry     56
6       Matt     48
7     Hayley     46
8       Nina     38
9      Shaun     36
10       Sam     34
```

This shows that, according to voting data until episode 15, Sam is the most likely to be voted out next, and Shonee is the best positioned to win (assuming the jury will vote for her at the end, of course).

## Future

I might also explore this graph data later on again, using my own ideas, but, for now, it's been fun.
