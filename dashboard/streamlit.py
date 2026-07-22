import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# Set page config for a better layout
st.set_page_config(page_title="E-Commerce Analytics", page_icon="🛍️", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Use relative pathing so it works anywhere
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_dir, "main_data.csv"))
    return df

df = load_data()

st.title('🛍️ E-Commerce Data Analytics Dashboard')
st.markdown("""
Welcome to the E-Commerce Data Analytics Dashboard! This analysis aims to uncover key insights regarding customer satisfaction by answering two primary questions:
1. **How does product data completeness (description length & number of photos) impact customer satisfaction?**
2. **How does delivery time influence customer satisfaction?**
""")

# --- KPI Metrics Row ---
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Reviews Analyzed", f"{len(df):,}")
with col2:
    st.metric("Average Review Score", f"{df['review_score'].mean():.2f} ⭐")
with col3:
    st.metric("Average Delivery Time", f"{df['deliveryTime'].mean():.1f} Days")
with col4:
    st.metric("Avg Product Photos", f"{df['product_photos_qty'].mean():.1f}")

st.divider()

# --- Distribution of Reviews ---
st.header('⭐ Overall Customer Satisfaction (Review Scores)')
st.markdown("A quick look at the distribution of review scores across all orders.")

review_counts = df['review_score'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=review_counts.index, y=review_counts.values, hue=review_counts.index, palette="viridis", legend=False, ax=ax)
ax.set_xlabel('Review Score', fontsize=12)
ax.set_ylabel('Number of Reviews', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

st.divider()

# --- Question 1 Analysis ---
st.header('📦 Impact of Product Data Completeness on Ratings')
st.markdown("Does writing a longer product description or adding more photos lead to happier customers?")

col_q1_a, col_q1_b = st.columns(2)

with col_q1_a:
    st.subheader("Description Length vs. Rating")
    fig, ax = plt.subplots(figsize=(8, 5))
    hb = ax.hist2d(
        df['product_description_length'], 
        df['review_score'], 
        bins=30, 
        cmap='Blues'
    )
    cb = plt.colorbar(hb[3], ax=ax)
    cb.set_label('Concentration of Reviews')
    ax.set_xlabel('Product Description Length (Characters)')
    ax.set_ylabel('Review Score')
    st.pyplot(fig)

with col_q1_b:
    st.subheader("Number of Photos vs. Rating")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x='product_photos_qty', y='review_score', hue='review_score', palette='Set3', legend=False, ax=ax)
    ax.set_xlabel('Number of Photos')
    ax.set_ylabel('Review Score')
    st.pyplot(fig)

st.info("💡 **Insight:** Highly-rated products (5-stars) typically feature descriptions around **500 characters** and utilize **2 to 8 photos**. More isn't always better; having a concise description and a reasonable amount of photos is the sweet spot.")

st.divider()

# --- Question 2 Analysis ---
st.header('🚚 Delivery Time and Customer Satisfaction')
st.markdown("How does the time it takes to deliver an order affect the customer's final rating?")

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist2d(
    df['deliveryTime'], 
    df['review_score'], 
    bins=[30, 5], 
    cmap='Oranges'
)
cbar = plt.colorbar(ax.collections[0], ax=ax)
cbar.set_label('Concentration of Reviews')
ax.set_xlabel('Delivery Time (Days)')
ax.set_ylabel('Review Score')
ax.set_yticks(range(1, 6))
st.pyplot(fig)

st.info("💡 **Insight:** There is a clear correlation between faster deliveries and higher ratings. Orders delivered in **under 25 days** have a significantly higher chance of receiving a 5-star rating.")

st.divider()

# --- Conclusion ---
st.header('🎯 Final Conclusions')
st.success("""
- **Product Presentation Matters, but Balance is Key:** Good product quality doesn't necessarily require excessively long descriptions or dozens of photos. An optimal presentation (around 500 characters and 2-8 photos) correlates strongly with high customer satisfaction.
- **Speed is Crucial for Satisfaction:** While not the *only* factor, delivery time heavily impacts the review score. Keeping delivery times under 25 days is critical for maximizing 5-star reviews.
""")

st.caption('© 2024 Darren Cahya Wijaya | Data Analytics Project')