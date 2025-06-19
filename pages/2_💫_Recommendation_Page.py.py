import streamlit as st
import pandas as pd
from utils.display import display_product_card
from utils.recommender import get_ml_recommendations
from utils.user_preferences import rank_by_preferences
from config.constants import PRODUCT_CATEGORIES

# Konfigurasi halaman
st.set_page_config(
    page_title="Rekomendasi Produk - Sociolla Skincare",
    page_icon="💫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Judul halaman
st.title("💫 Rekomendasi Produk Skincare")
st.write("Temukan rekomendasi produk yang serupa dengan produk favorit Anda")

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
    
    # Tambahkan informasi tentang sistem rekomendasi
    st.sidebar.markdown("---")
    st.sidebar.write("### 🧠 Tentang Sistem Rekomendasi")
    st.sidebar.info("""
    Sistem rekomendasi kami menggunakan pendekatan hybrid yang menggabungkan:
    
    1. **Content-Based Filtering** - Menganalisis fitur dan karakteristik produk
    
    2. **Similarity-Based Filtering** - Menganalisis rating dan jumlah review produk
    
    Kombinasi ini memberikan rekomendasi yang lebih relevan dan personal.
    """)

# Tampilkan preferensi pengguna jika ada
if 'user_preferences' in st.session_state and st.session_state.user_preferences:
    preferences = st.session_state.user_preferences
    
    st.info("🧬 Rekomendasi akan dipersonalisasi berdasarkan preferensi Anda:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        skin_type = preferences.get("skin_type")
        if skin_type:
            st.write(f"**Jenis Kulit:** {skin_type}")
        else:
            st.write("**Jenis Kulit:** Tidak dipilih")
    
    with col2:
        concerns = preferences.get("skin_concerns", [])
        if concerns:
            st.write(f"**Permasalahan Kulit:** {', '.join(concerns)}")
        else:
            st.write("**Permasalahan Kulit:** Tidak dipilih")

# Tampilkan empat elemen dalam satu baris dengan `st.columns`
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    # Pilih kategori produk
    selected_category = st.selectbox(
        "Pilih Kategori Produk",
        options=sorted(data['category'].unique())
    )

with col2:
    # Pilih brand produk
    category_data = data[data['category'] == selected_category]
    available_brands = sorted(category_data['brand'].unique())
    selected_brand = st.selectbox(
        "Pilih Brand",
        options=available_brands
    )

with col3:
    # Pilih produk dari brand tersebut
    brand_products = category_data[category_data['brand'] == selected_brand]
    selected_product = st.selectbox(
        "Pilih Produk",
        options=sorted(brand_products['product_name'].unique()),
        help=f"Pilih produk {selected_category} dari brand {selected_brand}"
    )

with col4:
    # Jumlah rekomendasi
    n_recommendations = st.slider(
        "Jumlah rekomendasi", 
        min_value=3, 
        max_value=10, 
        value=5
    )

# Tampilkan info produk yang dipilih
selected_product_data = data[data['product_name'] == selected_product].iloc[0]
st.write("### Produk yang Anda Pilih")
display_product_card(selected_product_data)

# Tombol untuk mencari rekomendasi
if st.button("🔍 Cari Rekomendasi Produk Serupa", use_container_width=True):
    with st.spinner(f"Mencari rekomendasi produk {selected_category} yang serupa..."):
        # Gunakan metode hybrid untuk hasil terbaik
        recommendations = get_ml_recommendations(
            selected_product, 
            data, 
            method="hybrid",
            n_recommendations=n_recommendations
        )
        
        # Tambahkan personalisasi berdasarkan preferensi pengguna
        if 'user_preferences' in st.session_state and st.session_state.user_preferences:
            recommendations = rank_by_preferences(
                recommendations, 
                st.session_state.user_preferences
            )
        
        # Tampilkan hasil rekomendasi
        if not recommendations.empty:
            st.success(f"Berikut {len(recommendations)} rekomendasi produk {selected_category} untuk Anda:")
            
            # Tampilkan produk yang direkomendasikan
            for idx, (_, product) in enumerate(recommendations.iterrows(), 1):
                display_product_card(product, idx)
        else:
            st.warning(f"Tidak ditemukan rekomendasi {selected_category} yang sesuai")

# Tambahkan sedikit informasi tentang bagaimana rekomendasi dibuat
with st.expander("ℹ️ Bagaimana Rekomendasi Dibuat?"):
    st.write("""
    ### Proses Rekomendasi Produk
    
    Sistem kami menggunakan pendekatan hybrid dengan 2 komponen utama:
    
    1. **Content-Based Filtering (40% bobot)**
       - Menganalisis kesamaan karakteristik produk seperti kategori dan brand
       - Cocok untuk menemukan produk dengan fitur yang serupa
    
    2. **Similarity-Based Filtering (60% bobot)**
       - Menganalisis rating dan jumlah review produk
       - Memberikan rekomendasi berdasarkan popularitas dan penilaian pengguna
    
    3. **Personalisasi Preferensi (bonus)**
       - Menyesuaikan rekomendasi berdasarkan jenis kulit dan permasalahan kulit Anda
       - Produk yang sesuai dengan preferensi Anda akan mendapat bobot lebih tinggi
    
    Hasil akhir adalah rekomendasi yang menggabungkan kualitas produk (berdasarkan rating) 
    dan relevansi produk (berdasarkan kesamaan fitur), serta mempertimbangkan kebutuhan personal Anda.
    """)