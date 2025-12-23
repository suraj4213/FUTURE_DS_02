"""
Metrics calculator for the Social Media Campaign Performance Tracker project.

Loads the cleaned dataset, recalculates KPI fields, and exports:
* CSV file for BI imports.
* Google Sheets compatible CSV.
* Multi-sheet Excel workbook summarising performance.
* Aggregated statistics used for documentation insights.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

CLEAN_DATA = Path("data/cleaned_campaign_data.csv")
POWERBI_CSV = Path("outputs/campaign_metrics_powerbi.csv")
SHEETS_CSV = Path("outputs/campaign_metrics_sheets.csv")
EXCEL_PATH = Path("outputs/campaign_metrics.xlsx")


def _calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["CTR (%)"] = ((df["Clicks"] / df["Impressions"]) * 100).round(2)
    df["EngagementRate (%)"] = (
        ((df["Likes"] + df["Comments"] + df["Shares"]) / df["Impressions"]) * 100
    ).round(2)
    df["ROI (%)"] = (
        ((df["Revenue ($)"] - df["AdSpend ($)"]) / df["AdSpend ($)"]) * 100
    ).round(2)
    df["ROAS"] = (df["Revenue ($)"] / df["AdSpend ($)"]).round(2)
    df["CPC ($)"] = (df["AdSpend ($)"] / df["Clicks"]).round(2)
    df["CPM ($)"] = ((df["AdSpend ($)"] / df["Impressions"]) * 1000).round(2)
    df["ConversionRate (%)"] = ((df["Conversions"] / df["Clicks"]) * 100).round(2)
    df["CostPerConversion ($)"] = (df["AdSpend ($)"] / df["Conversions"]).round(2)
    df = df.replace([pd.NA, pd.NaT], 0).fillna(0)
    return df


def _summaries(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    df["StartDate"] = pd.to_datetime(df["StartDate"])
    platform_summary = (
        df.groupby("Platform")
        .agg(
            TotalImpressions=("Impressions", "sum"),
            TotalClicks=("Clicks", "sum"),
            TotalSpend=("AdSpend ($)", "sum"),
            TotalRevenue=("Revenue ($)", "sum"),
            AvgCTR=("CTR (%)", "mean"),
            AvgROAS=("ROAS", "mean"),
            AvgROI=("ROI (%)", "mean"),
            TotalConversions=("Conversions", "sum"),
        )
        .round(2)
    )

    adtype_summary = (
        df.groupby("AdType")
        .agg(
            TotalImpressions=("Impressions", "sum"),
            TotalClicks=("Clicks", "sum"),
            AvgCTR=("CTR (%)", "mean"),
            AvgEngagement=("EngagementRate (%)", "mean"),
            AvgROAS=("ROAS", "mean"),
        )
        .round(2)
    )

    objective_summary = (
        df.groupby("Objective")
        .agg(
            TotalSpend=("AdSpend ($)", "sum"),
            TotalRevenue=("Revenue ($)", "sum"),
            AvgROI=("ROI (%)", "mean"),
            AvgROAS=("ROAS", "mean"),
        )
        .round(2)
    )

    daily = (
        df.groupby(pd.Grouper(key="StartDate", freq="D"))
        .agg(Impressions=("Impressions", "sum"), Revenue=("Revenue ($)", "sum"), Clicks=("Clicks", "sum"))
        .reset_index()
    )
    weekly = (
        df.groupby(pd.Grouper(key="StartDate", freq="W"))
        .agg(Impressions=("Impressions", "sum"), Revenue=("Revenue ($)", "sum"), Clicks=("Clicks", "sum"))
        .reset_index()
    )
    monthly = (
        df.groupby(pd.Grouper(key="StartDate", freq="ME"))
        .agg(Impressions=("Impressions", "sum"), Revenue=("Revenue ($)", "sum"), Clicks=("Clicks", "sum"))
        .reset_index()
    )

    return {
        "PlatformSummary": platform_summary,
        "AdTypeSummary": adtype_summary,
        "ObjectiveSummary": objective_summary,
        "DailyTrends": daily,
        "WeeklyTrends": weekly,
        "MonthlyTrends": monthly,
    }


def export_reports(df: pd.DataFrame) -> None:
    df.to_csv(POWERBI_CSV, index=False)
    df.to_csv(SHEETS_CSV, index=False)

    summaries = _summaries(df)
    with pd.ExcelWriter(EXCEL_PATH, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Campaigns", index=False)
        for sheet, data in summaries.items():
            data.to_excel(writer, sheet_name=sheet, index=True)


def main() -> None:
    cleaned = pd.read_csv(CLEAN_DATA)
    calculated = _calculate_metrics(cleaned)
    export_reports(calculated)
    print("Metrics exported to outputs/ directory")


if __name__ == "__main__":
    main()

