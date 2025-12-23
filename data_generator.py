"""
Synthetic social media campaign data generator.

This script creates a realistic multi-platform marketing dataset that can be
consumed by the cleaning and metric calculation pipelines as well as the
BI tools (Power BI, Looker Studio, Excel/Sheets).
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

OUTPUT_PATH = Path("data/raw_campaign_data.csv")
NUM_CAMPAIGNS = 650
SEED = 42


PLATFORMS = ["Facebook", "Instagram", "Twitter"]
AD_TYPES = ["Image", "Video", "Carousel", "Story"]
STATUSES = ["Active", "Paused", "Completed"]
AGE_SEGMENTS = ["18-24", "25-34", "35-44", "45+"]
GENDERS = ["M", "F", "All"]
OBJECTIVES = [
    "Awareness",
    "Traffic",
    "Engagement",
    "Conversions",
    "Sales",
]


@dataclass
class CampaignConfig:
    name_prefix: str
    objective_weights: List[float]


CAMPAIGN_CONFIG = {
    "Facebook": CampaignConfig("FB", [0.2, 0.25, 0.2, 0.2, 0.15]),
    "Instagram": CampaignConfig("IG", [0.25, 0.25, 0.25, 0.15, 0.1]),
    "Twitter": CampaignConfig("TW", [0.3, 0.3, 0.2, 0.1, 0.1]),
}


def _random_date() -> tuple[datetime, datetime]:
    start = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
    duration = random.randint(5, 40)
    end = start + timedelta(days=duration)
    return start, end


def _status_from_dates(end_date: datetime) -> str:
    today = datetime(2025, 1, 15)
    if end_date > today:
        return "Active"
    if (today - end_date).days < 15:
        return "Paused"
    return "Completed"


def _inject_missing(value: float, probability: float = 0.02) -> float | None:
    return None if random.random() < probability else value


def main() -> None:
    random.seed(SEED)
    np.random.seed(SEED)

    records = []

    for idx in range(1, NUM_CAMPAIGNS + 1):
        platform = random.choice(PLATFORMS)
        config = CAMPAIGN_CONFIG[platform]
        ad_type = random.choice(AD_TYPES)
        objective = random.choices(OBJECTIVES, weights=config.objective_weights, k=1)[0]

        start_date, end_date = _random_date()
        status = random.choice(STATUSES) if random.random() < 0.2 else _status_from_dates(end_date)

        impressions = random.randint(5_000, 750_000)
        reach = int(impressions * random.uniform(0.4, 0.9))
        clicks = max(1, int(impressions * random.uniform(0.005, 0.12)))
        likes = int(clicks * random.uniform(0.8, 2.5))
        comments = int(likes * random.uniform(0.05, 0.25))
        shares = int(likes * random.uniform(0.04, 0.2))
        video_views = int(impressions * random.uniform(0.1, 0.8)) if ad_type in {"Video", "Story"} else int(impressions * random.uniform(0.02, 0.15))
        link_clicks = int(clicks * random.uniform(0.4, 0.9))

        conversions = max(0, int(clicks * random.uniform(0.01, 0.15)))
        ad_spend = round(random.uniform(500, 45_000), 2)
        revenue_multiplier = random.uniform(0.5, 5.5)
        revenue = round(ad_spend * revenue_multiplier, 2)

        ctr = round((clicks / impressions) * 100, 2)
        engagement_rate = round(((likes + comments + shares) / impressions) * 100, 2)
        roi = round(((revenue - ad_spend) / ad_spend) * 100, 2)
        roas = round(revenue / ad_spend, 2)
        cpc = round(ad_spend / clicks, 2)
        cpm = round((ad_spend / impressions) * 1000, 2)
        conversion_rate = round((conversions / clicks) * 100, 2) if clicks else 0.0
        cost_per_conversion = round(ad_spend / conversions, 2) if conversions else None

        record = {
            "CampaignID": f"CMP-{idx:04d}",
            "CampaignName": f"{config.name_prefix}-{idx:04d}",
            "Platform": platform,
            "AdType": ad_type,
            "StartDate": start_date.strftime("%Y-%m-%d"),
            "EndDate": end_date.strftime("%Y-%m-%d"),
            "Status": status,
            "Impressions": impressions,
            "Reach": reach,
            "Clicks": clicks,
            "Likes": likes,
            "Comments": comments,
            "Shares": shares,
            "VideoViews": video_views,
            "LinkClicks": link_clicks,
            "CTR (%)": ctr,
            "EngagementRate (%)": engagement_rate,
            "AdSpend ($)": round(ad_spend, 2),
            "Revenue ($)": revenue,
            "Conversions": conversions,
            "ConversionRate (%)": conversion_rate,
            "CPC ($)": cpc,
            "CPM ($)": cpm,
            "ROAS": roas,
            "ROI (%)": roi,
            "AudienceAge": random.choice(AGE_SEGMENTS),
            "AudienceGender": random.choice(GENDERS),
            "Objective": objective,
        }

        record["CostPerConversion ($)"] = cost_per_conversion

        # Introduce sparse missingness to emulate real-world exports.
        record["Shares"] = _inject_missing(record["Shares"])
        record["Comments"] = _inject_missing(record["Comments"])

        records.append(record)

    df = pd.DataFrame(records)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(df)} campaign records at {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()

