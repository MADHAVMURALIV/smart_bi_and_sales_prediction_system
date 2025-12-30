from flask import Flask, render_template, request, jsonify, send_file
import os
import pandas as pd
import joblib
import webbrowser
import base64
from io import BytesIO
from utils.preprocessing import preprocess
from utils.ml_models import train_rf
from utils.forecasting import generate_future_data
from utils.inventory import inventory_plan

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


app = Flask(__name__)
UPLOAD_FOLDER = "data/uploads"
MODEL_FOLDER = "models"
REPORT_PATH = "data/smart_bi_report.pdf"
IMG_FOLDER = "data/charts"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)
os.makedirs(IMG_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Routes
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# csv upload - process
@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    # Preprocess
    df, encoders, meta = preprocess(path)
    avg_sales = float(df["Sales"].mean())
    total_sales = float(df["Sales"].sum())
    app.config["AVG_SALES"] = avg_sales
    app.config["TOTAL_SALES"] = total_sales

    # train
    model, preds, y_test, metrics = train_rf(df)
    joblib.dump(model, f"{MODEL_FOLDER}/rf_model.pkl")

    app.config["ENCODERS"] = encoders

    #montly sale s
    monthly_df = (
        df.groupby(["Year", "Month"])["Sales"]
        .sum()
        .reset_index()
        .sort_values(["Year", "Month"])
    )
    monthly_labels = monthly_df["Year"].astype(str) + "-" + monthly_df["Month"].astype(str)
    monthly_sales = monthly_df["Sales"].tolist()
    app.config["MONTHLY_LABELS"] = monthly_labels.tolist()
    app.config["MONTHLY_SALES"] = monthly_sales

    #forecast
    future_df = generate_future_data(df, months=6)
    future_preds = model.predict(future_df)
    inventory = inventory_plan(future_preds.tolist())
    #pdf storing
    app.config["MAE"] = float(metrics["MAE"])
    app.config["R2"] = float(metrics["R2"])
    app.config["FUTURE_SALES"] = future_preds.tolist()
    app.config["INVENTORY"] = inventory

    return jsonify({
        "avg_sales": avg_sales,
        "total_sales": total_sales,
        "total_revenue": total_sales,
        "metrics": metrics,
        "actual": y_test.tolist(),
        "predicted": preds.tolist(),
        "months": df.iloc[-len(y_test):]["Month"].tolist(),

        "monthly_labels": monthly_labels.tolist(),
        "monthly_sales": monthly_sales,

        "future_months": future_df["Month"].tolist(),
        "future_sales": future_preds.tolist(),
        "inventory_plan": inventory,

        "categories": meta["categories"],
        "regions": meta["regions"]
    })
# Predict 
@app.route("/predict-single", methods=["POST"])
def predict_single():
    data = request.json
    model = joblib.load(f"{MODEL_FOLDER}/rf_model.pkl")
    enc = app.config.get("ENCODERS")
    if enc is None:
        return jsonify({"error": "Upload CSV first"}), 400

    row = pd.DataFrame([{
        "Year": int(data["year"]),
        "Month": int(data["month"]),
        "Category": enc["Category"].transform([data["category"]])[0],
        "Sub-Category": 0,
        "Region": enc["Region"].transform([data["region"]])[0]
    }])

    pred = model.predict(row)[0]
    return jsonify({"prediction": round(float(pred), 2)})

#Save chart image
def save_chart(base64_str, name):
    img_data = base64.b64decode(base64_str.split(",")[1])
    path = os.path.join(IMG_FOLDER, f"{name}.png")
    with open(path, "wb") as f:
        f.write(img_data)
    return path

@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.json

    sales_img = save_chart(data["sales_img"], "actual_vs_predicted")
    monthly_img = None
    if "monthly_img" in data and data["monthly_img"]:
        monthly_img = save_chart(data["monthly_img"], "monthly_sales")

    future_img = save_chart(data["future_img"], "future_sales")
    predict_img = save_chart(data["predict_img"], "avg_vs_predicted")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("Smart BI & Sales Prediction Report", styles["Title"]))
    elements.append(Spacer(1, 14))

    #summary
    elements.append(Paragraph("<b>Business Summary</b>", styles["Heading2"]))
    elements.append(Table([
        ["Metric", "Value"],
        ["Total Revenue", f"{app.config.get('TOTAL_SALES', 0):.2f}"],
        ["Average Sales", f"{app.config.get('AVG_SALES', 0):.2f}"]
    ]))
    elements.append(Spacer(1, 16))

    # Model Performance 
    elements.append(Paragraph("<b>Model Performance</b>", styles["Heading2"]))
    elements.append(Table([
        ["Metric", "Value"],
        ["MAE", f"{app.config.get('MAE', 0):.2f}"],
        ["R² Score", f"{app.config.get('R2', 0):.2f}"],
        ["Model", "Random Forest"],
        ["Forecast Horizon", "6 Months"]
    ]))
    elements.append(Spacer(1, 18))

    # charts
    elements.append(Paragraph("<b>Actual vs Predicted Sales</b>", styles["Heading2"]))
    elements.append(Image(sales_img, width=420, height=220))
    elements.append(Spacer(1, 18))

    if monthly_img:
        elements.append(Paragraph("<b>Monthly Sales Trend</b>", styles["Heading2"]))
        elements.append(Image(monthly_img, width=420, height=220))
        elements.append(Spacer(1, 18))

    elements.append(Paragraph("<b>Future Sales Forecast</b>", styles["Heading2"]))
    elements.append(Image(future_img, width=420, height=220))
    elements.append(Spacer(1, 18))

    elements.append(Paragraph("<b>Average vs Predicted Sales</b>", styles["Heading2"]))
    elements.append(Image(predict_img, width=420, height=220))
    elements.append(Spacer(1, 18))

    # inventory
    elements.append(Paragraph("<b>Inventory Planning</b>", styles["Heading2"]))
    inv_table = [["Month", "Action"]]
    for i, action in enumerate(app.config.get("INVENTORY", [])):
        inv_table.append([f"Month {i+1}", action])
    elements.append(Table(inv_table))

# Build PDF into memory
    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Smart_BI_Report.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")    # remove this ffor manual url access
    app.run(debug=True)
