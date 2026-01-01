from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd 

def train_rf(df):
    #sort for time dependency
    df = df.sort_values(["Year", "Month"]).reset_index(drop=True)

    #ADD TEMPORAL FEATURES (core accuracy fix)
    df["lag_1"] = df["Sales"].shift(1)
    df["lag_3"] = df["Sales"].shift(3)
    df["roll_3"] = df["Sales"].rolling(3).mean()
    df["roll_6"] = df["Sales"].rolling(6).mean()

    df = df.dropna()

    features = ["Year", "Month", "Category", "Sub-Category", "Region"]

    X = df[features]
    y = df["Sales"]

    split = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    # TUNED RANDOM FOREST (reduces spikes)
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # tuning -

    preds = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(y_test, preds),
        "R2": r2_score(y_test, preds)
    }

    return model, preds, y_test, metrics
