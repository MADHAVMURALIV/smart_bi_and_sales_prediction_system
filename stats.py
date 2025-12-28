import pandas as pd

def get_stats(csv_path):
    df = pd.read_csv(csv_path)

    total_sales = df["Sales"].sum()
    avg_monthly_sales = df.groupby(["Year", "Month"])["Sales"].sum().mean()

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .to_dict(orient="records")
    )

    monthly_trend = (
        df.groupby(["Year", "Month"])["Sales"]
        .sum()
        .reset_index()
        .to_dict(orient="records")
    )

    return {
        "total_sales": round(total_sales, 2),
        "avg_monthly_sales": round(avg_monthly_sales, 2),
        "category_sales": category_sales,
        "monthly_sales_trend": monthly_trend
    }
