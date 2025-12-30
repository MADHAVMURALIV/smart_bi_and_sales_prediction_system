// Global state
let AVG_SALES = 0;
let TOTAL_SALES = 0;
let predictChart = null;

// Upload CSV
function uploadCSV() {
  const fileInput = document.getElementById("csvFile");

  if (!fileInput.files.length) {
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
      if (!res.ok) throw new Error("Server error");
      return res.json();
    })
    .then(data => {
      AVG_SALES = data.avg_sales;
      TOTAL_SALES = data.total_sales;

      document.getElementById("avgSalesValue").innerText = AVG_SALES.toFixed(2);
      document.getElementById("totalSalesValue").innerText = TOTAL_SALES.toFixed(2);
      document.getElementById("totalRevenue").innerText =
      "$" + data.total_revenue.toFixed(2);


      renderSalesChart(data);
      updateMetrics(data.metrics);
      renderFutureChart(data);
      renderInventory(data.inventory_plan);
      renderMonthlyTrend(data);

      populateDropdown("pCategory", data.categories);
      populateDropdown("pRegion", data.regions);
    })
    .catch(err => {
      console.error(err);
      alert("Upload failed. Check console.");
    })
    .finally(() => {
      hideLoader();   
    });
}

function downloadReport() {
  captureCharts();
  showLoader();
  fetch("/download-report", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sales_img: document.getElementById("img_sales").value,
      future_img: document.getElementById("img_future").value,
      predict_img: document.getElementById("img_predict").value
    })
  })
  .then(res => res.blob())
  .then(blob => {
    hideLoader();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Smart_BI_Report.pdf";
    a.click();
  });
}

//predict sales 

function predictSales() {
  const category = document.getElementById("pCategory").value;
  const region = document.getElementById("pRegion").value;
  const year = document.getElementById("pYear").value;
  const month = document.getElementById("pMonth").value;

  if (!category || !region) {
    alert("Please select Category and Region");
    return;
  }

  if (!year || !month) {
    alert("Please enter Year and Month");
    return;
  }

  showLoader();

  fetch("/predict-single", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      year: year,
      month: month,
      category: category,
      region: region
    })
  })
    .then(res => {
      if (!res.ok) throw new Error("Prediction failed");
      return res.json();
    })
    .then(data => {
      document.getElementById("predictedValue").innerText = data.prediction;
      renderPredictCompare(data.prediction);

      // Profit / Loss logic
      const status = document.getElementById("predictionStatus");

      if (data.prediction > AVG_SALES) {
        status.innerText = "✅ Profit detected – refill your inventory";
        status.style.color = "#22c55e";
      } else if (data.prediction === AVG_SALES) {
        status.innerText = " ⚠️ No change detected – inventory remains stable";
        status.style.color = "#eab308";
      } else {
        status.innerText = "❌ Loss detected – check your inventory";
        status.style.color = "#f97316";
      }

      hideLoader();
    })
    .catch(err => {
      console.error(err);
      hideLoader();
      alert("Prediction failed");
    });
}

// helper: populate dropdown

function populateDropdown(id, items) {
  const select = document.getElementById(id);
  select.innerHTML = "";

  items.forEach(v => {
    const opt = document.createElement("option");
    opt.value = v;
    opt.textContent = v;
    select.appendChild(opt);
  });
}

// Predict Comparison Chart
function renderPredictCompare(predicted) {
  const canvas = document.getElementById("predictCompareChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  if (predictChart) predictChart.destroy();

  predictChart = new Chart(ctx, {
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

    }
  });
}

// Loader helpers
function showLoader() {
  const loader = document.getElementById("loader");
  if (loader) loader.style.display = "flex";
}

function hideLoader() {
  const loader = document.getElementById("loader");
  if (loader) loader.style.display = "none";
}

function captureCharts() {
  document.getElementById("img_sales").value =
    document.getElementById("salesChart").toDataURL("image/png");

  document.getElementById("img_future").value =
    document.getElementById("futureChart").toDataURL("image/png");

  document.getElementById("img_predict").value =
    document.getElementById("predictCompareChart").toDataURL("image/png");
}
