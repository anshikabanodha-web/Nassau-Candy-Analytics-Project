import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    page_icon="🍫",
    layout="wide"
)

# Title
st.title("🍫 Nassau Candy Distributor")
st.subheader("Product Line Profitability & Margin Performance Analysis")

# Load dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Calculate metrics
df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

# KPI calculations
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
total_units = df["Units"].sum()
overall_margin = (total_profit / total_sales) * 100

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Gross Profit", f"${total_profit:,.2f}")
col3.metric("Gross Margin", f"{overall_margin:.2f}%")
col4.metric("Total Units", f"{total_units:,}")

st.divider()

# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

division_filter = st.sidebar.multiselect(
    "Select Division",
    options=df["Division"].unique(),
    default=df["Division"].unique()
)

filtered_df = df[df["Division"].isin(division_filter)]

st.divider()

# TOP PRODUCTS BY GROSS PROFIT
st.subheader("🏆 Top 10 Products by Gross Profit")

top_products = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.bar(
    top_products.sort_values(ascending=True),
    orientation="h",
    labels={
        "value": "Gross Profit",
        "Product Name": "Product"
    },
    title="Top 10 Products by Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)
# DIVISION PERFORMANCE
st.subheader("📊 Division Performance")

division_analysis = (
    filtered_df.groupby("Division")
    .agg({
        "Sales": "sum",
        "Gross Profit": "sum"
    })
)

division_analysis["Gross Margin %"] = (
    division_analysis["Gross Profit"] /
    division_analysis["Sales"]
) * 100

st.dataframe(
    division_analysis.style.format({
        "Sales": "${:,.2f}",
        "Gross Profit": "${:,.2f}",
        "Gross Margin %": "{:.2f}%"
    })
)
fig = px.bar(
    division_analysis.reset_index(),
    x="Division",
    y=["Sales", "Gross Profit"],
    barmode="group",
    title="Sales vs Gross Profit by Division"
)

st.plotly_chart(fig, use_container_width=True,
key="division_chart",height=500)

# COST VS SALES DIAGNOSTIC
st.subheader("💰 Cost vs Sales Diagnostic")

cost_analysis = (
    filtered_df.groupby("Product Name")
    .agg({
        "Sales": "sum",
        "Cost": "sum",
        "Gross Profit": "sum"
    })
)

cost_analysis["Gross Margin %"] = (
    cost_analysis["Gross Profit"] /
    cost_analysis["Sales"]
) * 100

cost_analysis["Cost % of Sales"] = (
    cost_analysis["Cost"] /
    cost_analysis["Sales"]
) * 100

st.dataframe(
    cost_analysis.sort_values(
        "Cost % of Sales",
        ascending=False
    ).style.format({
        "Sales": "${:,.2f}",
        "Cost": "${:,.2f}",
        "Gross Profit": "${:,.2f}",
        "Gross Margin %": "{:.2f}%",
        "Cost % of Sales": "{:.2f}%"
    })
)# MARGIN RISK PRODUCTS
st.subheader("⚠️ Margin Risk Products")

sales_median = filtered_df.groupby("Product Name")["Sales"].sum().median()

risk_products = (
    filtered_df.groupby("Product Name")
    .agg({
        "Sales": "sum",
        "Gross Profit": "sum",
        "Cost": "sum"
    })
)

risk_products["Gross Margin %"] = (
    risk_products["Gross Profit"] /
    risk_products["Sales"]
) * 100

risk_products["Profit per Unit"] = (
    risk_products["Gross Profit"] /
    filtered_df.groupby("Product Name")["Units"].sum()
)

risk_products = risk_products[
    (risk_products["Sales"] >= sales_median) &
    (risk_products["Gross Margin %"] < 50)
].sort_values("Sales", ascending=False)

st.dataframe(
    risk_products.style.format({
        "Sales": "${:,.2f}",
        "Gross Profit": "${:,.2f}",
        "Cost": "${:,.2f}",
        "Gross Margin %": "{:.2f}%",
        "Profit per Unit": "${:,.2f}"
    })
)# PROFIT CONCENTRATION / PARETO ANALYSIS
st.subheader("📈 Profit Concentration Analysis")

profit_by_product = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
)

total_profit_pareto = profit_by_product.sum()

pareto_df = profit_by_product.reset_index()
pareto_df.columns = ["Product Name", "Gross Profit"]

pareto_df["Cumulative Profit %"] = (
    pareto_df["Gross Profit"].cumsum() /
    total_profit_pareto
) * 100

st.dataframe(
    pareto_df.style.format({
        "Gross Profit": "${:,.2f}",
        "Cumulative Profit %": "{:.2f}%"
    })
)

st.line_chart(
    pareto_df.set_index("Product Name")["Cumulative Profit %"]
)