from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)
MODEL_PATH = r"D:\smart-bi-sales-prediction\models\sales_model.pkl"
# Load Model 
model = joblib.load(MODEL_PATH)

# Prediction Route
@app.route("/predict", methods=["POST"])
def predict_sales():
    try:
        data = request.get_json()

        
        input_df = pd.DataFrame([{
            "Year": data["year"],
            "Month": data["month"],
            "Category": data["category"],
            "Sub-Category": data["sub_category"],
            "Region": data["region"]
        }])       
        prediction = model.predict(input_df)[0]
        return jsonify({
            "predicted_sales": round(float(prediction), 2)
        })
    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": str(e)}), 500


# ---------- Test Route start 
@app.route("/test")
def test():
    sample_input = pd.DataFrame([{
        "Year": 2018,
        "Month": 11,
        "Category": "Furniture",
        "Sub-Category": "Chairs",                                                       # bruno not working 
        "Region": "West"
    }])

    prediction = model.predict(sample_input)[0]

    return jsonify({
        "predicted_sales": round(float(prediction), 2)
    })
#-----------------------------------------------------------------------------test route end ..

#  HTML Route s
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/predict-page")
def predict_page():
    return render_template("predict.html")


# Server runn
if __name__ == "__main__":
    app.run(debug=True)

