import pandas as pd
def generate_future_data(df, months=6):
    last_year = df["Year"].iloc[-1]
    last_month = df["Month"].iloc[-1]

    future_rows = []

    for i in range(1, months + 1):
        month = last_month + i
        year = last_year

        if month > 12:
            month -= 12
            year += 1

        future_rows.append({
            "Year": year,
            "Month": month,
            "Category": df["Category"].mode()[0],
            "Sub-Category": df["Sub-Category"].mode()[0],
            "Region": df["Region"].mode()[0]
        })

    return pd.DataFrame(future_rows)
