let AVG_SALES = 0;
let TOTAL_SALES = 0;
let predictChart = null;

// Upload CSV
function uploadCSV() {
  const fileInput = document.getElementById("csvFile");

  if (!fileInput || !fileInput.files.length) {
    alert("Please select a CSV file");
    return;
  }

  showLoader();

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  fetch("/upload-csv", {
    method: "POST",
    body: formData
  })
    .then(res => {
      if (!res.ok) throw new Error("Upload failed");
      return res.json();
    })
    .then(data => {
      // Core stats
      AVG_SALES = Number(data.avg_sales || 0);
      TOTAL_SALES = Number(data.total_sales || 0);

      // Update UI values
      setText("avgSalesValue", AVG_SALES.toFixed(2));
      setText("totalSalesValue", TOTAL_SALES.toFixed(2));
      setText("totalRevenue", data.total_revenue?.toFixed(2) || "0");

      // Charts & sections
      renderSalesChart(data);
      renderFutureChart(data);
      renderMonthlyTrend(data);
      renderInventory(data.inventory_plan);
      updateMetrics(data.metrics);

      // Dropdowns
      populateDropdown("pCategory", data.categories);
      populateDropdown("pRegion", data.regions);

// Demand Deviation
document.getElementById("demandDeviation").innerText =
  `±${Math.round(data.demand_deviation)} units`;

// Trend Consistency
const trendEl = document.getElementById("trendConsistency");
trendEl.innerText = data.trend_consistency;

trendEl.style.color =
  data.trend_consistency === "High" ? "#22c55e" :
  data.trend_consistency === "Medium" ? "#facc15" :
  "#ef4444";

    })
    .catch(err => {
      console.error(err);
      alert("Upload failed. Check console.");
    })
    .finally(hideLoader);
}

// Predict Sale
function predictSales() {
  const category = getVal("pCategory");
  const region = getVal("pRegion");
  const year = getVal("pYear");
  const month = getVal("pMonth");

  if (!category || !region) {
    alert("Select Category and Region");
    return;
  }

  if (!year || !month) {
    alert("Enter Year and Month");
    return;
  }

  showLoader();

  fetch("/predict-single", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ year, month, category, region })
  })
    .then(res => {
      if (!res.ok) throw new Error("Prediction failed");
      return res.json();
    })
    .then(data => {
      const prediction = Number(data.prediction || 0);
      setText("predictedValue", prediction.toFixed(2));
      renderPredictCompare(prediction);

      const status = document.getElementById("predictionStatus");
      if (!status) return;

      if (prediction > AVG_SALES) {
        status.innerText = "✅ Profit detected – refill inventory";
        status.style.color = "#22c55e";
      } else if (prediction === AVG_SALES) {
        status.innerText = "⚠️ Stable demand – no action required";
        status.style.color = "#eab308";
      } else {
        status.innerText = "❌ Loss detected – check inventory";
        status.style.color = "#ef4444";
      }
    })
    .catch(err => {
      console.error(err);
      alert("Prediction failed");
    })
    .finally(hideLoader);
}
// Download PDF Report
function downloadReport() {
  showLoader();
  captureCharts();

  fetch("/download-report", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sales_img: getVal("img_sales"),
      future_img: getVal("img_future"),
      predict_img: getVal("img_predict")
    })
  })
    .then(res => res.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "Smart_BI_Report.pdf";
      a.click();
    })
    .finally(hideLoader);
}
// Chart
function renderPredictCompare(predicted) {
  const canvas = document.getElementById("predictCompareChart");
  if (!canvas) return;

  if (predictChart) predictChart.destroy();

  predictChart = new Chart(canvas.getContext("2d"), {
    type: "bar",
    data: {
      labels: ["Average Sales", "Predicted Sales"],
      datasets: [{
        data: [AVG_SALES, predicted],
        backgroundColor: ["#64748b", "#2563eb"]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } }
    }
  });
}
// Helpers
function populateDropdown(id, items = []) {
  const select = document.getElementById(id);
  if (!select) return;

  select.innerHTML = "";
  items.forEach(v => {
    const opt = document.createElement("option");
    opt.value = v;
    opt.textContent = v;
    select.appendChild(opt);
  });
}

function captureCharts() {
  setVal("img_sales", getCanvasData("salesChart"));
  setVal("img_future", getCanvasData("futureChart"));
  setVal("img_predict", getCanvasData("predictCompareChart"));
}

function getCanvasData(id) {
  const c = document.getElementById(id);
  return c ? c.toDataURL("image/png") : "";
}

function updateMetrics(data = {}) {
  setText("demandDeviation", `±${data.demand_deviation || 0} units`);

  const trend = document.getElementById("trendConsistency");
  if (!trend) return;

  trend.innerText = data.trend_consistency || "Low";
  trend.style.color =
    data.trend_consistency === "High" ? "#22c55e" :
    data.trend_consistency === "Medium" ? "#eab308" :
    "#ef4444";
}

function showLoader() {
  const l = document.getElementById("loader");
  if (l) l.style.display = "flex";
}

function hideLoader() {
  const l = document.getElementById("loader");
  if (l) l.style.display = "none";
}

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.innerText = val;
}

function setVal(id, val) {
  const el = document.getElementById(id);
  if (el) el.value = val;
}

function getVal(id) {
  const el = document.getElementById(id);
  return el ? el.value : "";
}
