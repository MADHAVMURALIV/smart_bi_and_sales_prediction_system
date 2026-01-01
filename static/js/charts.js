// ACTUAL vs PREDICTED SALES
let salesChart = null;

function renderSalesChart(data) {
  if (!data || !data.actual || !data.predicted || !data.months) {
    console.warn("Sales chart data missing");
    return;
  }

  const canvas = document.getElementById("salesChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  if (salesChart) salesChart.destroy();

  salesChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.months.map(m => `M${m}`),
      datasets: [
        {
          label: "Actual",
          data: data.actual,
          borderColor: "#16a34a",
          backgroundColor: "rgba(34,197,94,0.15)",
          tension: 0.3,
          pointRadius: 1.5
        },
        {
          label: "Predicted",
          data: data.predicted,
          borderColor: "#ef4444",
          backgroundColor: "rgba(239,68,68,0.15)",
          tension: 0.3,
          pointRadius: 1.5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { font: { size: 11 } }
        }
      },
      scales: {
        x: { ticks: { font: { size: 9 } } },
        y: { ticks: { font: { size: 9 } } }
      }
    }
  });
}

// METRICS
function updateMetrics(metrics) {
  if (!metrics) return;

  const mae = document.getElementById("mae");
  const r2 = document.getElementById("r2");

  if (mae) mae.innerText = metrics.MAE?.toFixed(2) ?? "--";
  if (r2) r2.innerText = metrics.R2?.toFixed(2) ?? "--";
}

// FUTURE SALES FORECAST

let futureChart = null;

function renderFutureChart(data) {
  // Safety check
  if (!data || !Array.isArray(data.future_sales) || data.future_sales.length === 0) {
    console.warn("Future sales data missing – skipping chart");
    return;
  }

  const canvas = document.getElementById("futureChart");
  if (!canvas) {
    console.error("futureChart canvas not found");
    return;
  }

  const ctx = canvas.getContext("2d");

  if (futureChart) {
    futureChart.destroy();
  }

  futureChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.future_sales.map((_, i) => `Month ${i + 1}`),
      datasets: [{
        label: "Future Sales Forecast",
        data: data.future_sales,
        backgroundColor: "#d946ef",

        
        barPercentage: 0.6,
        categoryPercentage: 0.7
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { font: { size: 11 } }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 10 } }
        },
        y: {
          beginAtZero: true,
          ticks: {
            font: { size: 9 },
            maxTicksLimit: 6
          }
        }
      }
    }
  });
}
// INVENTORY PLAN
function renderInventory(plan) {
  const list = document.getElementById("inventoryList");
  if (!list || !Array.isArray(plan)) return;

  list.innerHTML = "";

  plan.forEach((p, i) => {
    const li = document.createElement("li");
    li.innerText = `Month ${i + 1}: ${p}`;
    list.appendChild(li);
  });
}
// MONTHLY SALES TREND

let monthlyChart = null;

function renderMonthlyTrend(data) {
  if (
    !data ||
    !Array.isArray(data.monthly_labels) ||
    !Array.isArray(data.monthly_sales) ||
    data.monthly_labels.length === 0
  ) {
    console.warn("Monthly sales data missing");
    return;
  }

  const canvas = document.getElementById("monthlyChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  if (monthlyChart) monthlyChart.destroy();

  monthlyChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.monthly_labels,
      datasets: [{
        label: "Monthly Sales Trend",
        data: data.monthly_sales,
        borderColor: "#38bdf8",
        backgroundColor: "rgba(56,189,248,0.15)",
        tension: 0.3,
        pointRadius: 1.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { font: { size: 11 } } }
      },
      scales: {
        x: { ticks: { font: { size: 9 } } },
        y: { ticks: { font: { size: 9 } }, beginAtZero: false }
      }
    }
  });
}
