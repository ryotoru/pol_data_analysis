#!/usr/bin/env python
import argparse
import pandas as pd
from src.prepare import load_and_prepare
from src.sentiment import compute_vader_sentiment
from src.utils import load_config
import os 


def main():
    ap = argparse.ArgumentParser(description="Compute VADER sentiment for tweets CSV.")
    ap.add_argument("--config", default="config/config.yaml", help="Config file path.")
    ap.add_argument("--input",  help="Input CSV with columns: created_at, text, topic, ...")
    ap.add_argument("--output", help="Output CSV path with added 'sentiment' column.")
    ap.add_argument("--time-col", help="Datetime column name (default: created_at)")
    args = ap.parse_args()

    config = load_config(args.config)

    df = load_and_prepare(args.input or config.get("input_path"), time_col=args.time_col or config.get("time_col")  or "created_at") 
    output_path = args.output or config.get("output_with_sentiment")
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if "tweets" not in df.columns:
        raise ValueError("Input CSV must have a 'tweet' column for sentiment.")
    df["sentiment"] = df["tweets"].apply(compute_vader_sentiment)
    df.to_csv(output_path, index=False)
    print(f"Wrote: {output_path}")

if __name__ == "__main__":
    main()
