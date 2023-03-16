# Survivor TV Show Network Analysis

Purely for fun, I decided to reproduce of the work by [Bonato et al. (2019)](https://arxiv.org/abs/1909.06810), where they proposed the Common Out-Neighbor score (CON), used to determine the next voted out contestant in the Survivor TV show, based on the prior network of votes.

The data we use is directly extracted from the Fandom Wiki for Survivor, and the script takes the URL for the season, as well as an optional maximum episode number, so that you can check the accuracy of the CON centrality score by yourself.

For example, for Survivor AU, season 10, entitled Heroes v Villains, you can compute the ranking scores based on the voting network up to episode 15 as follows:

```bash
$ ./compute_con_score.py "https://survivor.fandom.com/wiki/Australian_Survivor:_Heroes_v_Villains" 15
```

I might also explore this graph data later on again, using my own ideas, but, for now, it's been fun.
