import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

DATA_PATH = r"D:\smart-bi-sales-prediction\data\new_sales.csv"
MODEL_PATH = r"D:\smart-bi-sales-prediction\models\sales_model.pkl"

df = pd.read_csv(DATA_PATH)
X = df.drop("Sales", axis=1)
y = df["Sales"]

categorical_cols = ["Category", "Sub-Category", "Region"]
numeric_cols = ["Year", "Month"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols),
    ]
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#Linear Regression ----------
lr_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", LinearRegression())
    ]
)

lr_model.fit(X_train, y_train)
lr_preds = lr_model.predict(X_test)

print("Linear Regression:")
print("MAE:", mean_absolute_error(y_test, lr_preds))
print("R2 :", r2_score(y_test, lr_preds))
print("-" * 40)

#Random Forest 
rf_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=100,
            random_state=42
        ))
    ]
)

rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)

print("Random Forest:")
print("MAE:", mean_absolute_error(y_test, rf_preds))
print("R2 :", r2_score(y_test, rf_preds))

# pkl -Save Final Model ----------
joblib.dump(rf_model, MODEL_PATH)
print("Model saved as sales_model.pkl")
