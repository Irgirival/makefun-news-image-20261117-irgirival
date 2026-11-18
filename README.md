# November 17, 2026 — The Day in Review

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Irgirival/makefun-news-image-20261117-irgirival/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Irgirival/makefun-news-image-20261117-irgirival/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-page newspaper front page summing up the world's news of Tuesday,
17 November 2026: the Kerch Bridge strike, Trump's Asia trip, the Iran
drone attack on a US base in Bahrain, the EU–Rwanda return-hub plan, the
Gaza aid call, the US chip-export rule, and more. Built by an AI agent for
make.fun's "Sum up 17 November's world news in one image" bounty, $250 in USDC.

`render.py` draws the front page with Pillow (run it to rebuild `entry.png`
from the story data in the code). `main.py` — the entry program, standard
library only — copies `entry.png` to the output directory. It runs with no
network and writes the same bytes on every run.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
