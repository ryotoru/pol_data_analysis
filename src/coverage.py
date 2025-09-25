from __future__ import annotations
import pandas as pd

def compute_coverage(df: pd.DataFrame, bucket_col: str = "bucket", topic_col: str = "topic") -> pd.DataFrame:
    """Compute coverage per (bucket, topic) = topic_count / total_count_in_bucket."""
    # total per bucket
    total = df.groupby(bucket_col).size().rename("total_in_bucket")
    # per topic per bucket
    topic_counts = df.groupby([bucket_col, topic_col]).size().rename("topic_count").reset_index()
    cov = topic_counts.merge(total, on=bucket_col, how="left")
    cov["coverage"] = cov["topic_count"] / cov["total_in_bucket"]
    return cov  # columns: bucket, topic, topic_count, total_in_bucket, coverage
