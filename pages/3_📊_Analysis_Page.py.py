import streamlit as st
from utils.charts import (
    create_rating_chart, 
    create_price_chart, 
    create_brand_chart, 
    create_category_rating_chart, 
    create_repurchase_analysis
)
from config.constants import PRODUCT_CATEGORIES

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Data - Sociolla Skincare",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Judul halaman
st.title("📊 Analisis Data Skincare")
st.write("Lihat insight dan tren dari data produk skincare")

# Cek apakah data tersedia di session state
if 'data' not in st.session_state:
    st.error("Data belum dimuat. Silakan kembali ke halaman utama.")
    st.stop()

# Dapatkan data dari session state
data = st.session_state.data

# Sidebar - Informasi kategori
with st.sidebar:
    st.title("Panduan Kategori Produk")
    for category, info in PRODUCT_CATEGORIES.items():
        with st.expander(f"{info['icon']} {category}"):
            st.write(f"**Deskripsi:** {info['description']}")
            st.write("**Manfaat:**")
            for benefit in info['benefits']:
                st.write(f"- {benefit}")

# Opsi untuk menampilkan grafik
analysis_options = [
    "Rating Analysis", 
    "Price Analysis", 
    "Brand Analysis", 
    "Category Analysis", 
    "Repurchase Analysis"
]

selected_analyses = st.multiselect(
    "Pilih Analisis yang Ingin Ditampilkan",
    options=analysis_options,
    default=["Rating Analysis"]
)

# Tampilkan grafik sesuai pilihan
if "Rating Analysis" in selected_analyses:
    with st.container():
        st.write("### 📈 Distribusi Rating Produk")
        fig_rating = create_rating_chart(data)
        st.plotly_chart(fig_rating, use_container_width=True)

if "Price Analysis" in selected_analyses:
    with st.container():
        st.write("### 💰 Distribusi Harga per Kategori")
        fig_price = create_price_chart(data)
        st.plotly_chart(fig_price, use_container_width=True)

if "Brand Analysis" in selected_analyses:
    with st.container():
        st.write("### 🏢 Analisis Brand Terpopuler")
        fig_brand = create_brand_chart(data)
        st.plotly_chart(fig_brand, use_container_width=True)

if "Category Analysis" in selected_analyses:
    with st.container():
        st.write("### 🧴 Analisis Rating per Kategori")
        fig_category = create_category_rating_chart(data)
        st.plotly_chart(fig_category, use_container_width=True)

if "Repurchase Analysis" in selected_analyses:
    with st.container():
        st.write("### 🔄 Analisis Pembelian Ulang")
        fig_repurchase = create_repurchase_analysis(data)
        if fig_repurchase:  # Check if the figure was created successfully
            st.plotly_chart(fig_repurchase, use_container_width=True)
        else:
            st.warning("Data repurchase tidak cukup untuk membuat analisis")

# Tambahkan penjelasan insight
with st.expander("🔍 Insight dari Analisis Data"):
    st.write("""
    ### Insight Utama dari Data Skincare
    
    1. **Rating dan Harga**
       - Produk dengan rating tertinggi cenderung berada di kisaran harga menengah
       - Produk termahal tidak selalu memiliki rating tertinggi
    
    2. **Kategori dan Popularitas**
       - Beberapa kategori seperti Sunscreen dan Moisturizer memiliki tingkat repurchase yang lebih tinggi
       - Kategori Treatment memiliki rentang harga yang paling luas
    
    3. **Brand Performance**
       - Brand dengan jumlah review terbanyak tidak selalu memiliki rating tertinggi
       - Beberapa brand lokal menunjukkan performa yang baik dibandingkan brand internasional
    
    4. **Pembelian Ulang**
       - Produk dengan rating di atas 4.5 memiliki tingkat pembelian ulang yang jauh lebih tinggi
       - Tingkat pembelian ulang menurun drastis untuk produk dengan rating di bawah 3.5
    """)