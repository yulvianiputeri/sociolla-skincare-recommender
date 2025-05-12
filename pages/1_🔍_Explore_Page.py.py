import streamlit as st
import pandas as pd
from utils.display import display_product_card, paginate_dataframe, display_metrics, apply_filters
from utils.user_preferences import filter_by_preferences
from config.constants import PRODUCT_CATEGORIES

# Konfigurasi halaman
st.set_page_config(
    page_title="Jelajahi Produk - Sociolla Skincare",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Judul halaman
st.title("🔍 Jelajahi Produk Skincare")
st.write("Cari dan filter produk skincare sesuai preferensi Anda")

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

# Tampilkan preferensi pengguna jika ada
has_preferences = False
if 'user_preferences' in st.session_state and st.session_state.user_preferences:
    has_preferences = True
    preferences = st.session_state.user_preferences
    
    st.info("🧬 Produk akan difilter berdasarkan preferensi Anda:")
    
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
    
    # Checkbox untuk menggunakan preferensi
    use_preferences = st.checkbox("Gunakan preferensi saya untuk filter", value=True)
    has_preferences = use_preferences

# Filter produk
col1, col2 = st.columns(2)

with col1:
    selected_category = st.selectbox(
        "Pilih Kategori Produk",
        options=['Semua'] + sorted(data['category'].unique().tolist())
    )

with col2:
    available_brands = sorted(data['brand'].unique())
    if selected_category != 'Semua':
        available_brands = sorted(
            data[data['category'] == selected_category]['brand'].unique()
        )
    
    selected_brand = st.selectbox(
        "Pilih Brand",
        options=['Semua'] + available_brands
    )

# Filter harga
st.subheader("💰 Rentang Harga")
min_price = float(data['price'].min()) * 1000
max_price = float(data['price'].max()) * 1000
price_range = st.slider(
    "Pilih rentang harga (Rp)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    step=50000.0,
    format="%d"
)

# Terapkan filter
filtered_data = apply_filters(
    data=data,
    selected_category=selected_category,
    selected_brand=selected_brand,
    price_range=price_range
)

# Terapkan filter preferensi jika ada
if has_preferences:
    preferences_filtered_data = filter_by_preferences(filtered_data, st.session_state.user_preferences)
    
    # Jika tidak ada hasil dengan preferensi, gunakan data asli dengan pesan
    if preferences_filtered_data.empty and not filtered_data.empty:
        st.warning("Tidak ditemukan produk yang sesuai dengan preferensi Anda. Menampilkan semua produk yang sesuai dengan filter lainnya.")
    else:
        filtered_data = preferences_filtered_data

# Tampilkan metrik
display_metrics(filtered_data)

# Tampilkan produk dengan pagination
st.subheader("🏷️ Daftar Produk")
items_per_page = st.select_slider(
    "Jumlah produk per halaman",
    options=[5, 10, 15, 20, 25, 30],
    value=10
)

current_page = st.session_state.get('explore_current_page', 1)
paginated_data, total_pages = paginate_dataframe(
    filtered_data, 
    current_page, 
    items_per_page
)

# Navigasi halaman
if total_pages > 1:
    cols = st.columns(min(total_pages, 5))
    for i, col in enumerate(cols):
        page_num = i + 1
        if col.button(str(page_num), key=f"explore_page_{page_num}"):
            st.session_state.explore_current_page = page_num
            st.rerun()

# Tampilkan produk
if paginated_data.empty:
    st.warning("Tidak ditemukan produk yang sesuai dengan filter Anda.")
else:
    for _, product in paginated_data.iterrows():
        display_product_card(product)