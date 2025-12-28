import pandas as pd

def monthly_demand_forecast(csv_path, months=6):
    df = pd.read_csv(csv_path)

    monthly_sales = (
        df.groupby(["Year", "Month"])["Sales"]
        .sum()
        .reset_index()
    )

    avg_demand = monthly_sales["Sales"].mean()

    last_year = monthly_sales.iloc[-1]["Year"]
    last_month = monthly_sales.iloc[-1]["Month"]

    forecast = []
    for i in range(1, months + 1):
        m = last_month + i
        y = last_year + (m - 1) // 12
        m = ((m - 1) % 12) + 1

        forecast.append({
            "month": f"{int(y)}-{int(m):02d}",
            "expected_demand": round(avg_demand, 2)
        })

    return forecast
