import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_data, clean_reviews
from utils.display import display_product_card, paginate_dataframe, display_metrics, apply_filters
from utils.charts import create_rating_chart, create_price_chart, create_brand_chart, create_category_rating_chart, create_repurchase_analysis
from config.constants import PRODUCT_CATEGORIES
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="Rekomendasi Skincare Sociolla",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_recommendations(product_name, data, n_recommendations=5):
    """
    Mendapatkan rekomendasi produk berdasarkan rating dan jumlah review
    """
    try:
        # 1. Dapatkan info produk yang dipilih
        selected_product = data[data['product_name'] == product_name].iloc[0]
        selected_category = selected_product['category']
        selected_brand = selected_product['brand']
        
        # Debug info
        #st.write("Debug - Selected product info:")
        #st.write(f"- Category: {selected_category}")
        #st.write(f"- Brand: {selected_brand}")

        # 2. Filter produk dengan kategori yang sama tapi brand berbeda
        filtered_data = data[
            (data['category'] == selected_category) & 
            (data['brand'] != selected_brand)
        ].copy()
        
        # Debug info
        #st.write(f"Debug - Found {len(filtered_data)} products in same category from other brands")

        if filtered_data.empty:
            st.warning("Tidak ditemukan produk lain dalam kategori yang sama")
            return pd.DataFrame()

        # 3. Bersihkan dan konversi data review
        filtered_data['clean_reviews'] = filtered_data['number_of_reviews'].apply(clean_reviews)
        
        # Hitung skor
        filtered_data['review_weight'] = np.log1p(filtered_data['clean_reviews'])
        max_reviews = filtered_data['review_weight'].max()
        if max_reviews > 0:
            filtered_data['review_weight'] = filtered_data['review_weight'] / max_reviews

        # Normalisasi rating
        filtered_data['rating_normalized'] = pd.to_numeric(filtered_data['rating'], errors='coerce').fillna(0)
        max_rating = filtered_data['rating_normalized'].max()
        if max_rating > 0:
            filtered_data['rating_normalized'] = filtered_data['rating_normalized'] / max_rating

        # Skor gabungan (50% rating, 50% review weight)
        filtered_data['score'] = (
            filtered_data['rating_normalized'] * 0.5 +
            filtered_data['review_weight'] * 0.5
        )

        # 4. Urutkan rekomendasi
        recommendations = filtered_data.sort_values(
            by=['score', 'rating', 'clean_reviews'],
            ascending=[False, False, False]
        )

        # Debug info
        #st.write("\nDebug - Top 3 recommendations scores:")
        #for _, row in recommendations.head(3).iterrows():
        #    st.write(f"- {row['product_name']}: rating={row['rating']}, reviews={row['number_of_reviews']} ({row['clean_reviews']}), score={row['score']:.2f}")

        # Kembalikan rekomendasi tanpa kolom tambahan
        final_recommendations = recommendations.drop(columns=[
            'clean_reviews', 'review_weight', 'rating_normalized', 'score'
        ], errors='ignore')
        
        return final_recommendations.head(n_recommendations)

    except Exception as e:
        st.error(f"Error dalam pembuatan rekomendasi: {str(e)}")
        # Tambahkan debugging info
        #st.write("Debug info:")
        #st.write("- Selected product name:", product_name)
        #st.write("- Data columns:", data.columns.tolist())
        #st.write("- Data shape:", data.shape)
        return pd.DataFrame()

def main():
    # Judul aplikasi
    st.title("🧴 Rekomendasi Produk Skincare Sociolla")
    st.write("Temukan produk skincare yang sesuai dengan kebutuhan Anda")
    
    # Load data
    with st.spinner('Memuat data...'):
        data = load_data()
        
    if data is None:
        st.error("Tidak dapat melanjutkan karena error saat memuat data.")
        return
    
    # Sidebar - Informasi kategori
    st.sidebar.title("Panduan Kategori Produk")
    for category, info in PRODUCT_CATEGORIES.items():
        with st.sidebar.expander(f"{info['icon']} {category}"):
            st.write(f"**Deskripsi:** {info['description']}")
            st.write("**Manfaat:**")
            for benefit in info['benefits']:
                st.write(f"- {benefit}")
    
    # Tab utama
    tab1, tab2, tab3 = st.tabs(["🔍 Jelajahi", "💫 Rekomendasi", "📊 Analisis"])
    
    with tab1:
        # Filter produk
        col1, col2 = st.columns(2)
        
        with col1:
            selected_category = st.selectbox(
                "Pilih Kategori Produk",
                options=['Semua'] + list(PRODUCT_CATEGORIES.keys())
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
        
        # Tampilkan metrik
        display_metrics(filtered_data)
        
        # Tampilkan produk dengan pagination
        st.subheader("🏷️ Daftar Produk")
        items_per_page = st.select_slider(
            "Jumlah produk per halaman",
            options=[5, 10, 15, 20, 25, 30],
            value=10
        )
        
        current_page = st.session_state.get('current_page', 1)
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
                if col.button(str(page_num)):
                    st.session_state.current_page = page_num
                    st.rerun()
        
        # Tampilkan produk
        for _, product in paginated_data.iterrows():
            display_product_card(product)
    
        with tab2:
            st.subheader("🎯 Rekomendasi Produk Serupa")
            st.write("Kami akan merekomendasikan produk dari brand lain dalam kategori yang sama")
            
            # 1. Pilih kategori
            selected_category = st.selectbox(
                "Pilih Kategori Produk",
                options=list(PRODUCT_CATEGORIES.keys()),
                format_func=lambda x: f"{PRODUCT_CATEGORIES[x]['icon']} {x}"
            )
            
            # Filter data berdasarkan kategori
            category_data = data[data['category'] == selected_category]
            
            # 2. Pilih brand
            available_brands = sorted(category_data['brand'].unique())
            selected_brand = st.selectbox(
                "Pilih Brand",
                options=available_brands
            )
            
            # 3. Pilih produk dari brand tersebut
            brand_products = category_data[category_data['brand'] == selected_brand]
            selected_product = st.selectbox(
                "Pilih Produk",
                options=list(brand_products['product_name'].unique()),
                help=f"Pilih produk {selected_category} dari brand {selected_brand}"
            )
            
            if st.button("🔍 Cari Rekomendasi", use_container_width=True):
                with st.spinner(f"Mencari produk {selected_category} yang serupa dari brand lain..."):
                    # Filter untuk mendapatkan produk dari brand lain dalam kategori yang sama
                    other_brand_products = data[
                        (data['category'] == selected_category) & 
                        (data['brand'] != selected_brand)
                    ]
                    
                    # Hitung similarity
                    if len(other_brand_products) > 0:
                        recommendations = get_recommendations(selected_product, data)
                        
                        if not recommendations.empty:
                            st.success(f"Berikut rekomendasi produk {selected_category} dari brand lain:")
                            for idx, (_, product) in enumerate(recommendations.iterrows(), 1):
                                display_product_card(product, idx)
                        else:
                            st.warning(f"Tidak ditemukan rekomendasi {selected_category} yang sesuai dari brand lain")
    
    with tab3:
        st.subheader("📊 Analisis Data")

        # Tampilkan semua grafik
        if st.checkbox("Tampilkan Analisis Rating"):
            fig_rating = create_rating_chart(data)
            st.plotly_chart(fig_rating)

        if st.checkbox("Tampilkan Analisis Harga"):
            fig_price = create_price_chart(data)
            st.plotly_chart(fig_price)

        if st.checkbox("Tampilkan Analisis Brand"):
            fig_brand = create_brand_chart(data)
            st.plotly_chart(fig_brand)

        if st.checkbox("Tampilkan Analisis Kategori"):
            fig_category = create_category_rating_chart(data)
            st.plotly_chart(fig_category)

        if st.checkbox("Tampilkan Analisis Pembelian Ulang"):
            fig_repurchase = create_repurchase_analysis(data)
            st.plotly_chart(fig_repurchase)


if __name__ == "__main__":
    main()