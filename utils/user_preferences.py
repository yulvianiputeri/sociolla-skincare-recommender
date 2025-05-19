import streamlit as st
import pandas as pd

# Definisi jenis kulit
SKIN_TYPES = [
    "Normal", 
    "Kering", 
    "Berminyak", 
    "Kombinasi", 
    "Sensitif"
]

# Definisi permasalahan kulit
SKIN_CONCERNS = [
    "Jerawat",
    "Penuaan Dini",
    "Hiperpigmentasi",
    "Kulit Kusam",
    "Pori-pori Besar",
    "Kemerahan",
    "Tekstur Tidak Rata",
    "Skin Barrier Rusak"
]

# Definisi bahan yang dihindari
AVOID_INGREDIENTS = [
    "Alcohol", 
    "Fragrance", 
    "Paraben", 
    "Sulfate", 
    "Essential Oils"
]

# Definisi bahan yang disukai
PREFERRED_INGREDIENTS = [
    "Hyaluronic Acid", 
    "Niacinamide", 
    "Vitamin C", 
    "Retinol", 
    "Salicylic Acid",
    "Centella Asiatica",
    "Peptides",
    "Ceramide",
    "Tea Tree",
    "AHA/BHA"
]

def show_preference_filters():
    """
    Menampilkan filter preferensi pengguna dan menyimpannya ke session state
    """
    st.sidebar.markdown("---")
    st.sidebar.header("🧬 Preferensi Personal")
    
    # Inisialisasi nilai default dari session state jika ada
    current_preferences = st.session_state.get("user_preferences", {})
    
    # Jenis Kulit dengan nilai default
    current_skin_type = current_preferences.get("skin_type", None)
    skin_type_index = 0  # Default "Tidak dipilih"
    if current_skin_type and current_skin_type in SKIN_TYPES:
        skin_type_index = SKIN_TYPES.index(current_skin_type) + 1
    
    selected_skin_type = st.sidebar.selectbox(
        "Jenis Kulit Anda", 
        options=["Tidak dipilih"] + SKIN_TYPES,
        index=skin_type_index,
        help="Pilih jenis kulit Anda untuk mendapatkan rekomendasi yang lebih relevan"
    )
    
    # Permasalahan Kulit dengan nilai default
    current_concerns = current_preferences.get("skin_concerns", [])
    selected_concerns = st.sidebar.multiselect(
        "Permasalahan Kulit", 
        options=SKIN_CONCERNS,
        default=current_concerns,
        help="Pilih permasalahan kulit yang ingin Anda atasi"
    )
    
    # Bahan yang dihindari dengan nilai default
    current_avoid = current_preferences.get("avoid_ingredients", [])
    avoid_ingredients = st.sidebar.multiselect(
        "Bahan yang Dihindari",
        options=AVOID_INGREDIENTS,
        default=current_avoid,
        help="Pilih bahan-bahan yang ingin Anda hindari dalam produk skincare"
    )
    
    # Bahan yang disukai dengan nilai default
    current_preferred = current_preferences.get("preferred_ingredients", [])
    preferred_ingredients = st.sidebar.multiselect(
        "Bahan yang Disukai",
        options=PREFERRED_INGREDIENTS,
        default=current_preferred,
        help="Pilih bahan-bahan yang Anda sukai dalam produk skincare"
    )
    
    # Tombol untuk reset preferensi
    if st.sidebar.button("🔄 Reset Preferensi"):
        st.session_state.user_preferences = None
        st.rerun()
    
    # Simpan preferensi ke session state
    preferences = {}
    
    # Hanya simpan jika ada yang dipilih
    if selected_skin_type != "Tidak dipilih":
        preferences["skin_type"] = selected_skin_type
    
    if selected_concerns:
        preferences["skin_concerns"] = selected_concerns
        
    if avoid_ingredients:
        preferences["avoid_ingredients"] = avoid_ingredients
        
    if preferred_ingredients:
        preferences["preferred_ingredients"] = preferred_ingredients
    
    # Update session state
    if preferences:
        st.session_state.user_preferences = preferences
    else:
        st.session_state.user_preferences = None
        
    # Tampilkan info singkat tentang preferensi yang dipilih
    if st.session_state.get("user_preferences"):
        st.sidebar.success("✅ Preferensi tersimpan!")
        prefs = st.session_state.user_preferences
        
        info_text = []
        if prefs.get("skin_type"):
            info_text.append(f"Kulit: {prefs['skin_type']}")
        if prefs.get("skin_concerns"):
            info_text.append(f"Masalah: {len(prefs['skin_concerns'])} item")
        if prefs.get("avoid_ingredients"):
            info_text.append(f"Hindari: {len(prefs['avoid_ingredients'])} bahan")
        if prefs.get("preferred_ingredients"):
            info_text.append(f"Suka: {len(prefs['preferred_ingredients'])} bahan")
        
        if info_text:
            st.sidebar.info("📝 " + " | ".join(info_text))
    else:
        st.sidebar.info("ℹ️ Belum ada preferensi yang dipilih")
        
    return st.session_state.get("user_preferences")

def filter_by_preferences(data, preferences):
    """
    Filter produk berdasarkan preferensi pengguna
    
    Parameters:
    - data: DataFrame produk
    - preferences: Dict preferensi pengguna
    
    Returns:
    - DataFrame produk yang difilter
    """
    if preferences is None:
        return data
    
    filtered_data = data.copy()
    
    # Filter berdasarkan jenis kulit (jika ada)
    if preferences.get("skin_type"):
        skin_type = preferences["skin_type"]
        
        # Gunakan kolom suitable_skin_types yang sudah tersedia
        if 'suitable_skin_types' in filtered_data.columns:
            # Pilih produk yang cocok untuk jenis kulit tertentu atau "Semua Jenis Kulit"
            skin_type_filter = (
                filtered_data['suitable_skin_types'].str.contains(skin_type, case=False, na=False) | 
                filtered_data['suitable_skin_types'].str.contains('Semua Jenis Kulit', case=False, na=False)
            )
            
            if skin_type_filter.any():
                filtered_data = filtered_data[skin_type_filter]
    
    # Filter berdasarkan permasalahan kulit (jika ada)
    if preferences.get("skin_concerns") and len(preferences["skin_concerns"]) > 0:
        # Gunakan kolom targets_skin_concerns yang sudah tersedia
        if 'targets_skin_concerns' in filtered_data.columns:
            # Buat filter untuk setiap masalah kulit
            concern_filter = False
            for concern in preferences["skin_concerns"]:
                concern_filter = concern_filter | filtered_data['targets_skin_concerns'].str.contains(concern, case=False, na=False)
            
            if concern_filter.any():
                filtered_data = filtered_data[concern_filter]
    
    # Filter berdasarkan bahan yang harus dihindari (jika ada)
    if preferences.get("avoid_ingredients") and len(preferences["avoid_ingredients"]) > 0:
        # Gunakan kolom key_ingredients untuk menghindari bahan tertentu
        if 'key_ingredients' in filtered_data.columns:
            avoid_filter = True  # Mulai dengan semua produk
            
            for ingredient in preferences["avoid_ingredients"]:
                # Kecualikan produk yang mengandung bahan yang dihindari
                avoid_filter = avoid_filter & ~filtered_data['key_ingredients'].str.contains(ingredient, case=False, na=False)
            
            if avoid_filter.any():
                filtered_data = filtered_data[avoid_filter]
    
    return filtered_data

def rank_by_preferences(recommendations, preferences):
    """
    Memberikan bobot tambahan pada produk yang sesuai dengan preferensi
    
    Parameters:
    - recommendations: DataFrame rekomendasi produk
    - preferences: Dict preferensi pengguna
    
    Returns:
    - DataFrame rekomendasi dengan skor yang disesuaikan
    """
    if preferences is None or recommendations.empty:
        return recommendations
    
    adjusted_recommendations = recommendations.copy()
    
    # Tambahkan kolom preference_score
    adjusted_recommendations['preference_score'] = 0.0
    
    # 1. Tambahkan bobot untuk produk yang sesuai dengan jenis kulit
    if preferences.get("skin_type") and 'suitable_skin_types' in adjusted_recommendations.columns:
        skin_type = preferences["skin_type"]
        
        # Cek apakah produk cocok untuk jenis kulit tertentu
        skin_type_match = adjusted_recommendations['suitable_skin_types'].str.contains(skin_type, case=False, na=False)
        
        # Tambahkan bobot 0.3 untuk produk yang cocok dengan jenis kulit
        adjusted_recommendations.loc[skin_type_match, 'preference_score'] += 0.3
    
    # 2. Tambahkan bobot untuk produk yang mengatasi permasalahan kulit
    if preferences.get("skin_concerns") and 'targets_skin_concerns' in adjusted_recommendations.columns:
        for concern in preferences["skin_concerns"]:
            # Cek apakah produk mengatasi masalah kulit tertentu
            concern_match = adjusted_recommendations['targets_skin_concerns'].str.contains(concern, case=False, na=False)
            
            # Tambahkan bobot 0.15 untuk setiap permasalahan kulit yang cocok
            adjusted_recommendations.loc[concern_match, 'preference_score'] += 0.15
    
    # 3. Tambahkan bobot untuk produk yang mengandung bahan yang disukai
    if preferences.get("preferred_ingredients") and 'key_ingredients' in adjusted_recommendations.columns:
        for ingredient in preferences["preferred_ingredients"]:
            # Cek apakah produk mengandung bahan yang disukai
            ingredient_match = adjusted_recommendations['key_ingredients'].str.contains(ingredient, case=False, na=False)
            
            # Tambahkan bobot 0.1 untuk setiap bahan yang disukai
            adjusted_recommendations.loc[ingredient_match, 'preference_score'] += 0.1
    
    # 4. Gabungkan preference_score dengan similarity_score
    if 'similarity_score' in adjusted_recommendations.columns:
        # Gunakan bobot 70% untuk similarity_score original dan 30% untuk preference_score
        adjusted_recommendations['final_score'] = (
            0.7 * adjusted_recommendations['similarity_score'] + 
            0.3 * adjusted_recommendations['preference_score']
        )
        
        # Ganti similarity_score dengan final_score
        adjusted_recommendations['similarity_score'] = adjusted_recommendations['final_score']
        
        # Hapus kolom temporary
        adjusted_recommendations = adjusted_recommendations.drop(['preference_score', 'final_score'], axis=1)
        
        # Urutkan ulang berdasarkan skor yang disesuaikan
        adjusted_recommendations = adjusted_recommendations.sort_values('similarity_score', ascending=False)
    
    return adjusted_recommendations

def explain_preference_match(product, preferences):
    """
    Menjelaskan mengapa produk cocok dengan preferensi pengguna
    
    Parameters:
    - product: Series data produk
    - preferences: Dict preferensi pengguna
    
    Returns:
    - String penjelasan kesesuaian produk dengan preferensi
    """
    if preferences is None:
        return None
        
    explanations = []
    
    # Cek kesesuaian dengan jenis kulit
    if preferences.get("skin_type") and 'suitable_skin_types' in product:
        skin_type = preferences["skin_type"]
        if pd.notna(product['suitable_skin_types']) and skin_type in product['suitable_skin_types']:
            explanations.append(f"✅ Cocok untuk jenis kulit {skin_type}")
    
    # Cek kesesuaian dengan masalah kulit
    if preferences.get("skin_concerns") and 'targets_skin_concerns' in product and pd.notna(product['targets_skin_concerns']):
        matching_concerns = []
        for concern in preferences["skin_concerns"]:
            if concern in product['targets_skin_concerns']:
                matching_concerns.append(concern)
        
        if matching_concerns:
            if len(matching_concerns) == 1:
                explanations.append(f"✅ Mengatasi masalah {matching_concerns[0]}")
            else:
                explanations.append(f"✅ Mengatasi masalah: {', '.join(matching_concerns)}")
    
    # Cek kesesuaian dengan bahan yang disukai
    if preferences.get("preferred_ingredients") and 'key_ingredients' in product and pd.notna(product['key_ingredients']):
        matching_ingredients = []
        for ingredient in preferences["preferred_ingredients"]:
            if ingredient in product['key_ingredients']:
                matching_ingredients.append(ingredient)
        
        if matching_ingredients:
            if len(matching_ingredients) == 1:
                explanations.append(f"✅ Mengandung {matching_ingredients[0]} yang Anda sukai")
            else:
                explanations.append(f"✅ Mengandung bahan yang Anda sukai: {', '.join(matching_ingredients)}")
    
    # Gabungkan semua penjelasan
    if explanations:
        return "\n".join(explanations)
    else:
        return None