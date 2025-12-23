const DATA_PATH = "../outputs/campaign_metrics_powerbi.csv";

const numberFormatter = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 0,
});
const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});
const percentFormatter = new Intl.NumberFormat("en-US", {
  style: "percent",
  maximumFractionDigits: 1,
});

document.addEventListener("DOMContentLoaded", () => {
  Papa.parse(DATA_PATH, {
    download: true,
    header: true,
    dynamicTyping: true,
    skipEmptyLines: true,
    complete: ({ data }) => {
      renderDashboard(data);
    },
    error: (err) => {
      console.error("Failed to load CSV", err);
      const root = document.querySelector("main");
      root.innerHTML =
        "<section class='panel'><p>Unable to load data file. Make sure outputs/campaign_metrics_powerbi.csv exists.</p></section>";
    },
  });
});

function renderDashboard(data) {
  const metrics = getCoreMetrics(data);
  renderKpis(metrics);
  renderCharts(data, metrics);
  renderLeaderboard(data);
  renderInsights(metrics);
}

function getCoreMetrics(data) {
  const sum = (field) =>
    data.reduce((acc, row) => acc + (Number(row[field]) || 0), 0);
  const avg = (field) => sum(field) / data.length || 0;

  const totalImpressions = sum("Impressions");
  const totalClicks = sum("Clicks");
  const totalSpend = sum("AdSpend ($)");
  const totalRevenue = sum("Revenue ($)");
  const totalConversions = sum("Conversions");
  const avgCTR = avg("CTR (%)");
  const avgROAS = avg("ROAS");
  const avgROI = avg("ROI (%)");

  const platformSummary = data.reduce((acc, row) => {
    const key = row.Platform;
    if (!acc[key]) {
      acc[key] = {
        spend: 0,
        revenue: 0,
        impressions: 0,
        roi: 0,
        roas: 0,
        count: 0,
      };
    }
    acc[key].spend += Number(row["AdSpend ($)"]) || 0;
    acc[key].revenue += Number(row["Revenue ($)"]) || 0;
    acc[key].impressions += Number(row["Impressions"]) || 0;
    acc[key].roi += Number(row["ROI (%)"]) || 0;
    acc[key].roas += Number(row["ROAS"]) || 0;
    acc[key].count += 1;
    return acc;
  }, {});

  Object.values(platformSummary).forEach((item) => {
    item.avgRoi = item.roi / item.count || 0;
    item.avgRoas = item.roas / item.count || 0;
  });

  return {
    totalImpressions,
    totalClicks,
    totalSpend,
    totalRevenue,
    avgCTR,
    avgROAS,
    avgROI,
    totalConversions,
    platformSummary,
  };
}

function renderKpis(metrics) {
  const kpis = [
    {
      label: "Total Impressions",
      value: numberFormatter.format(metrics.totalImpressions),
    },
    {
      label: "Total Clicks",
      value: numberFormatter.format(metrics.totalClicks),
    },
    {
      label: "Total Ad Spend",
      value: currencyFormatter.format(metrics.totalSpend),
    },
    {
      label: "Total Revenue",
      value: currencyFormatter.format(metrics.totalRevenue),
    },
    {
      label: "Average CTR",
      value: percentFormatter.format(metrics.avgCTR / 100),
    },
    {
      label: "Average ROAS",
      value: metrics.avgROAS.toFixed(2),
    },
    {
      label: "Average ROI",
      value: percentFormatter.format(metrics.avgROI / 100),
    },
    {
      label: "Total Conversions",
      value: numberFormatter.format(metrics.totalConversions),
    },
  ];

  const grid = document.getElementById("kpiGrid");
  grid.innerHTML = "";
  kpis.forEach((kpi) => {
    const card = document.createElement("article");
    card.className = "kpi-card";
    card.innerHTML = `
      <p class="kpi-label">${kpi.label}</p>
      <p class="kpi-value">${kpi.value}</p>
    `;
    grid.appendChild(card);
  });
}

function renderCharts(data, metrics) {
  const platformLabels = Object.keys(metrics.platformSummary);
  const platformSpend = platformLabels.map(
    (key) => metrics.platformSummary[key].spend
  );
  const platformColors = ["#5e4ae3", "#7b6cf6", "#ffb347"];

  const topCampaigns = [...data]
    .sort((a, b) => (b["ROAS"] || 0) - (a["ROAS"] || 0))
    .slice(0, 8);

  const months = {};
  data.forEach((row) => {
    const date = new Date(row.StartDate);
    if (Number.isNaN(date)) return;
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(
      2,
      "0"
    )}`;
    if (!months[key]) {
      months[key] = 0;
    }
    months[key] += Number(row["Revenue ($)"]) || 0;
  });
  const monthLabels = Object.keys(months).sort();
  const monthRevenue = monthLabels.map((label) => months[label]);

  new Chart(document.getElementById("platformSpendChart"), {
    type: "doughnut",
    data: {
      labels: platformLabels,
      datasets: [
        {
          data: platformSpend,
          backgroundColor: platformColors,
          borderWidth: 0,
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#dbe1ff" },
        },
      },
    },
  });

  new Chart(document.getElementById("topCampaignsChart"), {
    type: "bar",
    data: {
      labels: topCampaigns.map((row) => row.CampaignName),
      datasets: [
        {
          label: "ROAS",
          data: topCampaigns.map((row) => row.ROAS),
          backgroundColor: "#7b6cf6",
        },
      ],
    },
    options: {
      scales: {
        x: {
          ticks: { color: "#dbe1ff" },
        },
        y: {
          ticks: { color: "#dbe1ff" },
        },
      },
      plugins: {
        legend: { display: false },
      },
    },
  });

  new Chart(document.getElementById("revenueTrendChart"), {
    type: "line",
    data: {
      labels: monthLabels,
      datasets: [
        {
          label: "Revenue",
          data: monthRevenue,
          borderColor: "#ffb347",
          backgroundColor: "rgba(255, 179, 71, 0.15)",
          tension: 0.4,
          fill: true,
        },
      ],
    },
    options: {
      scales: {
        x: {
          ticks: { color: "#dbe1ff" },
        },
        y: {
          ticks: { color: "#dbe1ff" },
        },
      },
      plugins: {
        legend: { display: false },
      },
    },
  });
}

function renderLeaderboard(data) {
  const tbody = document.getElementById("leaderboardBody");
  tbody.innerHTML = "";
  const rows = [...data]
    .sort((a, b) => (b["ROAS"] || 0) - (a["ROAS"] || 0))
    .slice(0, 25);

  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.CampaignName}</td>
      <td>${row.Platform}</td>
      <td>${row.Objective}</td>
      <td>${currencyFormatter.format(row["AdSpend ($)"] || 0)}</td>
      <td>${currencyFormatter.format(row["Revenue ($)"] || 0)}</td>
      <td>${(row.ROAS || 0).toFixed(2)}</td>
      <td>${percentFormatter.format((row["ROI (%)"] || 0) / 100)}</td>
      <td>${percentFormatter.format((row["CTR (%)"] || 0) / 100)}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderInsights(metrics) {
  const platforms = metrics.platformSummary;
  const entries = Object.entries(platforms);

  const bestRoi = entries.reduce(
    (best, [platform, stats]) =>
      stats.avgRoi > best.value ? { platform, value: stats.avgRoi } : best,
    { platform: "", value: -Infinity }
  );

  const bestRoas = entries.reduce(
    (best, [platform, stats]) =>
      stats.avgRoas > best.value ? { platform, value: stats.avgRoas } : best,
    { platform: "", value: -Infinity }
  );

  const highestSpend = entries.reduce(
    (best, [platform, stats]) =>
      stats.spend > best.value ? { platform, value: stats.spend } : best,
    { platform: "", value: -Infinity }
  );

  const insights = [
    {
      title: "ROI Leader",
      body: `${bestRoi.platform} averages ${percentFormatter.format(
        bestRoi.value / 100
      )} ROI.`,
    },
    {
      title: "ROAS Standout",
      body: `${bestRoas.platform} delivers ROAS of ${bestRoas.value.toFixed(
        2
      )}.`,
    },
    {
      title: "Spend Focus",
      body: `${highestSpend.platform} accounts for ${currencyFormatter.format(
        highestSpend.value
      )} in spend.`,
    },
    {
      title: "Overall Efficiency",
      body: `Portfolio averages ${percentFormatter.format(
        metrics.avgROI / 100
      )} ROI and ROAS ${metrics.avgROAS.toFixed(2)}.`,
    },
  ];

  const grid = document.getElementById("insightsGrid");
  grid.innerHTML = "";
  insights.forEach((insight) => {
    const card = document.createElement("article");
    card.className = "insight-card";
    card.innerHTML = `
      <h4>${insight.title}</h4>
      <p>${insight.body}</p>
    `;
    grid.appendChild(card);
  });
}
