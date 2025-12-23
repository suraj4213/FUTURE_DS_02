## Google Looker Studio Dashboard Guide

### Data Source
1. Upload `outputs/campaign_metrics_sheets.csv` to Google Drive → convert to Google Sheets (e.g., `Campaign_Metrics`).
2. In Looker Studio, create a new data source:
   - Connector: **Google Sheets** → select `Campaign_Metrics`.
   - Use first row as headers, auto-detect types.
3. Create calculated fields (type = Number, decimal):
   - `CTR Calculated = (Clicks / Impressions) * 100`
   - `Engagement Rate = ((Likes + Comments + Shares) / Impressions) * 100`
   - `ROI Calculated = ((Revenue - AdSpend) / AdSpend) * 100`
   - `ROAS Calculated = Revenue / AdSpend`
   - `Conversion Rate = (Conversions / Clicks) * 100`
4. Enable extract data (optional) for faster refresh.

### Report Pages

#### Page 1 · Campaign Overview
- **Scorecards**: Total Impressions, Total Clicks, Total Ad Spend, Total Revenue, CTR Calculated (average), ROAS Calculated (average), ROI Calculated (average), Total Conversions.
- **Time Series**: Dimension `StartDate`, Metrics `Impressions`, `Clicks`, `AdSpend`, `Revenue` (dual-axis).
- **Geo Map**: If location data not available, substitute with Platform map or remove.
- **Table**: `CampaignName`, Platform, AdType, AdSpend, Revenue, ROAS, ROI, CTR, Conversions (enable conditional formatting).
- **Controls**: Date range (StartDate), Filter for Platform.

#### Page 2 · Platform Analytics
- **Comparison table**: `Platform` dimension with aggregated metrics (Impressions, Clicks, CTR, Engagement Rate, Spend, Revenue, ROAS, ROI, Conversions).
- **Bar chart**: `Platform` vs `Likes`, `Comments`, `Shares`.
- **Pie chart**: `Platform` vs AdSpend.
- **Line chart**: Dimension `StartDate`, Breakdown `Platform`, Metric `CTR Calculated`.
- **Controls**: Platform, Ad Type, Campaign Status.

#### Page 3 · Ad Performance
- **Table with pagination**: `CampaignName`, `Platform`, `AdType`, `AdSpend`, `Revenue`, `ROAS`, `ROI`, `CTR`, `Conversion Rate`.
- **Heat map table**: Rows `AdType`, Columns `Platform`, Cell color by `ROAS`.
- **Combo chart**: `CampaignName` (Top 15) with bars `AdSpend` and line `Revenue`.
- **Bullet chart**: Actual vs Target (add constant control for target ROAS or ROI).

#### Page 4 · ROI Analysis
- **Scatter chart**: X `AdSpend`, Y `ROI Calculated`, Bubble size `Conversions`, Color `Platform`.
- **Table with conditional formatting**: highlight ROAS > 3 in green, <1 in red.
- **Scorecards**: Underperforming campaigns count (ROI < 100), High performer count (ROAS > 3).
- **Recommendations text box**: reference insights from `reports/insights.md`.

### Styling
- Theme: Custom palette (#1F2A44, #5E4AE3, #7B6CF6, #F2F4FF, #FFB347).
- Use Montserrat or Roboto for typography.
- Add company logo (Insert → Image) in header; include navigation buttons linking to each page.
- Enable responsive layout (Layout → Theme and Layout → Responsive).

### Sharing
- Grant Viewer access to stakeholders and enable link sharing (View only).
- For embedding: Share → Manage access → Allow embed. Paste iframe into intranet if needed.
- Document the public URL inside `reports/insights.md` once published.
