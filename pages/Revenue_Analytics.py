import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Load Data ----
df = pd.read_csv(r"E:\Streamlit\Project2\Data_cleaned.csv")
df['revenue'] = df['subtotal_inr'] + df['delivery_charges']

st.title("📊 Business Performance Analysis Dashboard")

# ---------------- Question 6 ----------------
st.header("Revenue Growth Analysis")

rev_by_month = df.groupby('order_month')['revenue'].sum().reset_index().sort_values("order_month")

st.subheader("📈 Month-over-Month Revenue Trend")
fig1 = px.line(
    rev_by_month, x='order_month', y='revenue',
    markers=True, title="Monthly Revenue Trend"
)
st.plotly_chart(fig1, use_container_width=True)

#st.subheader("📊 Growth Rate by Subcategory")
#fig2 = px.bar(
 #   df, x='subcategory', y='revenue',
  #  title="Revenue by Subcategory", text_auto=True
#)
#st.plotly_chart(fig2, use_container_width=True)

# ---------------- Question 8 ----------------
st.header("Tier-based Revenue Performance")

tier_df = df.groupby("customer_tier")["revenue"].sum().reset_index()

fig3 = px.bar(
    tier_df, x='customer_tier', y='revenue',
    text='revenue', title="Revenue by Customer Tier"
)
fig3.update_traces(textposition="outside")
st.plotly_chart(fig3, use_container_width=True)

# ---------------- Question 9 ----------------
st.header("Festival Sale Analytics")

st.subheader("🧭 Festival Sale — Revenue Contribution")
fig4 = px.pie(
    df, values='revenue', names='is_festival_sale',
    hole=0.35, title="Festival Sale vs Non-Festival Sale Revenue Share"
)
fig4.update_traces(textinfo='percent+label')
st.plotly_chart(fig4, use_container_width=True)

st.subheader("🧭 Festival Revenue Comparison")
festival_df = df.groupby('is_festival_sale')['revenue'].sum().reset_index()

fig5 = px.bar(
    festival_df, x='is_festival_sale', y='revenue',
    text='revenue', title="Festival vs Non-Festival Revenue"
)
fig5.update_traces(textposition='outside')
st.plotly_chart(fig5, use_container_width=True)

# ---------------- Question 10 ----------------
st.header("Price Optimization Dashboard")

st.subheader("🔍 Correlation Heatmap — Pricing & Discounts")
cc = df[['original_price_inr', 'discount_percent', 'discounted_price_inr',
         'delivery_charges', 'final_amount_inr']].corr()

fig6 = px.imshow(
    cc, text_auto=True, color_continuous_scale="Blues",
    title="Correlation Matrix — Price vs Discount Factors"
)
st.plotly_chart(fig6, use_container_width=True)
