import streamlit as st
from config.constants import PRODUCT_CATEGORIES
from utils.data_loader import load_data
from utils.user_preferences import show_preference_filters

# Konfigurasi halaman
st.set_page_config(
    page_title="Rekomendasi Skincare Sociolla",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Judul aplikasi
st.title("🧴 Rekomendasi Produk Skincare Sociolla")
st.write("Temukan produk skincare yang sesuai dengan kebutuhan Anda berdasarkan machine learning")

# Load data (menyimpan di session state agar bisa digunakan di halaman lain)
with st.spinner('Memuat data...'):
    if 'data' not in st.session_state:
        data = load_data()
        if data is not None:
            st.session_state.data = data
        else:
            st.error("Tidak dapat memuat data. Silakan cek file data Anda.")

# Sidebar - Informasi kategori
with st.sidebar:
    st.title("Panduan Kategori Produk")
    for category, info in PRODUCT_CATEGORIES.items():
        with st.expander(f"{info['icon']} {category}"):
            st.write(f"**Deskripsi:** {info['description']}")
            st.write("**Manfaat:**")
            for benefit in info['benefits']:
                st.write(f"- {benefit}")
    
    # Tambahkan filter preferensi pengguna
    user_preferences = show_preference_filters()
    
    # Tambahkan informasi tentang machine learning
    st.sidebar.markdown("---")
    st.sidebar.write("### 🧠 Sistem Rekomendasi")
    st.sidebar.info("""
    Aplikasi ini menggunakan sistem rekomendasi yang mengkombinasikan:
    
    1. **Content-Based Filtering** - Merekomendasikan produk dengan karakteristik serupa
    
    2. **Similarity-Based Filtering** - Merekomendasikan produk berdasarkan rating dan popularitas
    
    Hasil rekomendasi mempertimbangkan kesamaan produk dan penilaian pengguna untuk memberikan saran yang paling relevan.
    """)

# Berikan informasi tambahan tentang aplikasi
st.markdown("""
## Selamat Datang di Aplikasi Rekomendasi Skincare!

Aplikasi ini dikembangkan untuk membantu Anda menemukan produk skincare yang sesuai dengan kebutuhan Anda.

### 🌟 Fitur Utama
- **Jelajahi Produk** - Filter dan cari produk skincare berdasarkan kategori, brand, dan harga
- **Rekomendasi Cerdas** - Dapatkan rekomendasi produk serupa berdasarkan teknologi machine learning
- **Analisis Data** - Visualisasi data dan insight tentang tren produk skincare
- **Preferensi Personal** - Tentukan jenis kulit dan permasalahan kulit untuk rekomendasi yang lebih personal

### 🧠 Teknologi Machine Learning
Aplikasi ini menggunakan pendekatan *hybrid recommendation system* yang mengkombinasikan:

1. **Content-Based Filtering** - Merekomendasikan produk berdasarkan karakteristik dan fitur produk
2. **Similarity-Based Filtering** - Merekomendasikan produk berdasarkan rating dan popularitas
3. **Preference-Based Personalization** - Menyesuaikan rekomendasi berdasarkan jenis kulit dan kebutuhan Anda

### 📱 Cara Menggunakan
Gunakan menu di sidebar untuk menavigasi ke halaman berbeda:
- **Explore Page** - Untuk mencari dan filter produk
- **Recommendation Page** - Untuk mendapatkan rekomendasi produk
- **Analysis Page** - Untuk melihat analisis data dan insight
""")

# Tampilkan preferensi pengguna jika ada
if 'user_preferences' in st.session_state and st.session_state.user_preferences:
    preferences = st.session_state.user_preferences
    st.success("✅ Preferensi Anda telah disimpan!")
    
    st.write("### 🧬 Preferensi Personal Anda")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Jenis Kulit:**")
        st.info(preferences.get("skin_type", "Tidak dipilih"))
        
        st.write("**Bahan yang Dihindari:**")
        avoid_ingredients = preferences.get("avoid_ingredients", [])
        if avoid_ingredients:
            for ingredient in avoid_ingredients:
                st.info(ingredient)
        else:
            st.info("Tidak dipilih")
    
    with col2:
        st.write("**Permasalahan Kulit:**")
        skin_concerns = preferences.get("skin_concerns", [])
        if skin_concerns:
            for concern in skin_concerns:
                st.info(concern)
        else:
            st.info("Tidak dipilih")
            
        st.write("**Bahan yang Disukai:**")
        preferred_ingredients = preferences.get("preferred_ingredients", [])
        if preferred_ingredients:
            for ingredient in preferred_ingredients:
                st.info(ingredient)
        else:
            st.info("Tidak dipilih")
    
    # Tampilkan informasi tentang bagaimana preferensi digunakan
    st.markdown("""
    ### 🔍 Bagaimana Preferensi Anda Digunakan?
    
    Preferensi yang Anda pilih akan digunakan untuk:
    
    1. **Filter Produk** - Produk yang tidak sesuai dengan jenis kulit dan masalah kulit Anda akan difilter
    
    2. **Prioritas Rekomendasi** - Produk yang cocok untuk jenis kulit dan masalah kulit Anda akan mendapat prioritas lebih tinggi
    
    3. **Perhitungan Skor** - Algoritma kami akan memberikan bobot tambahan pada produk yang:
       - Cocok untuk jenis kulit Anda (30% bobot preferensi)
       - Mengatasi masalah kulit yang Anda pilih (15% bobot per masalah)
       - Mengandung bahan yang Anda sukai (10% bobot per bahan)
       - Tidak mengandung bahan yang Anda hindari (filter)
    
    4. **Penjelasan Rekomendasi** - Anda akan melihat penjelasan mengapa produk tertentu direkomendasikan berdasarkan preferensi Anda
    """)
    
    # Tampilkan contoh rekomendasi berdasarkan preferensi
    st.markdown("""
    ### 💡 Contoh Rekomendasi Berdasarkan Preferensi
    
    Berdasarkan preferensi Anda, kami akan merekomendasikan produk seperti:
    """)
    
    # Cari contoh produk yang sesuai dengan preferensi
    if 'data' in st.session_state:
        sample_data = st.session_state.data.copy()
        
        # Filter berdasarkan jenis kulit
        if preferences.get("skin_type") and 'suitable_skin_types' in sample_data.columns:
            sample_data = sample_data[
                sample_data['suitable_skin_types'].str.contains(
                    preferences.get("skin_type"), 
                    case=False, 
                    na=False
                )
            ]
        
        # Filter berdasarkan masalah kulit
        if preferences.get("skin_concerns") and 'targets_skin_concerns' in sample_data.columns:
            concern_filter = False
            for concern in preferences.get("skin_concerns"):
                concern_filter = concern_filter | sample_data['targets_skin_concerns'].str.contains(
                    concern, 
                    case=False, 
                    na=False
                )
            if concern_filter.any():
                sample_data = sample_data[concern_filter]
        
        # Tampilkan 1 contoh produk dari setiap kategori
        if not sample_data.empty:
            # Ambil kategori unik
            categories = sample_data['category'].unique()
            
            for category in categories[:3]:  # Batasi hanya 3 kategori
                category_samples = sample_data[sample_data['category'] == category]
                if not category_samples.empty:
                    # Ambil produk dengan rating tertinggi
                    best_product = category_samples.sort_values('rating', ascending=False).iloc[0]
                    
                    # Tampilkan produk
                    from utils.display import display_product_card
                    st.write(f"#### {category}")
                    display_product_card(best_product)
        else:
            st.warning("Tidak ditemukan produk yang cocok dengan preferensi Anda. Silakan sesuaikan preferensi Anda.")