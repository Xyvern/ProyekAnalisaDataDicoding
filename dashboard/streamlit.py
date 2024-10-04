import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Notebook code
dfOrderItems = pd.read_csv("data/order_items_dataset.csv", delimiter=",")
dfOrderReviews = pd.read_csv("data/order_reviews_dataset.csv", delimiter=",")
dfOrders = pd.read_csv("data/orders_dataset.csv", delimiter=",")
dfProducts = pd.read_csv("data/products_dataset.csv", delimiter=",")

dfProducts.rename(columns={
    'product_name_lenght': 'product_name_length',
    'product_description_lenght': 'product_description_length'
}, inplace=True)
dfOrderItems["shipping_limit_date"] = pd.to_datetime(dfOrderItems["shipping_limit_date"])
dfOrderReviews["review_creation_date"] = pd.to_datetime(dfOrderReviews["review_creation_date"])
dfOrderReviews["review_answer_timestamp"] = pd.to_datetime(dfOrderReviews["review_answer_timestamp"])
dfOrders["order_purchase_timestamp"] = pd.to_datetime(dfOrders["order_purchase_timestamp"])
dfOrders["order_approved_at"] = pd.to_datetime(dfOrders["order_approved_at"])
dfOrders["order_delivered_carrier_date"] = pd.to_datetime(dfOrders["order_delivered_carrier_date"])
dfOrders["order_delivered_customer_date"] = pd.to_datetime(dfOrders["order_delivered_customer_date"])
dfOrders["order_estimated_delivery_date"] = pd.to_datetime(dfOrders["order_estimated_delivery_date"])
dfProducts["product_name_length"] = dfProducts["product_name_length"].fillna(0).astype(int)
dfProducts["product_description_length"] = dfProducts["product_description_length"].fillna(0).astype(int)
dfProducts["product_photos_qty"] = dfProducts["product_photos_qty"].fillna(0).astype(int)
dfOrders.dropna(subset=['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date'], inplace=True)
dfOrderReviews['review_comment_title'].fillna('No Title', inplace=True)
dfOrderReviews['review_comment_message'].fillna('No Comment', inplace=True)
dfProducts['product_category_name'].fillna('No Name', inplace=True)
dfProducts['product_weight_g'].fillna(dfProducts['product_weight_g'].mean(), inplace=True)
dfProducts['product_length_cm'].fillna(dfProducts['product_length_cm'].mean(), inplace=True)
dfProducts['product_height_cm'].fillna(dfProducts['product_height_cm'].mean(), inplace=True)
dfProducts['product_width_cm'].fillna(dfProducts['product_width_cm'].mean(), inplace=True)

dfMergedOrderandProductsandReviews = pd.merge(dfOrderItems, dfProducts, how='inner', on='product_id')
dfMergedOrderandProductsandReviews = pd.merge(dfMergedOrderandProductsandReviews, dfOrderReviews, how='inner', on='order_id')
deliveryTime = dfOrders["order_delivered_customer_date"] - dfOrders["order_approved_at"]
deliveryTime = deliveryTime.apply(lambda x: x.total_seconds())
dfOrders["deliveryTime"] = round(deliveryTime / 86400)
dfMergedOrderandReviews = dfOrders.merge(dfOrderReviews, on='order_id', how='left')
dfMergedOrderandReviews = dfMergedOrderandReviews[(dfMergedOrderandReviews['deliveryTime'] >= 0) & (dfMergedOrderandReviews['deliveryTime'] <= 50)]
dfMergedOrderandReviews = dfMergedOrderandReviews.dropna(subset=['deliveryTime', 'review_score'])
# -------------


st.title('Analisis Data: E-Commerce')
st.markdown(
    """
    Analisa ini bertujuan untuk menjawab: 
    - Analisa hubungan antara kelengkapan data produk dengan kepuasan pelanggan
    - Analisa hubungan waktu pengiriman dengan kepuasan pelanggan
    """
)
st.header('Persebaran Rating secara keseluruhan')
# Grafik keseluruhan
review_counts = dfOrderReviews['review_score'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(review_counts.index, review_counts.values, color='blue', alpha=0.7)
ax.set_xlabel('Review Score')
ax.set_ylabel('Number of Reviews')
st.pyplot(fig)

st.header('Persebaran Rating dengan pengaruh kelengkapan deskripsi produk dan jumlah foto')
st.subheader("Persebaran Rating vs Kelengkapan Deskripsi")
# Grafik Rating vs Kelengkapan Deskripsi
fig, ax = plt.subplots(figsize=(10, 6))
hb = ax.hist2d(
    dfMergedOrderandProductsandReviews['product_description_length'], 
    dfMergedOrderandProductsandReviews['review_score'], 
    bins=50, 
    cmap='Blues'
)
cb = plt.colorbar(hb[3], ax=ax)
cb.set_label('Count')
ax.set_xlabel('Product Description Length')
ax.set_ylabel('Review Score')
st.pyplot(fig)

st.subheader("Persebaran Rating vs Jumlah foto produk")

# Grafik Rating vs Jumlah foto produk
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=dfMergedOrderandProductsandReviews, x='product_photos_qty', y='review_score', ax=ax)
ax.set_title('Product Photos vs Review Score')
ax.set_xlabel('Number of Photos')
ax.set_ylabel('Review Score')
st.pyplot(fig)

st.header('Persebaran Rating dengan pengaruh lama waktu pengiriman')

fig, ax = plt.subplots(figsize=(10, 6))
hist, xedges, yedges = np.histogram2d(
    dfMergedOrderandReviews['deliveryTime'], 
    dfMergedOrderandReviews['review_score'], 
    bins=50
)
xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing="ij")
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = hist.ravel()
ax.hist2d(
    dfMergedOrderandReviews['deliveryTime'], 
    dfMergedOrderandReviews['review_score'], 
    bins=50, 
    cmap='Blues'
)
cbar = plt.colorbar(ax.collections[0], ax=ax)
cbar.set_label('Count')
ax.set_xlabel('Delivery Time in days')
ax.set_ylabel('Review Score')
st.pyplot(fig)


st.markdown("""- Deskripsi produk yang memiliki rating bagus terkonsentrasi pada angka sekitar 500 huruf
- Jumlah foto produk yang memiliki rating bagus berada pada angka 2 - 8
- Waktu pengantaran barang dibawah 25 hari memiliki peluang yang lebih besar untuk mendapat rating 5 dari pelanggan"""
)

st.header('Kesimpulan')
st.markdown("""
- Berdasarkan hasil analisa saya meyimpulkan bahwa kualitas barang yang baik tidak selalu memiliki deskripsi yang panjang dan jumlah foto yang banyak tetapi memiliki jumlah yang ideal yaitu tidak lebih dari 500 huruf untuk deskripsi dan 2-8 foto. Kepuasan pelanggan memiliki korelasi dengan kualitas barang, semakin berkualitas barangnya semakin bagus rating yang diberikan.
- Berdasarkan hasil analisa saya meyimpulkan bahwa lama waktu pengantaran bukan satu-satunya faktor kepuasann pelanggan, tetapi waktu pengantaran dibawah 25 hari memiliki peluang yang lebih besar untuk mendapatkan rating 5. Kepuasan pelanggan memiliki korelasi dengan waktu pengantaran."""
)

st.caption('Copyright (c) 2024 Darren Cahya Wijaya')