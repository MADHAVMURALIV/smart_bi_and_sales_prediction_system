import pandas as pd

DATA_PATH = r"D:\smart-bi-sales-prediction\data\sales.csv"   
OUTPUT_PATH = r"D:\smart-bi-sales-prediction\data\new_sales.csv"

df = pd.read_csv(DATA_PATH)
print(df.head())  #sample display
# column selection 
df = df[["Order Date","Sales","Category","Sub-Category","Region"]]
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True,
    errors="coerce"
)


df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month

#Original Date drop 
df.drop(columns=["Order Date"], inplace=True)

# Missing Values 
df.dropna(inplace=True)
monthly_df = (
    df.groupby(["Year", "Month", "Category", "Sub-Category", "Region"])
      .agg({
          "Sales": "sum"
      })
      .reset_index()
)

#Processed Data
monthly_df.to_csv(OUTPUT_PATH, index=False)

print("Preprocessing completed. File saved as processed_sales.csv")
