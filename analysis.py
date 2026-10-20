import pandas as pd

df = pd.read_csv("Nassau Candy Distributor.csv")

print("DATASET SHAPE:", df.shape)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nDUPLICATE ROWS:", df.duplicated().sum())
print("\nDATA TYPES:")
print(df.dtypes)

print("\nFIRST 5 ROWS:")
print(df.head())
print("\nNUMERIC SUMMARY:")
print(df[["Sales", "Units", "Gross Profit", "Cost"]].describe())
# PROFITABILITY METRICS

df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100

df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

print("\nPROFITABILITY METRICS:")
print(df[["Product Name", "Sales", "Units", "Gross Profit", "Cost",
          "Gross Margin %", "Profit per Unit"]].head())
          # TOP 10 PRODUCTS BY GROSS PROFIT

top_products = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 PRODUCTS BY GROSS PROFIT:")
print(top_products)
# PRODUCT-LEVEL PROFITABILITY ANALYSIS

product_analysis = (
    df.groupby("Product Name")
    .agg({
        "Sales": "sum",
        "Units": "sum",
        "Gross Profit": "sum",
        "Cost": "sum"
    })
)

product_analysis["Gross Margin %"] = (
    product_analysis["Gross Profit"] / product_analysis["Sales"]
) * 100

product_analysis["Profit per Unit"] = (
    product_analysis["Gross Profit"] / product_analysis["Units"]
)

print("\nPRODUCT-LEVEL PROFITABILITY:")
print(product_analysis.sort_values("Gross Profit", ascending=False).head(10))
# DIVISION-LEVEL PERFORMANCE

division_analysis = (
    df.groupby("Division")
    .agg({
        "Sales": "sum",
        "Units": "sum",
        "Gross Profit": "sum",
        "Cost": "sum"
    })
)

division_analysis["Gross Margin %"] = (
    division_analysis["Gross Profit"] / division_analysis["Sales"]
) * 100

division_analysis["Profit per Unit"] = (
    division_analysis["Gross Profit"] / division_analysis["Units"]
)

print("\nDIVISION-LEVEL PERFORMANCE:")
print(division_analysis.sort_values("Gross Profit", ascending=False))
# PROFIT CONCENTRATION / PARETO ANALYSIS

profit_by_product = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
)

cumulative_profit = profit_by_product.cumsum()
total_profit = profit_by_product.sum()

cumulative_percentage = (cumulative_profit / total_profit) * 100

products_for_80_profit = (cumulative_percentage <= 80).sum()

print("\nTOTAL GROSS PROFIT:", total_profit)

print("\nPROFIT CONCENTRATION:")
print("Products contributing up to 80% of total profit:",
      products_for_80_profit)

print("\nCUMULATIVE PROFIT PERCENTAGE:")
print(cumulative_percentage)
# COST VS SALES DIAGNOSTIC

cost_analysis = (
    df.groupby("Product Name")
    .agg({
        "Sales": "sum",
        "Cost": "sum",
        "Gross Profit": "sum"
    })
)

cost_analysis["Gross Margin %"] = (
    cost_analysis["Gross Profit"] / cost_analysis["Sales"]
) * 100

cost_analysis["Cost % of Sales"] = (
    cost_analysis["Cost"] / cost_analysis["Sales"]
) * 100

print("\nCOST VS SALES DIAGNOSTIC:")
print(
    cost_analysis.sort_values("Cost % of Sales", ascending=False)
)
# HIGH-SALES / LOW-MARGIN PRODUCTS

sales_median = product_analysis["Sales"].median()

risk_products = product_analysis[
    (product_analysis["Sales"] >= sales_median) &
    (product_analysis["Gross Margin %"] < 50)
].sort_values("Sales", ascending=False)

print("\nHIGH-SALES / LOW-MARGIN PRODUCTS:")
print(risk_products)