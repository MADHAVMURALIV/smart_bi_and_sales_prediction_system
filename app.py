from flask import Flask, render_template, request, jsonify, send_file
import os
import pandas as pd
import joblib
import webbrowser
from io import BytesIO

from utils.preprocessing import preprocess
from utils.ml_models import train_rf
from utils.forecasting import generate_future_data
from utils.inventory import inventory_plan

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

app = Flask(__name__)


import base64

def chart_from_base64(img_b64, width=400):
    if not img_b64:
        return None
    img_data = base64.b64decode(img_b64.split(",")[1])
    return Image(BytesIO(img_data), width=width, height=250)


#paths
UPLOAD_FOLDER = "data/uploads"
MODEL_FOLDER = "models"
IMG_FOLDER = "data/charts"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)
os.makedirs(IMG_FOLDER, exist_ok=True)

# routes

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

#file uploads

@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

   # preprocessing
    df, encoders, meta = preprocess(path)

    avg_sales = float(df["Sales"].mean())
    total_sales = float(df["Sales"].sum())

    app.config["AVG_SALES"] = avg_sales
    app.config["TOTAL_SALES"] = total_sales
    app.config["ENCODERS"] = encoders

    # model train
    model, preds, y_test, metrics = train_rf(df)
    joblib.dump(model, f"{MODEL_FOLDER}/rf_model.pkl")

    demand_deviation = float(abs(y_test - preds).mean())

    accuracy_pct = max(0, 100 - (metrics["MAE"] / avg_sales) * 100)

    if accuracy_pct >= 85:
        trend_consistency = "High"
    elif accuracy_pct >= 70:
        trend_consistency = "Medium"
    else:
        trend_consistency = "Low"

    app.config["DEMAND_DEVIATION"] = demand_deviation
    app.config["TREND_CONSISTENCY"] = trend_consistency

    # sales monthly
    monthly_df = (
        df.groupby(["Year", "Month"])["Sales"]
        .sum()
        .reset_index()
        .sort_values(["Year", "Month"])
    )

    monthly_labels = (
        monthly_df["Year"].astype(str) + "-" + monthly_df["Month"].astype(str)
    ).tolist()
    monthly_sales = monthly_df["Sales"].tolist()

    # forecasr 
    future_df = generate_future_data(df, months=6)
    future_sales = model.predict(future_df).tolist()
    inventory = inventory_plan(future_sales)

    app.config["FUTURE_SALES"] = future_sales
    app.config["INVENTORY"] = inventory



    demand_deviation = float(df["Sales"].std())
    trend_consistency = (
        "High" if demand_deviation < avg_sales * 0.15
        else "Medium" if demand_deviation < avg_sales * 0.3
        else "Low"
    )


    return jsonify({
        # Core numbers
        "avg_sales": round(avg_sales, 2),
        "total_revenue": round(total_sales, 2),

        "trend_consistency": trend_consistency,
        # Dashboard KPIs
        "demand_deviation": round(demand_deviation, 2),
        "trend_consistency": trend_consistency,
        "forecast_horizon": "6 Months",
        "model": "Random Forest",

        # Charts
        "actual": y_test.tolist(),
        "predicted": preds.tolist(),
        "months": df.iloc[-len(y_test):]["Month"].tolist(),

        "monthly_labels": monthly_labels,
        "monthly_sales": monthly_sales,

        "future_sales": future_sales,
        "inventory_plan": inventory,

        # Predict dropdowns
        "categories": meta["categories"],
        "regions": meta["regions"]
    })

#individual prediction

@app.route("/predict-single", methods=["POST"])
def predict_single():
    data = request.json
    model = joblib.load(f"{MODEL_FOLDER}/rf_model.pkl")
    enc = app.config.get("ENCODERS")

    row = pd.DataFrame([{
        "Year": int(data["year"]),
        "Month": int(data["month"]),
        "Category": enc["Category"].transform([data["category"]])[0],
        "Sub-Category": 0,
        "Region": enc["Region"].transform([data["region"]])[0]
    }])

    pred = model.predict(row)[0]

    return jsonify({
        "prediction": round(float(pred), 2),
        "avg_sales": round(app.config.get("AVG_SALES", 0), 2)
    })

# -report

@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.json
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Smart BI & Sales Prediction Report", styles["Title"]))
    elements.append(Spacer(1, 14))

    
    elements.append(Table([
        ["Metric", "Value"],
        ["Total Revenue", f"{app.config.get('TOTAL_SALES', 0):.2f}"],
        ["Average Sales", f"{app.config.get('AVG_SALES', 0):.2f}"],
        ["Demand Deviation", f"±{app.config.get('DEMAND_DEVIATION', 0):.2f} units"],
        ["Trend Consistency", app.config.get("TREND_CONSISTENCY", "N/A")],
        ["Forecast Horizon", "6 Months"]
    ]))

    elements.append(Spacer(1, 16))

    # ---- CHARTS ----
    elements.append(Paragraph("AI Prediction vs Actual Sales", styles["Heading2"]))
    img = chart_from_base64(data.get("sales_img"))
    if img: elements.append(img)

    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Future Sales Forecast", styles["Heading2"]))
    img = chart_from_base64(data.get("future_img"))
    if img: elements.append(img)

    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Average vs Predicted Sales", styles["Heading2"]))
    img = chart_from_base64(data.get("predict_img"))
    if img: elements.append(img)

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Smart_BI_Report.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000") # remove this for url in terminal 
    app.run(debug=True)
