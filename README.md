# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b101-front-page-dense/rank.svg)](https://make.fun/leaderboard/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b101-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up **23 November 2026** in a single image:
31 stories across 6 regions — the AI rout in Asia (Kospi −3.3%), Guterres urging
AI rules at the Bridgetown summit, and the US lead over China at a record low in
the Asia Power Index 2026.

## How it is made

- `draw.py` renders `entry.png` (1024×1024) with PIL — every scene is a drawn
  illustration, not a photograph.
- `main.py` (stdlib only) validates the PNG header/chunk structure and copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. It never writes next to itself.

## Stories

3 hero stories, 10 cards, 18 more in "ALSO ON MONDAY", plus a DATE CHECK box that
separates 23 November stories from earlier dates (Dems 258, Sparta II fire,
El Chapo captured, EU–Indonesia pact, Nigeria boat, ICJ Myanmar ruling) and
from stories not yet settled (Dymer search, 4 House races, COP32 venue, WHO
Ebola evacuation).

Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · ESPN ·
Lowy Institute (Asia Power Index 2026).
