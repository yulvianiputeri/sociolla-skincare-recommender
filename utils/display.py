import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import clean_reviews, format_price

def display_product_card(product, rank=None):
    """
    Menampilkan informasi produk menggunakan komponen Streamlit dengan perbaikan
    """
    try:
        rank_text = f"Peringkat #{rank} - " if rank else ""
        
        st.subheader(f"{rank_text}{product['brand']} - {product['product_name']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"✨ Kategori: {product['category']}")
            st.write(f"⭐ Penilaian: {float(product['rating']):.1f}/5.0")
        
        with col2:
            # Format harga
            if 'price_display' in product and not pd.isna(product['price_display']):
                price_display = str(product['price_display'])
                if '-' in price_display:
                    parts = [p.strip() for p in price_display.split('-') if p.strip()]
                    if len(parts) >= 2:
                        formatted_price = f" {parts[0]} -  {parts[1]}"
                    else:
                        formatted_price = price_display
                else:
                    formatted_price = price_display
                st.write(f"💰 Harga: {formatted_price}")
            else:
                try:
                    price = float(product['price'])
                    st.write(f"💰 Harga: Rp {int(price):,}".replace(",", "."))
                except:
                    st.write("💰 Harga: Tidak tersedia")
            
            # Tampilkan review - perbaikan logika
            review_count = clean_reviews(str(product.get('number_of_reviews', '0')))
            if review_count > 0:
                if review_count >= 1000:
                    formatted_review = f"({review_count/1000:.1f}k)".replace('.0k', 'k')
                else:
                    formatted_review = f"{review_count:,}".replace(",", ".")
                st.write(f"👥 Review: {formatted_review}")
            else:
                st.write("👥 Review: Belum ada review")

        # Tampilkan informasi repurchase berdasarkan tab
        repurchase_yes = clean_reviews(str(product.get('repurchase_yes', '0')))
        repurchase_no = clean_reviews(str(product.get('repurchase_no', '0')))
        repurchase_maybe = clean_reviews(str(product.get('repurchase_maybe', '0')))

        st.info(f"🔄 {repurchase_yes:,}".replace(",", ".") + " pengguna akan membeli kembali")
        st.warning(f"❌ {repurchase_no}" + " pengguna tidak akan membeli kembali")
        st.info(f"❓ {repurchase_maybe:,}".replace(",", ".") + " pengguna mungkin akan membeli kembali")
        
    except Exception as e:
        st.error(f"Error displaying product card: {str(e)}")

def paginate_dataframe(df, page_number, page_size):
    """
    Membuat pagination untuk DataFrame
    """
    total_pages = math.ceil(len(df) / page_size)
    start_idx = (page_number - 1) * page_size
    end_idx = min(start_idx + page_size, len(df))
    
    return df.iloc[start_idx:end_idx], total_pages

def display_metrics(data):
    """
    Menampilkan metrik statistik dengan penanganan error
    """
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        # Total Produk
        with col1:
            total_products = len(data)
            st.metric(
                "Total Produk", 
                f"{total_products:,}".replace(",", ".")
            )
        
        # Rating Rata-rata
        with col2:
            try:
                avg_rating = float(data['rating'].mean())
                st.metric(
                    "Rating Rata-rata", 
                    f"{avg_rating:.1f} ⭐"
                )
            except:
                st.metric("Rating Rata-rata", "N/A")
        
        # Harga Rata-rata
        with col3:
            try:
                avg_price = float(data['price'].mean())
                st.metric(
                    "Harga Rata-rata", 
                    f"Rp {int(avg_price):,}".replace(",", ".")
                )
            except:
                st.metric("Harga Rata-rata", "N/A")
        
        # Total Review
        with col4:
            try:
                # Convert to numeric first to handle any string values
                data['number_of_reviews'] = pd.to_numeric(data['number_of_reviews'], errors='coerce')
                total_reviews = int(data['number_of_reviews'].sum())
                st.metric(
                    "Total Review", 
                    f"{total_reviews:,}".replace(",", ".")
                )
            except Exception as e:
                st.metric("Total Review", "N/A")
                
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")
        # Optional: tampilkan debug info
        # st.write("Data shape:", data.shape)
        # st.write("Data columns:", data.columns.tolist())
        # st.write("Data types:", data.dtypes)

def create_price_range_analysis(data):
    """
    Membuat analisis berdasarkan range harga
    """
    try:
        # Buat kategori harga
        data = data.copy()  # Buat copy untuk menghindari warning
        data['price_range'] = pd.qcut(data['price'], q=5, labels=[
            'Sangat Murah', 'Murah', 'Menengah', 'Mahal', 'Sangat Mahal'
        ])
        
        # Analisis per range harga
        price_analysis = data.groupby('price_range').agg({
            'rating': 'mean',
            'number_of_reviews': 'mean'
        }).round(2)
        
        # Buat figure
        fig = go.Figure()
        
        # Bar untuk rating
        fig.add_trace(go.Bar(
            x=price_analysis.index,
            y=price_analysis['rating'],
            name='Rating Rata-rata',
            marker_color='#FF69B4',
            yaxis='y'
        ))
        
        # Line untuk review
        fig.add_trace(go.Scatter(
            x=price_analysis.index,
            y=price_analysis['number_of_reviews'],
            name='Review Rata-rata',
            line=dict(color='#FFD700', width=2),
            yaxis='y2'
        ))
        
        # Update layout
        fig.update_layout(
            title="Analisis Rating & Review Berdasarkan Range Harga",
            xaxis_title="Range Harga",
            yaxis_title="Rating Rata-rata",
            yaxis2=dict(
                title="Review Rata-rata",
                overlaying="y",
                side="right"
            ),
            template="plotly_white",
            showlegend=True,
            height=500
        )
        
        return fig
    except Exception as e:
        st.error(f"Error membuat analisis range harga: {str(e)}")
        return None

def apply_filters(data, selected_category, selected_brand, price_range):
    """
    Menerapkan filter kategori, brand, dan harga pada DataFrame
    
    Parameters:
    - data: DataFrame asli
    - selected_category: Kategori yang dipilih ('Semua' atau nama kategori)
    - selected_brand: Brand yang dipilih ('Semua' atau nama brand)
    - price_range: Tuple (min_price, max_price) dalam Rupiah
    
    Returns:
    - DataFrame yang sudah difilter
    """
    filtered_data = data.copy()
    
    # Filter kategori
    if selected_category != 'Semua':
        filtered_data = filtered_data[filtered_data['category'] == selected_category]
    
    # Filter brand
    if selected_brand != 'Semua':
        filtered_data = filtered_data[filtered_data['brand'] == selected_brand]
    
    # Filter harga - konversi price_range dari Rupiah ke nilai yang sesuai dengan data
    min_price = price_range[0] / 1000  # Konversi ke ribuan
    max_price = price_range[1] / 1000  # Konversi ke ribuan
    
    # Pastikan kolom price adalah numerik
    filtered_data['price'] = pd.to_numeric(filtered_data['price'], errors='coerce')
    
    # Terapkan filter harga
    filtered_data = filtered_data[
        (filtered_data['price'] >= min_price) & 
        (filtered_data['price'] <= max_price)
    ]
    
    return filtered_data
    