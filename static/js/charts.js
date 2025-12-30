let salesChart = null;

function renderSalesChart(data) {
  const ctx = document.getElementById("salesChart").getContext("2d");

  if (salesChart) {
    salesChart.destroy();
  }

 salesChart = new Chart(ctx, {
  type: "line",                           
  data: {
    labels: data.months.map(m => `M${m}`),
    datasets: [
      {
        label: "Actual",
        data: data.actual,
        borderColor: "#007e65ff",      
        backgroundColor: "rgba(34,197,94,0.2)",
        tension: 0.3,
        pointRadius: 2
      },
      {
        label: "Predicted",
        data: data.predicted,
        borderColor: "#ff0000ff",      
        backgroundColor: "rgba(239,68,68,0.2)",
        tension: 0.3,
        pointRadius: 2
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          font: { size: 11 }
        }
      }
    },
    scales: {
      x: {
        ticks: { font: { size: 10 } }
      },
      y: {
        ticks: { font: { size: 10 } }
      }
    }
  }
});

}

function updateMetrics(metrics) {
  document.getElementById("mae").innerText = metrics.MAE.toFixed(2);
  document.getElementById("r2").innerText = metrics.R2.toFixed(2);
}

let futureChart = null;

function renderFutureChart(data) {
  const ctx = document.getElementById("futureChart").getContext("2d");

  if (futureChart) futureChart.destroy();

  futureChart = new Chart(ctx, {
    type: "bar",              // line , bar ,doughnut , polarArea , bubble , scatter  , radar  - alternatives
    data: {
      labels: data.future_months.map(m => `Month ${m}`),
      datasets: [{
        label: "Future Sales Forecast",
        borderColor: "#7a7a7aff",      // green
        backgroundColor: "rgba(234, 0, 255, 1)",
        data: data.future_sales,
        borderWidth: 1,
      }]
    },
    options: {
      responsive: true
    }
  });
}

function renderInventory(plan) {
  const list = document.getElementById("inventoryList");
  list.innerHTML = "";

  plan.forEach((p, i) => {
    const li = document.createElement("li");
    li.innerText = `Month ${i + 1}: ${p}`;
    list.appendChild(li);
  });
}

let monthlyChart = null;
function renderMonthlyTrend(data) {
  if (
    !data.monthly_labels ||
    !data.monthly_sales ||
    data.monthly_labels.length === 0
  ) {
    console.warn("Monthly sales data missing");
    return;
  }

  const canvas = document.getElementById("monthlyChart");
  if (!canvas) {
    console.error("monthlyChart canvas missing");
    return;
  }

  const ctx = canvas.getContext("2d");

  if (monthlyChart) monthlyChart.destroy();

  monthlyChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.monthly_labels,
      datasets: [{
        label: "Monthly Sales Trend",
        data: data.monthly_sales,
        tension: 0.3,
        pointRadius: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: false }
      }
    }
  });
}
