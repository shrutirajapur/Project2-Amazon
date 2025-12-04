import streamlit as st
import pandas as pd
import plotly.express as px
st.title("🛒 Amazon India: A Decade of Sales Analytics 📈🇮🇳")

df = pd.read_csv(r"E:\Streamlit\Project2\Data_cleaned.csv")
df["profit"] = df["discounted_price_inr"] - df["original_price_inr"]   # or whichever formula you use
df["profit"] = df["profit"].fillna(0)

# ---------------- KPI Calculations ----------------
df['order_date'] = pd.to_datetime(df['order_date'])
df['year'] = df['order_date'].dt.year
df['revenue'] = df['subtotal_inr'] + df['delivery_charges']

total_revenue = df['revenue'].sum()
active_customers = df['customer_id'].nunique()
average_order_value = total_revenue / df['transaction_id'].nunique()

rev_by_year = df.groupby('year')['revenue'].sum()

growth_rate = (
    (rev_by_year.iloc[-1] - rev_by_year.iloc[-2]) / rev_by_year.iloc[-2] * 100
    if len(rev_by_year) > 1
    else 0
)

top_categories = df.groupby('brand')['revenue'].sum().sort_values(ascending=False).head(5)

# ---------------- Dashboard Header ----------------
st.title("📌 Executive Summary Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
col2.metric("YoY Growth", f"{growth_rate:.2f}%")
col3.metric("Active Customers", f"{active_customers:,}")
col4.metric("Avg Order Value", f"₹ {average_order_value:,.0f}")

# ---------------- YoY Revenue ----------------
st.subheader("📈 Year-over-Year Revenue Trend")
fig_rev = px.line(rev_by_year, markers=True)
st.plotly_chart(fig_rev, use_container_width=True)

# ---------------- Top 5 Categories ----------------
st.subheader("🏆 Top Performing Categories")
fig_top = px.bar(top_categories, text_auto=True)
st.plotly_chart(fig_top, use_container_width=True)

# ---------------- Q2 - Revenue vs Target ----------------
st.subheader("📈 Revenue Trend vs Target")
df['order_month'] = df['order_date'].dt.month
df_trend = df.groupby(['year', 'order_month'])['revenue'].sum().reset_index()
fig_trend = px.line(df_trend, x='order_month', y='revenue', color='year', markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------- Profit Margin ----------------
st.subheader("📌 Profit Margin by Category")
profit_margin_df = df.groupby('subcategory').apply(
    lambda x: (x['profit'].sum() / x['revenue'].sum()) * 100
).reset_index(name='profit_margin')

fig_profit = px.bar(
    profit_margin_df,
    x='subcategory',
    y='profit_margin',
    text='profit_margin',
    title="Profit Margin by Subcategory"
)

fig_profit.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_profit.update_layout(yaxis_title="Profit Margin (%)")
st.plotly_chart(fig_profit, use_container_width=True)



# ---------------- Cost Structure Allocation ----------------
st.subheader("📌 Cost Structure Allocation")
cost_str = df.groupby('subcategory')['original_price_inr'].sum().reset_index()
fig_cost = px.pie(cost_str, names='subcategory', values='original_price_inr', hole=0.4)
st.plotly_chart(fig_cost, use_container_width=True)

# ---------------- Market Share ----------------
st.subheader("📌 Market Share by SubCategory")
market_df = df.groupby('subcategory')['transaction_id'].count().reset_index()
market_df.columns = ['subcategory', 'orders']
fig_market = px.pie(market_df, names='category', values='orders')
st.plotly_chart(fig_market, use_container_width=True)

# ---------------- Competitive Positioning ----------------
st.subheader("📌 Competitive Positioning Matrix")
fig_compete = px.scatter(
    df,
    x="product_rating",
    y="revenue",
    size="quantity",
    color="brand",
    hover_name="product_name",
    title="Product Positioning: Rating vs Revenue"
)
st.plotly_chart(fig_compete, use_container_width=True)
