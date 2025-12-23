## Social Media Campaign Performance Tracker

Interactive marketing analytics toolkit designed to evaluate Facebook, Instagram, and Twitter ad campaigns across Power BI, Google Looker Studio, Excel/Sheets, and Canva.

### Project Overview
- **Goal**: Provide a repeatable pipeline (data → cleanup → metrics → dashboards) for CTR, ROAS, ROI, CPC, CPM, engagement, and conversion KPIs.
- **Deliverables**: Python data stack, BI-ready exports, dashboard build guides, insights memo, and optional Canva report brief.
- **Audience**: Growth marketers, media buyers, analysts needing consistent reporting across multiple tooling ecosystems.

### Repository Structure
- `data_generator.py` · synthetic campaign data creator (650 records, 2024 coverage).
- `data_cleaner.py` · duplicate removal, missing value handling, derived metric validation.
- `metrics_calculator.py` · KPI recalculation plus platform/ad-type/objective/time summaries; exports CSV + XLSX.
- `data/` · raw and cleaned datasets.
- `outputs/` · BI-ready CSVs and Excel workbook with multiple analysis tabs.
- `dashboards/` · implementation playbooks for Power BI, Looker Studio, Excel/Sheets, and Canva.
- `reports/insights.md` · narrative of key findings & optimization ideas.
- `docs/dashboard_build_guide.md` · consolidated setup + DAX + styling guidance (Power BI focus).
- `docs/looker_studio_guide.md` · data source, calculated fields, widget mapping.
- `docs/excel_tracker_guide.md` · workbook blueprint, formulas, visualization tips.
- `docs/canva_template_brief.md` · creative requirements for the optional report.
- `web/` · lightweight web UI that reads `outputs/campaign_metrics_powerbi.csv` and surfaces KPIs/charts via Chart.js.
- `run_project.bat` · Windows helper script that runs the full Python pipeline and starts the local web server.
- `.gitignore` · excludes generated datasets, outputs, IDE files, and platform artifacts.
- `LICENSE` · MIT license covering all code/resources in this repository.

### Tooling & Versions
- Python 3.13 + pandas 2.3, numpy 2.3, XlsxWriter 3.2 (see `requirements.txt`).
- Power BI Desktop (Oct 2024 or later recommended for on-object interactions).
- Google Looker Studio (web).
- Microsoft Excel 365 Desktop / Google Sheets.
- Canva (Pro template recommended, but optional).

### Data Pipeline
1. `python data_generator.py` → `data/raw_campaign_data.csv`
2. `python data_cleaner.py` → `data/cleaned_campaign_data.csv`
3. `python metrics_calculator.py` → `outputs/campaign_metrics_powerbi.csv`, `campaign_metrics_sheets.csv`, `campaign_metrics.xlsx`

Each stage can be re-run independently; scripts automatically overwrite prior outputs.

### Metric Definitions
- `CTR (%) = (Clicks / Impressions) * 100`
- `EngagementRate (%) = ((Likes + Comments + Shares) / Impressions) * 100`
- `ROI (%) = ((Revenue - AdSpend) / AdSpend) * 100`
- `ROAS = Revenue / AdSpend`
- `CPC ($) = AdSpend / Clicks`
- `CPM ($) = (AdSpend / Impressions) * 1000`
- `ConversionRate (%) = (Conversions / Clicks) * 100`
- `Cost Per Conversion ($) = AdSpend / Conversions`

### Dashboard Assets
- **Power BI**: Follow `docs/dashboard_build_guide.md` for page layouts, slicers, bookmarks, reset buttons, and DAX measures supplied in the spec. Export final interactive report to `dashboards/PowerBI/SocialMediaCampaigns.pbix` (placeholder).
- **Looker Studio**: Use `dashboards/looker_studio_guide.md` to connect Google Sheets, add calculated fields, and configure four report pages mirroring Power BI.
- **Excel/Google Sheets Tracker**: Blueprint in `docs/excel_tracker_guide.md` with sheet-by-sheet formulas, pivot tables, slicers, sparklines, and conditional formatting.
- **Canva Report** (optional): Layout guidance plus asset checklist in `docs/canva_template_brief.md`.

### Insights Snapshot (based on latest synthetic run)
- Facebook led ROI (≈209%) and ROAS (≈3.09) making it the priority scaling channel.
- Video ads edged other formats for ROAS (~2.98) with Story and Carousel close behind; static images lagged at 2.83.
- Conversion-focused objectives generated the strongest ROI (>203%), followed by Traffic and Engagement intents.
- Audiences aged 25-34 delivered the best ROI (~199%), suggesting incremental budget shifts toward that cohort.
- Revenue spikes were observed in Jan and May 2024, indicating seasonal uplift windows for spend acceleration.

See `reports/insights.md` for detailed commentary and optimization recommendations.

### Setup & Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run the three Python scripts sequentially (commands above).
3. Import `outputs/campaign_metrics_powerbi.csv` into Power BI using the supplied DAX & layout plan.
4. Publish a Google Sheets copy of `campaign_metrics_sheets.csv` and connect it to Looker Studio per guide.
5. Build Excel tracker referencing the XLSX workbook tabs, or recreate formulas in Google Sheets.
6. Populate Canva template with exported visuals/screenshots from BI tools.
7. Preview the web dashboard: `python -m http.server 8000` from the repo root, then browse to `http://localhost:8000/web/`.

### One-Click Run
- Windows users can double-click `run_project.bat` (or execute it from PowerShell/CMD) to run the full Python pipeline and automatically launch the local web server plus browser tab pointed at the analytics UI.

### Licensing
- This project is released under the MIT License (see `LICENSE` for details). Feel free to adapt the scripts, guides, and web UI for personal or commercial use with attribution.

### Key Questions Answered
- Which platform maximizes ROI & ROAS?
- Which ad types and objectives outperform per platform?
- How should spend be reallocated for optimal conversions?
- Which campaigns exceed ROAS > 3 vs. underperformers with ROI < 100%?
- What demographic segments respond best?
- Where are seasonal peaks/dips occurring across the calendar?

### Next Steps
- Automate data refresh (e.g., schedule scripts with Windows Task Scheduler or GitHub Actions).
- Integrate real ad platform APIs to replace synthetic data.
- Extend to additional channels (LinkedIn, TikTok) and include creative-level metadata.
- Layer attribution models (first-touch / last-touch) for deeper ROI accuracy.

