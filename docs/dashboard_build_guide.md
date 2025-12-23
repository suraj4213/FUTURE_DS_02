## Power BI Dashboard Build Guide

This playbook mirrors the five-page experience described in the project brief. Replace placeholder texts (logo, company name, etc.) with your brand before publishing.

### 1. Data Model
- Import `outputs/campaign_metrics_powerbi.csv` as a single table named `Campaigns`.
- Ensure `Campaigns[StartDate]` and `Campaigns[EndDate]` are typed as `Date`.
- Create a Calendar table (optional) for time intelligence:
  ```DAX
  Calendar =
  ADDCOLUMNS (
      CALENDAR ( MIN ( Campaigns[StartDate] ), MAX ( Campaigns[EndDate] ) ),
      "YearMonth", FORMAT ( [Date], "YYYY-MM" ),
      "Year", YEAR ( [Date] ),
      "Month", FORMAT ( [Date], "MMM" )
  )
  ```
- Relate `Calendar[Date]` to `Campaigns[StartDate]` (Many-to-One, single direction).

### 2. Core Measures
- Add the DAX measures listed in the user brief. Recommended extras:
  ```DAX
  Total Engagement =
      SUM ( Campaigns[Likes] )
      + SUM ( Campaigns[Comments] )
      + SUM ( Campaigns[Shares] )

  Engagement Rate % =
      DIVIDE ( [Total Engagement], [Total Impressions], 0 ) * 100

  MoM Revenue Growth % =
  VAR CurrentMonth = [Total Revenue]
  VAR PreviousMonth =
      CALCULATE ( [Total Revenue], DATEADD ( Campaigns[StartDate], -1, MONTH ) )
  RETURN DIVIDE ( CurrentMonth - PreviousMonth, PreviousMonth, 0 ) * 100

  Underperforming Campaign ROI =
      CALCULATE ( [ROI %], Campaigns[ROI (%) ] < 100 )

  High Performer ROAS =
      CALCULATE ( [ROAS], Campaigns[ROAS] > 3 )
  ```

### 3. Page Layouts

#### Page 1 · Executive Overview
- **KPI cards (grid)**: Total Impressions, Total Clicks, Total Ad Spend, Total Revenue, Avg CTR, Avg ROAS, Avg ROI, Total Conversions.
- **Line chart**: Axis `Calendar[Date]`, values `[Total Impressions]`, `[Total Clicks]`, `[Total AdSpend]` (secondary axis).
- **Donut**: Field `Campaigns[Platform]`, value `[Total AdSpend]`.
- **Bar**: `Campaigns[CampaignName]` (Top N 10 by `[ROAS]`) vs `[ROAS]`.
- **Column**: Likes/Comments/Shares by `Platform` (use multi-measure column chart).
- **Card**: `[MoM Revenue Growth %]` with conditional formatting arrow.

#### Page 2 · Platform Performance
- **Table**: `Platform` with `[Total Impressions]`, `[Total Reach]`, `[CTR %]`, `[Engagement Rate %]`, `[Total AdSpend]`, `[Total Revenue]`, `[ROAS]`, `[ROI %]`, `[Total Conversions]`.
- **Clustered column**: Platform vs `[CTR %]`, `[Engagement Rate %]`, `[ROAS]`.
- **Area chart**: Axis `Calendar[Date]`, legend `Platform`, values `[Total Impressions]` & `[Total Reach]`.
- **Funnel**: Platform aggregated `Clicks → Conversions`.
- **Slicers**: Platform, Ad Type, Campaign Status, Start Date range.

#### Page 3 · Campaign Deep Dive
- **Matrix**: Rows `CampaignName`, Columns `Objective`, Values `[Total AdSpend]`, `[Total Revenue]`, `[ROAS]`, `[ROI %]`, `[Conversions]`.
- **Scatter**: X `[Total AdSpend]`, Y `[Total Revenue]`, Size `[Conversions]`, Details `CampaignName`, Play axis optional `Month`.
- **Treemap**: Group `Objective`, Details `AdType`, Values `[Total Revenue]`.
- **Waterfall**: Category `CampaignName` (Top 15), Breakdown `[Total Revenue]`.
- **Drill-through**: Enable on `CampaignName` to show per-campaign detail page (dup Page 3 visuals filtered).

#### Page 4 · Audience Insights
- **Stacked bar**: Axis `AudienceAge`, Legend `Platform`, Value `[Total Engagement]`.
- **Pie**: `AudienceGender`, `[Total Impressions]`.
- **Heat map**: Use matrix or custom visual: Rows `AudienceAge`, Columns `AdType`, Values `[ROAS]`.
- **Column**: `AudienceAge` vs `[CTR %]`, segmented by `AudienceGender`.

#### Page 5 · Optimization Recommendations
- **Table**: Filter `Campaigns[ROI (%)] < 100`, show spend, revenue, ROI, CTR.
- **Table**: Filter `Campaigns[ROAS] > 3`, highlight top performers.
- **Card visuals**: Use smart narrative or multi-row cards for recommendations (manual text).
- Optional: Add **What-If** parameters for budget reallocation.

### 4. UX Enhancements
- **Bookmarks & Navigation**: Create bookmark per page, add left-hand navigation buttons (icons) for quick jumps.
- **Reset Filters**: Insert blank bookmark with data, add button with action “Reset filters”.
- **Tooltips**: Build tooltip pages for scatter and treemap to show extra KPIs (CPM, CPC, Conversion Rate).
- **Branding**: Apply a color palette (e.g., `#1F2A44`, `#5E4AE3`, `#7B6CF6`, `#F2F4FF`). Use PowerPoint or Canva background exported as image and set as page background (Transparency 15%).
- **Logo Placeholder**: Add image visual with `CompanyLogo.png` placeholder (store in `dashboards/assets/` if available).

### 5. Publishing
- Save the PBIX as `dashboards/PowerBI/SocialMediaCampaignPerformance.pbix`.
- Update README with screenshot (File → Export → PDF or PNG).
- Set data source to `outputs/campaign_metrics_powerbi.csv`; refresh whenever new data is generated.

> **Tip**: Use field parameters (Power BI feature) to switch between CTR/ROI/ROAS in charts without duplicating visuals.
