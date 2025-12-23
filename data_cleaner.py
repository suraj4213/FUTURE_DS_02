"""
Data cleaning utility for the social media campaign dataset.

Responsibilities:
* Remove duplicates and invalid rows.
* Standardise date formats.
* Recalculate derived metrics for verification.
* Handle missing values using pragmatic business rules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

RAW_PATH = Path("data/raw_campaign_data.csv")
CLEAN_PATH = Path("data/cleaned_campaign_data.csv")


def _ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    required = [
        "Impressions",
        "Clicks",
        "Likes",
        "Comments",
        "Shares",
        "AdSpend ($)",
        "Revenue ($)",
        "Conversions",
    ]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in raw data: {missing}")
    return df


def _clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    df["StartDate"] = pd.to_datetime(df["StartDate"], errors="coerce")
    df["EndDate"] = pd.to_datetime(df["EndDate"], errors="coerce")
    return df


def _handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [
        "Impressions",
        "Reach",
        "Clicks",
        "Likes",
        "Comments",
        "Shares",
        "VideoViews",
        "LinkClicks",
        "AdSpend ($)",
        "Revenue ($)",
        "Conversions",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    return df


def _recalculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    impressions = df["Impressions"].replace(0, np.nan)
    clicks = df["Clicks"].replace(0, np.nan)
    conversions = df["Conversions"].replace(0, np.nan)
    ad_spend = df["AdSpend ($)"].replace(0, np.nan)

    df["CTR (%)"] = ((df["Clicks"] / impressions) * 100).round(2)
    df["EngagementRate (%)"] = (
        ((df["Likes"] + df["Comments"] + df["Shares"]) / impressions) * 100
    ).round(2)
    df["ROI (%)"] = (((df["Revenue ($)"] - df["AdSpend ($)"]) / ad_spend) * 100).round(2)
    df["ROAS"] = (df["Revenue ($)"] / ad_spend).round(2)
    df["CPC ($)"] = (df["AdSpend ($)"] / clicks).round(2)
    df["CPM ($)"] = ((df["AdSpend ($)"] / impressions) * 1000).round(2)
    df["ConversionRate (%)"] = ((df["Conversions"] / clicks) * 100).round(2)
    df["CostPerConversion ($)"] = (df["AdSpend ($)"] / conversions).round(2)

    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    return df


def clean_dataset(raw_path: Path = RAW_PATH, output_path: Path = CLEAN_PATH) -> Tuple[Path, int]:
    df = pd.read_csv(raw_path)
    df = df.drop_duplicates(subset="CampaignID")
    df = _ensure_columns(df)
    df = _clean_dates(df)
    df = _handle_missing(df)
    df = _recalculate_metrics(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d")
    return output_path, len(df)


if __name__ == "__main__":
    path, count = clean_dataset()
    print(f"Cleaned dataset with {count} rows saved to {path.resolve()}")

