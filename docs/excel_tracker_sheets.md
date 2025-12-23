## Excel / Google Sheets Tracker Guide

### Sheet 1 · `Raw_Data`
- Import `outputs/campaign_metrics_sheets.csv`.
- Convert to Table (`Ctrl + T`) named `tblCampaigns`.
- Apply data validation (Data → Data Validation) for:
  - `Platform` list: Facebook, Instagram, Twitter.
  - `AdType` list: Image, Video, Carousel, Story.
  - `Status` list: Active, Paused, Completed.
- Freeze top row + enable filters.

### Sheet 2 · `Calculated_Metrics`
- Reference table columns with structured references, e.g. `=[@[Clicks]]/[@[Impressions]]`.
- Suggested columns:
  - `CTR` → `=IFERROR([@[Clicks]]/[@[Impressions]],0)`
  - `EngagementRate` → `=IFERROR(([@[Likes]]+[@[Comments]]+[@[Shares]])/[@[Impressions]],0)`
  - `ROI` → `=IFERROR(([@[Revenue]]-[@[AdSpend]])/[@[AdSpend]],0)`
  - `ROAS` → `=IFERROR([@[Revenue]]/[@[AdSpend]],0)`
  - `CPC` → `=IFERROR([@[AdSpend]]/[@[Clicks]],0)`
  - `CPM` → `=IFERROR(([@[AdSpend]]/[@[Impressions]])*1000,0)`
  - `ConversionRate` → `=IFERROR([@[Conversions]]/[@[Clicks]],0)`
  - Format as percentages/currency where appropriate.
- Add conditional formatting icon sets for CTR, ROAS, ROI.

### Sheet 3 · `Platform_Summary`
- Option 1: Pivot Table from `tblCampaigns`.
  - Rows: Platform.
  - Values: Sum of Impressions, Clicks, AdSpend, Revenue, Conversions.
  - Values: Average of CTR, ROAS, ROI (calculated fields).
- Option 2: Formulas.
  - `TotalImpressions (Facebook)` → `=SUMIFS(Raw_Data!Impressions, Raw_Data!Platform, "Facebook")`.
  - Use `SUMIFS` / `AVERAGEIFS` for other metrics.
- Apply conditional formatting (color scale) to highlight best/worst.

### Sheet 4 · `Dashboard`
- Create KPI cards using merged cells referencing named ranges (e.g., `=Platform_Summary!B2`).
- Charts:
  - Column: Platform vs Total AdSpend.
  - Line: Monthly trend using `PivotChart` or `=SUMIFS` by `StartDate`.
  - Pie: Ad Spend distribution by platform.
  - Bar: Top 10 campaigns by ROAS (`=LARGE` or Pivot filter).
- Add slicers (Insert → Slicer) for Platform, Objective, Status (Excel only). For Google Sheets, use filter views or dropdowns.
- Include Sparklines for Impressions/Revenue trends per platform.

### Sheet 5 · `Campaign_Insights`
- **Top Performers**: `=FILTER(Raw_Data!A:Z, Raw_Data!ROAS > 3)` (Sheets) or Table filter (Excel).
- **Underperformers**: ROI < 0.5 (50%).
- **Recommendations**: Text boxes referencing insights (e.g., “Shift +10% budget to Facebook Video campaigns”).
- Add bullet icons via conditional formatting (e.g., Wingdings) for quick-glance statuses.

### Google Sheets Tips
- Replace table references with A1 ranges; use `ARRAYFORMULA` for entire columns.
- Use `QUERY` for dynamic views; example:  
  `=QUERY(Raw_Data!A:Z, "SELECT B, C, R WHERE R > 3 ORDER BY R DESC LIMIT 10", 1)`
- Share workbook with “Anyone with the link (Viewer)” for Looker Studio connection.
- Protect formula ranges to prevent accidental edits.

### Automation
- Excel: Refresh all tables (Data → Refresh All) after regenerating CSV.
- Sheets: Use `IMPORTRANGE` to pull data from master tracker to reporting sheets.

### Deliverable
- Save Excel as `dashboards/Excel/SocialMediaTracker.xlsx`.
- For Google Sheets, document the share URL inside `reports/insights.md`.
