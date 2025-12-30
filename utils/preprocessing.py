import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess(csv_path):
    df = pd.read_csv(csv_path)

    required_cols = ["Year", "Month", "Category", "Sub-Category", "Region", "Sales"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df["Date"] = pd.to_datetime(
        df["Year"].astype(str) + "-" +
        df["Month"].astype(str) + "-01"
    )

    df = df.sort_values("Date").reset_index(drop=True)
    df = df.dropna(subset=["Sales"])

    encoders = {}
    meta = {
        "categories": [],
        "regions": []
    }

    # Category
    le_cat = LabelEncoder()
    df["Category"] = le_cat.fit_transform(df["Category"].astype(str))
    encoders["Category"] = le_cat
    meta["categories"] = le_cat.classes_.tolist()

    # Sub-Category
    le_sub = LabelEncoder()
    df["Sub-Category"] = le_sub.fit_transform(df["Sub-Category"].astype(str))
    encoders["Sub-Category"] = le_sub

    # Region
    le_reg = LabelEncoder()
    df["Region"] = le_reg.fit_transform(df["Region"].astype(str))
    encoders["Region"] = le_reg
    meta["regions"] = le_reg.classes_.tolist()

    return df, encoders, meta
