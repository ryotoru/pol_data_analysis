from __future__ import annotations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
import matplotlib.dates as mdates

def plot_sentiment_boxplot_with_coverage(
    df_topic: pd.DataFrame,
    outpath: str,
    bucket_col: str = "bucket",
    sentiment_col: str = "sentiment",
    coverage_col: str = "coverage",
    smooth_window: Optional[int] = None
) -> None:
    """Create one figure: sentiment boxplots per bucket + coverage curve on a twin axis.

    Expects df_topic to contain at least [bucket_col, sentiment_col, coverage_col].
    """
    # Sort by bucket for coherent x-axis
    df_topic = df_topic.sort_values(bucket_col)
    buckets = df_topic[bucket_col].drop_duplicates().sort_values()

    # Prepare coverage series per bucket (median coverage if multiple rows per bucket-topic)
    cov_series = df_topic.groupby(bucket_col)[coverage_col].median().reindex(buckets, fill_value=np.nan)

    # Optional smoothing (use for 'day' buckets; for week/month it's often unnecessary)
    if smooth_window and smooth_window > 1:
        cov_series = cov_series.rolling(window=smooth_window, min_periods=1, center=True).mean()

    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Boxplots of sentiment per bucket (left y-axis)
    data_per_bucket = [df_topic.loc[df_topic[bucket_col] == b, sentiment_col].dropna().values for b in buckets]
    positions = np.arange(len(buckets)) + 1  # 1-based positions for matplotlib boxplot
    ax1.boxplot(data_per_bucket, positions=positions, widths=0.6, showfliers=False)
    ax1.set_ylabel("Sentiment (VADER compound)")
    ax1.set_xlabel("Time buckets")
    ax1.set_ylim(-1.05, 1.05)

    # x-ticks (sparse to avoid clutter)
    labels = [pd.to_datetime(b).strftime("%Y-%m-%d") for b in buckets]
    max_ticks = 10
    if len(labels) > max_ticks:
        step = int(np.ceil(len(labels) / max_ticks))
        ax1.set_xticks(positions[::step])
        ax1.set_xticklabels(labels[::step], rotation=30, ha="right")
    else:
        ax1.set_xticks(positions)
        ax1.set_xticklabels(labels, rotation=30, ha="right")

    # Coverage curve on twin y-axis
    ax2 = ax1.twinx()
    ax2.plot(positions, cov_series.values, marker="o")  # default matplotlib style, no explicit colors
    ax2.set_ylabel("Coverage (share of tweets)")
    ax2.set_ylim(0, min(1.0, max(0.05, float(np.nanmax(cov_series.values)) * 1.2)) if len(cov_series) else 1.0)

    # Title from topic if present
    topic_val = df_topic["topic"].iloc[0] if "topic" in df_topic.columns and len(df_topic) else "topic"
    ax1.set_title(f"Topic: {topic_val} — Sentiment Boxplots + Coverage Curve")

    fig.tight_layout()
    fig.savefig(outpath, dpi=200)
    plt.close(fig)
