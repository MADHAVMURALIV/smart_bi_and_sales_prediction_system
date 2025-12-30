import pandas as pd
from prophet import Prophet

def train_prophet(df, periods=6):
    # Aggregate monthly sales
    ts = df.groupby("Date")["Sales"].sum().reset_index()
    ts.columns = ["ds", "y"]

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(ts)

    future = model.make_future_dataframe(periods=periods, freq="M")
    forecast = model.predict(future)

    result = forecast[["ds", "yhat"]].tail(periods)

    return result
