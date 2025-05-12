import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.data_loader import clean_reviews

# ========== Content-Based Filtering ==========
def get_content_based_recommendations(product_name, data, n_recommendations=5):
    """
    Mendapatkan rekomendasi berdasarkan fitur produk (kategori, brand, dll)
    """
    try:
        # Validasi awal produk yang dipilih
        if product_name not in data['product_name'].values:
            return pd.DataFrame()
            
        # Dapatkan kategori dan brand produk yang dipilih
        selected_product_df = data[data['product_name'] == product_name]
        if selected_product_df.empty:
            return pd.DataFrame()
            
        selected_product = selected_product_df.iloc[0]
        selected_category = selected_product['category']
        selected_brand = selected_product['brand']
        
        # Filter data berdasarkan kategori yang sama
        filtered_data = data[data['category'] == selected_category].copy()
        
        # Pastikan produk yang dipilih ada dalam filtered_data
        if product_name not in filtered_data['product_name'].values:
            return pd.DataFrame()
        
        # Filter untuk brand berbeda
        other_brands_data = filtered_data[filtered_data['brand'] != selected_brand].copy()
        
        if other_brands_data.empty:
            return pd.DataFrame()
        
        # Pendekatan alternatif: gunakan perbandingan langsung untuk atribut
        recommendations = []
        
        # Untuk setiap produk dari brand berbeda
        for _, candidate in other_brands_data.iterrows():
            similarity_score = 0.0
            
            # Kategori sama (sudah difilter sebelumnya)
            similarity_score += 0.5
            
            # Skor rating similarity
            if pd.notna(selected_product['rating']) and pd.notna(candidate['rating']):
                rating_diff = 1.0 - abs(float(selected_product['rating']) - float(candidate['rating'])) / 5.0
                similarity_score += rating_diff * 0.3
            
            # Tambahkan produk ke rekomendasi
            candidate_dict = candidate.to_dict()
            candidate_dict['content_score'] = similarity_score
            recommendations.append(candidate_dict)
        
        # Validasi hasil
        if not recommendations:
            return pd.DataFrame()
        
        # Urutkan berdasarkan similarity score
        recommendations_df = pd.DataFrame(recommendations)
        recommendations_df = recommendations_df.sort_values('content_score', ascending=False).head(n_recommendations)
        
        return recommendations_df
            
    except Exception as e:
        # Fallback ke metode similarity tanpa pesan error
        return get_similarity_recommendations(product_name, data, n_recommendations)

# ========== Similarity-Based Filtering ==========
def get_similarity_recommendations(product_name, data, n_recommendations=5):
    """
    Mendapatkan rekomendasi produk berdasarkan rating dan jumlah review
    """
    try:
        # Validasi awal produk yang dipilih
        if product_name not in data['product_name'].values:
            return pd.DataFrame()
            
        # Dapatkan info produk yang dipilih
        selected_product_df = data[data['product_name'] == product_name]
        if selected_product_df.empty:
            return pd.DataFrame()
            
        selected_product = selected_product_df.iloc[0]
        selected_category = selected_product['category']
        selected_brand = selected_product['brand']
        
        # Filter produk dengan kategori yang sama tapi brand berbeda
        filtered_data = data[
            (data['category'] == selected_category) & 
            (data['brand'] != selected_brand)
        ].copy()
        
        if filtered_data.empty:
            return pd.DataFrame()

        # Hitung skor review
        filtered_data['clean_reviews'] = filtered_data['number_of_reviews'].apply(clean_reviews)
        filtered_data['review_weight'] = np.log1p(filtered_data['clean_reviews'])
        max_reviews = filtered_data['review_weight'].max()
        if max_reviews > 0:
            filtered_data['review_weight'] = filtered_data['review_weight'] / max_reviews
        else:
            filtered_data['review_weight'] = 0

        # Hitung skor rating
        filtered_data['rating_normalized'] = pd.to_numeric(filtered_data['rating'], errors='coerce').fillna(0)
        max_rating = filtered_data['rating_normalized'].max()
        if max_rating > 0:
            filtered_data['rating_normalized'] = filtered_data['rating_normalized'] / max_rating
        else:
            filtered_data['rating_normalized'] = 0

        # Hitung skor akhir
        filtered_data['similarity_score'] = (
            filtered_data['rating_normalized'] * 0.6 +
            filtered_data['review_weight'] * 0.4
        )

        # Validasi nilai similarity_score
        filtered_data['similarity_score'] = filtered_data['similarity_score'].fillna(0)

        # Urutkan rekomendasi
        recommendations = filtered_data.sort_values(
            by=['similarity_score'], 
            ascending=False
        ).head(n_recommendations)
        
        # Pastikan recommendations tidak kosong
        if recommendations.empty:
            return pd.DataFrame()
            
        return recommendations

    except Exception as e:
        return pd.DataFrame()

# ========== Fungsi Utama untuk Mendapatkan Rekomendasi ==========
def get_ml_recommendations(product_name, data, method="hybrid", n_recommendations=5):
    """
    Fungsi utama untuk mendapatkan rekomendasi produk
    
    Parameters:
    - product_name: Nama produk yang ingin diberikan rekomendasi serupa
    - data: DataFrame dengan data produk
    - method: Metode rekomendasi (default: hybrid)
    - n_recommendations: Jumlah rekomendasi yang diinginkan
    
    Returns:
    - DataFrame dengan produk yang direkomendasikan
    """
    try:
        # Validasi keberadaan produk
        if product_name not in data['product_name'].values:
            return pd.DataFrame()
        
        # Jika metode bukan hybrid, langsung panggil fungsi terkait
        if method == "content_based":
            return get_content_based_recommendations(product_name, data, n_recommendations)
        elif method == "similarity":
            return get_similarity_recommendations(product_name, data, n_recommendations)
        
        # Untuk metode hybrid, kita gunakan pendekatan robust
        # Coba dapatkan rekomendasi dengan similarity-based (lebih stabil)
        similarity_recommendations = get_similarity_recommendations(product_name, data, n_recommendations)
        
        # Jika similarity berhasil, gunakan itu sebagai hasil
        if not similarity_recommendations.empty:
            return similarity_recommendations
        
        # Jika similarity gagal, coba content-based
        content_recommendations = get_content_based_recommendations(product_name, data, n_recommendations)
        
        # Jika content-based berhasil, gunakan itu sebagai hasil
        if not content_recommendations.empty:
            return content_recommendations
        
        # Jika kedua pendekatan gagal
        return pd.DataFrame()
        
    except Exception as e:
        return pd.DataFrame()
    
# Contoh cara menambahkan mode debug yang dapat diaktifkan/dinonaktifkan
# if 'debug_mode' in st.session_state and st.session_state.debug_mode:
#    st.info("Debug info...")