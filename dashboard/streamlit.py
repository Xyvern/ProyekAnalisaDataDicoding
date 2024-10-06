import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Importing csv to dataframe
dfMergedOrderandProductsandReviews = pd.read_csv("dashboard/MergedOrderandProductsandReviews.csv", delimiter=",")
dfOrderReviews = pd.read_csv("dashboard/OrderReviews.csv", delimiter=",")
dfMergedOrderandReviews = pd.read_csv("dashboard/MergedOrderandReviews.csv", delimiter=",")
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