#!/usr/bin/env python
import argparse
import os
import pandas as pd
from src.prepare import load_and_prepare, add_time_buckets
from src.coverage import compute_coverage
from src.plotting import plot_sentiment_boxplot_with_coverage
from src.utils import load_config


def main():
    ap = argparse.ArgumentParser(description="Plot per-topic: sentiment boxplots + coverage curve.")
    ap.add_argument("--config", default="config/config.yaml", help="Config file path.")
    ap.add_argument("--input", help="CSV with sentiment already added.")
    ap.add_argument("--outdir", help="Output directory for figures.")
    ap.add_argument("--time-col", help="Datetime column name (default: created_at)")
    ap.add_argument("--bucket", dest="bucket", default="week", choices=["day","week","month"], help="Time bucket granularity.")
    ap.add_argument("--smooth-window", type=int, default=None, help="Rolling window for coverage smoothing (only sensible for 'day').")
    args = ap.parse_args()

    

    config = load_config(args.config)

    outdir = args.outdir or config.get("figures_dir")

    time_col = args.time_col or config.get("time_col") or "created_at"
    bucket = args.bucket or config.get("time_bucket") or "week"
    smooth_window = args.smooth_window if args.smooth_window is not None else config.get("smooth_window")

    
    os.makedirs(args.outdir or outdir, exist_ok=True)
    
    df = load_and_prepare(args.input or config.get("input_for_plots_with_sentiment"), time_col=args.time_col or config.get("time_col") or "created_at")
    
     
    smooth_window = args.smooth_window if args.smooth_window is not None else config.get("smooth_window")
    if "sentiment" not in df.columns:
        raise ValueError("Input CSV must already have a 'sentiment' column. Run compute_sentiment.py first.")

    df = add_time_buckets(df, time_col=time_col, bucket=bucket)

    # Compute coverage per topic per bucket
    cov = compute_coverage(df, bucket_col="bucket", topic_col="topic")

    # Merge coverage back into original df (by bucket + topic)
    df_merged = df.merge(cov[["bucket","topic","coverage"]], on=["bucket","topic"], how="left")

    # For each topic, create a figure
    for topic, sub in df_merged.groupby("topic"):
        safe_topic = str(topic).replace("/", "_").replace(" ", "_")
        outpath = os.path.join(outdir, f"topic_{safe_topic}_{args.bucket}.png")
        plot_sentiment_boxplot_with_coverage(
            sub[["bucket","sentiment","coverage","topic"]].copy(),
            outpath=outpath,
            bucket_col="bucket",
            sentiment_col="sentiment",
            coverage_col="coverage",
            smooth_window=args.smooth_window
        )
        print(f"Wrote: {outpath}")

if __name__ == "__main__":
    main()
