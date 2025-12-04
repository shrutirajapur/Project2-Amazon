import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

# Load data
df = pd.read_csv(r"E:\Streamlit\Project2\Data_cleaned.csv")
df['revenue'] = df['subtotal_inr'].fillna(0) + df['delivery_charges'].fillna(0)
df["profit"] = df["discounted_price_inr"] - df["original_price_inr"]   # or whichever formula you use
df["profit"] = df["profit"].fillna(0)
df['quantity'] = df['quantity'].fillna(0)

# Database connection (optional)
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="Amazon",
    user="postgres",
    password="Direction@12"
)
cur = conn.cursor()

# ---------------------------------------------------------
# QUESTION 16
# ---------------------------------------------------------
st.subheader("⭐ Top Product Performance")
fig = px.bar(
    df.groupby('subcategory')['revenue'].sum().reset_index(),
    x='subcategory',
    y='revenue',
    title='Top Product Performance by Subcategory',
    text_auto=True
)
fig.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig, use_container_width=True)

st.subheader("⭐ Top Product Performance (Scatter)")
fig = px.scatter(
    df,
    x='subcategory',
    y='revenue',
    size='revenue',
    color='subcategory',
    hover_name='product_name',
    title='Revenue Distribution Across Subcategories'
)
fig.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig, use_container_width=True)

# Rating vs Return
st.subheader("⭐ Rating vs Return Rate")
fig = px.scatter(
    df,
    x="product_rating",
    y="return_status",
    #size="revenue",
    color="subcategory",
    hover_name="product_name",
    title="Rating vs Return Rate"
)
st.plotly_chart(fig, use_container_width=True)

# Top Rated Products
st.subheader("⭐ Average Rating by Subcategory")
fig3 = px.bar(
    df.groupby('subcategory')['product_rating'].mean().reset_index(),
    x='subcategory',
    y='product_rating',
    title="Top Rated Subcategories"
)
fig3.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------
# QUESTION 17
# ---------------------------------------------------------

st.subheader("🏷 Brand Performance (Revenue Share)")
fig = px.pie(
    df.groupby('brand')['revenue'].sum().reset_index(),
    values='revenue',
    names='brand',
    hole=0.3,
    title='Revenue Contribution by Brand'
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📦 Units Sold per Brand")
fig = px.bar(
    df.groupby('brand')['quantity'].sum().reset_index(),
    x='brand', y='quantity',
    title="Quantity Sold by Brand"
)
fig.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig, use_container_width=True)

#st.subheader("⏱ Operational Efficiency")
#fig = px.bar(
 #   df,
  #  x='delivery_days',
   # y='product_rating',
    #title="Delivery Days vs Product Rating"
#)
#st.plotly_chart(fig, use_container_width=True)

st.subheader("💳 Payment Analytics")
fig = px.bar(
    df.groupby('payment_method')['revenue'].sum().reset_index(),
    x='payment_method', y='revenue',
    title="Payment Method Impact on Revenue"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("♻️ Return Rate by Category")
df['return_status'] = df['return_status'].map({'Returned': 1, 'Not Returned': 0})
df['return_status'] = df['return_status'].fillna(0) 
return_rate = df.groupby('subcategory')['return_status'].mean().reset_index()
fig = px.bar(
    df.groupby('subcategory')['return_status'].mean().reset_index(),
    x='subcategory', y='return_status',
    title="Return Rate per Subcategory"
)
fig.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🚚 Supply Chain Performance")
fig = px.scatter(
    df,
    x='delivery_days', y='revenue',
    size='quantity',
    color='subcategory',
    title="Delivery Time vs Revenue"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("👑 Prime vs Non-Prime Revenue Behavior")
fig = px.box(
    df,
    x="is_prime_member",
    y="revenue",
    color="is_prime_member",
    title="Prime Members Drive More Revenue?"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🧑‍🤝‍🧑 Age Group Purchase Preference")
fig = px.bar(
    df.groupby('customer_age_group')['revenue'].sum().reset_index(),
    x='customer_age_group', y='revenue',
    title="Revenue by Age Group"
)
st.plotly_chart(fig, use_container_width=True)
