# Topic Coverage + Sentiment (One-Figure Combo) — Python Project

This project computes sentiment for tweets (by topic) and generates a **single figure per topic** that overlays:
- **Boxplots** of **sentiment distribution** per time bucket (week or month), and
- A **coverage curve** (share of tweets) on a **secondary y-axis**.

## Data assumptions
- Input CSV has at least these columns:
  - `tweet_id` (optional)
  - `created_at` (string datetime; e.g. ISO format)
  - `text` (tweet text)
  - `topic` (topic label/cluster name)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 1) Compute sentiment
This will create a new CSV adding `sentiment` (compound VADER score in [-1, 1]).

```bash
python scripts/compute_sentiment.py   --input path/to/tweets.csv   --output data/tweets_with_sentiment.csv
```

### 2) Plot combined figure (sentiment boxplots + coverage curve)
You can choose weekly or monthly buckets.

```bash
python scripts/plot_topic_coverage_sentiment.py   --input data/tweets_with_sentiment.csv   --outdir figures   --time-bucket week
```

Outputs one PNG per topic, e.g. `figures/topic_<name>_week.png`.

## Notes
- Sentiment: NLTK VADER (auto-downloads the lexicon on first run).
- Coverage: share of tweets in a bucket, normalized by **total tweets in that same bucket** (not just the topic). This makes coverage comparable across time.
- If you want smoothed coverage, use `--smooth-window 7` (days) when bucketing daily; for weekly/monthly, smoothing is usually unnecessary.
- If your quarter spans multiple months, using `--time-bucket week` is recommended.
