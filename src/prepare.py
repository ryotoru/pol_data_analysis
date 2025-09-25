from __future__ import annotations
import pandas as pd

def load_and_prepare(path: str, time_col: str = "created_at") -> pd.DataFrame:
    df = pd.read_csv(path)
    if time_col not in df.columns:
        raise ValueError(f"Missing time column '{time_col}' in CSV")
    # parse time
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce", utc=True)
    df = df.dropna(subset=[time_col])
    # normalize text fields if present
    if "text" in df.columns:
        df["text"] = df["text"].astype(str)
    if "topic" not in df.columns:
        raise ValueError("Input CSV must have a 'topic' column.")
    return df

def add_time_buckets(df: pd.DataFrame, time_col: str = "created_at", bucket: str = "week") -> pd.DataFrame:
    if bucket not in {"day", "week", "month"}:
        raise ValueError("bucket must be one of {'day','week','month'}")
    dt = df[time_col].dt
    if bucket == "day":
        df["bucket"] = dt.floor("D")
    elif bucket == "week":
        # ISO week start Monday: floor to weekly
        df["bucket"] = dt.to_period("W-MON").apply(lambda p: p.start_time.tz_localize("UTC"))
    else:  # month
        df["bucket"] = dt.to_period("M").apply(lambda p: p.start_time.tz_localize("UTC"))
    return df
