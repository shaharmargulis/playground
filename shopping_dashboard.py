import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('shopping_behavior_updated.csv')

df = load_data()

# Title
st.title("Shopping Behavior Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("Filters")

# Gender filter
gender = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())

# Category filter
category = st.sidebar.multiselect("Category", options=df['Category'].unique(), default=df['Category'].unique())

# Season filter
season = st.sidebar.multiselect("Season", options=df['Season'].unique(), default=df['Season'].unique())

# Age range
age_min, age_max = st.sidebar.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))

# Purchase amount range
amount_min, amount_max = st.sidebar.slider("Purchase Amount ($)", int(df['Purchase Amount (USD)'].min()), int(df['Purchase Amount (USD)'].max()), (int(df['Purchase Amount (USD)'].min()), int(df['Purchase Amount (USD)'].max())))

# Apply filters
filtered_df = df[
    (df['Gender'].isin(gender)) &
    (df['Category'].isin(category)) &
    (df['Season'].isin(season)) &
    (df['Age'] >= age_min) &
    (df['Age'] <= age_max) &
    (df['Purchase Amount (USD)'] >= amount_min) &
    (df['Purchase Amount (USD)'] <= amount_max)
]

# Main content
st.header(f"Data Overview ({len(filtered_df)} records)")

# Key metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", len(filtered_df))
col2.metric("Avg Purchase", f"${filtered_df['Purchase Amount (USD)'].mean():.2f}")
col3.metric("Total Revenue", f"${filtered_df['Purchase Amount (USD)'].sum():,.0f}")
col4.metric("Avg Rating", f"{filtered_df['Review Rating'].mean():.2f}")

st.markdown("---")

# Aggregation section
st.header("Data Aggregation")

col1, col2 = st.columns(2)

with col1:
    group_by = st.selectbox("Group By", ["Category", "Gender", "Season", "Location", "Item Purchased", "Payment Method", "Shipping Type", "Frequency of Purchases"])

with col2:
    agg_metric = st.selectbox("Metric", ["Purchase Amount (USD)", "Review Rating", "Previous Purchases", "Age"])

agg_function = st.radio("Aggregation Function", ["Sum", "Mean", "Median", "Count", "Min", "Max"], horizontal=True)

# Perform aggregation
if agg_function == "Sum":
    agg_data = filtered_df.groupby(group_by)[agg_metric].sum().reset_index().sort_values(agg_metric, ascending=False)
elif agg_function == "Mean":
    agg_data = filtered_df.groupby(group_by)[agg_metric].mean().reset_index().sort_values(agg_metric, ascending=False)
elif agg_function == "Median":
    agg_data = filtered_df.groupby(group_by)[agg_metric].median().reset_index().sort_values(agg_metric, ascending=False)
elif agg_function == "Count":
    agg_data = filtered_df.groupby(group_by)[agg_metric].count().reset_index().sort_values(agg_metric, ascending=False)
elif agg_function == "Min":
    agg_data = filtered_df.groupby(group_by)[agg_metric].min().reset_index().sort_values(agg_metric, ascending=False)
else:  # Max
    agg_data = filtered_df.groupby(group_by)[agg_metric].max().reset_index().sort_values(agg_metric, ascending=False)

# Display chart
fig = px.bar(agg_data, x=group_by, y=agg_metric, title=f"{agg_function} of {agg_metric} by {group_by}")
st.plotly_chart(fig, use_container_width=True)

# Display table
st.dataframe(agg_data, use_container_width=True)

st.markdown("---")

# Distribution charts
st.header("Distributions")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Purchase Amount Distribution")
    fig1 = px.histogram(filtered_df, x="Purchase Amount (USD)", nbins=30)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Age Distribution")
    fig2 = px.histogram(filtered_df, x="Age", nbins=30)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Category breakdown
st.header("Category Breakdown")
category_data = filtered_df['Category'].value_counts()
fig3 = px.pie(values=category_data.values, names=category_data.index, title="Purchases by Category")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df, use_container_width=True)
