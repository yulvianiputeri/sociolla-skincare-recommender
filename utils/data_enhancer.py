import pandas as pd
import numpy as np
import re

def enhance_product_data(data):
    """
    Memperkaya data produk dengan menambahkan atribut
    jenis kulit dan masalah kulit
    
    Parameters:
    - data: DataFrame original produk
    
    Returns:
    - DataFrame yang diperkaya dengan atribut tambahan
    """
    enhanced_data = data.copy()
    
    # Tambahkan kolom untuk jenis kulit yang cocok
    enhanced_data['suitable_skin_types'] = None
    
    # Tambahkan kolom untuk masalah kulit yang diatasi
    enhanced_data['targets_skin_concerns'] = None
    
    # Tambahkan kolom untuk bahan utama
    enhanced_data['key_ingredients'] = None
    
    # ----- Pembersih Wajah -----
    # Ekstrak informasi berdasarkan nama produk dan kategori
    cleansers = enhanced_data[enhanced_data['category'] == 'Pembersih Wajah']
    
    # Tentukan jenis kulit berdasarkan nama produk
    for idx, row in cleansers.iterrows():
        product_name = row['product_name'].lower()
        
        # Jenis kulit
        skin_types = []
        if any(term in product_name for term in ['oily', 'minyak', 'berminyak', 'acne', 'jerawat']):
            skin_types.append('Berminyak')
        if any(term in product_name for term in ['dry', 'kering', 'moisturizing', 'hydrating']):
            skin_types.append('Kering')
        if any(term in product_name for term in ['sensitive', 'sensitif', 'calm', 'soothing']):
            skin_types.append('Sensitif')
        if any(term in product_name for term in ['combination', 'kombinasi']):
            skin_types.append('Kombinasi')
        
        # Default jika tidak ada yang terdeteksi
        if not skin_types:
            skin_types = ['Normal', 'Kombinasi']
        
        # Masalah kulit
        concerns = []
        if any(term in product_name for term in ['acne', 'jerawat', 'blemish', 'pimple']):
            concerns.append('Jerawat')
        if any(term in product_name for term in ['pore', 'pori']):
            concerns.append('Pori-pori Besar')
        if any(term in product_name for term in ['bright', 'cerah', 'glow', 'white', 'putih']):
            concerns.append('Kulit Kusam')
        if any(term in product_name for term in ['exfoliat', 'scrub']):
            concerns.append('Tekstur Tidak Rata')
        
        # Bahan utama
        ingredients = []
        if 'salicylic' in product_name or 'bha' in product_name:
            ingredients.append('Salicylic Acid')
        if 'glycolic' in product_name or 'aha' in product_name:
            ingredients.append('Glycolic Acid')
        if 'tea tree' in product_name:
            ingredients.append('Tea Tree')
        if 'hyaluronic' in product_name or 'hyaluron' in product_name:
            ingredients.append('Hyaluronic Acid')
        if 'centella' in product_name or 'cica' in product_name:
            ingredients.append('Centella Asiatica')
        
        # Update data
        enhanced_data.at[idx, 'suitable_skin_types'] = ', '.join(skin_types)
        enhanced_data.at[idx, 'targets_skin_concerns'] = ', '.join(concerns) if concerns else None
        enhanced_data.at[idx, 'key_ingredients'] = ', '.join(ingredients) if ingredients else None
    
    # ----- Pelembab -----
    moisturizers = enhanced_data[enhanced_data['category'] == 'Pelembab']
    
    for idx, row in moisturizers.iterrows():
        product_name = row['product_name'].lower()
        
        # Jenis kulit
        skin_types = []
        if any(term in product_name for term in ['oily', 'minyak', 'berminyak', 'light', 'ringan']):
            skin_types.append('Berminyak')
        if any(term in product_name for term in ['dry', 'kering', 'moisturizing', 'hydrating', 'intense']):
            skin_types.append('Kering')
        if any(term in product_name for term in ['sensitive', 'sensitif', 'calm', 'soothing']):
            skin_types.append('Sensitif')
        if any(term in product_name for term in ['combination', 'kombinasi']):
            skin_types.append('Kombinasi')
        
        # Default jika tidak ada yang terdeteksi
        if not skin_types:
            skin_types = ['Normal', 'Kombinasi']
        
        # Masalah kulit
        concerns = []
        if any(term in product_name for term in ['acne', 'jerawat', 'blemish']):
            concerns.append('Jerawat')
        if any(term in product_name for term in ['bright', 'cerah', 'glow', 'white', 'putih']):
            concerns.append('Kulit Kusam')
        if any(term in product_name for term in ['aging', 'anti-aging', 'wrinkle', 'keriput']):
            concerns.append('Penuaan Dini')
        if any(term in product_name for term in ['repair', 'barrier']):
            concerns.append('Skin Barrier Rusak')
        
        # Bahan utama
        ingredients = []
        if 'niacinamide' in product_name:
            ingredients.append('Niacinamide')
        if 'hyaluronic' in product_name or 'hyaluron' in product_name:
            ingredients.append('Hyaluronic Acid')
        if 'centella' in product_name or 'cica' in product_name:
            ingredients.append('Centella Asiatica')
        if 'ceramide' in product_name:
            ingredients.append('Ceramide')
        if 'collagen' in product_name:
            ingredients.append('Collagen')
        if 'vitamin c' in product_name or 'vit c' in product_name:
            ingredients.append('Vitamin C')
        
        # Update data
        enhanced_data.at[idx, 'suitable_skin_types'] = ', '.join(skin_types)
        enhanced_data.at[idx, 'targets_skin_concerns'] = ', '.join(concerns) if concerns else None
        enhanced_data.at[idx, 'key_ingredients'] = ', '.join(ingredients) if ingredients else None
    
    # ----- Sunscreen -----
    sunscreens = enhanced_data[enhanced_data['category'] == 'Sunscreen']
    
    for idx, row in sunscreens.iterrows():
        product_name = row['product_name'].lower()
        
        # Jenis kulit
        skin_types = []
        if any(term in product_name for term in ['oily', 'minyak', 'berminyak', 'light', 'ringan', 'gel', 'water']):
            skin_types.append('Berminyak')
        if any(term in product_name for term in ['dry', 'kering', 'moisturizing', 'hydrating', 'cream']):
            skin_types.append('Kering')
        if any(term in product_name for term in ['sensitive', 'sensitif', 'calm', 'soothing', 'mineral']):
            skin_types.append('Sensitif')
        
        # Default jika tidak ada yang terdeteksi
        if not skin_types:
            skin_types = ['Normal', 'Kombinasi']
        
        # Masalah kulit
        concerns = []
        if any(term in product_name for term in ['acne', 'jerawat', 'blemish']):
            concerns.append('Jerawat')
        if any(term in product_name for term in ['bright', 'cerah', 'glow', 'white', 'putih']):
            concerns.append('Kulit Kusam')
        if any(term in product_name for term in ['aging', 'anti-aging', 'wrinkle']):
            concerns.append('Penuaan Dini')
        
        # Bahan utama
        ingredients = []
        if 'zinc' in product_name:
            ingredients.append('Zinc Oxide')
        if 'titanium' in product_name:
            ingredients.append('Titanium Dioxide')
        if 'chemical' in product_name:
            ingredients.append('Chemical Filters')
        if 'physical' in product_name or 'mineral' in product_name:
            ingredients.append('Physical Filters')
        if 'niacinamide' in product_name:
            ingredients.append('Niacinamide')
        if 'hyaluronic' in product_name:
            ingredients.append('Hyaluronic Acid')
        
        # Update data
        enhanced_data.at[idx, 'suitable_skin_types'] = ', '.join(skin_types)
        enhanced_data.at[idx, 'targets_skin_concerns'] = ', '.join(concerns) if concerns else None
        enhanced_data.at[idx, 'key_ingredients'] = ', '.join(ingredients) if ingredients else None
    
    # ----- Perawatan -----
    treatments = enhanced_data[enhanced_data['category'] == 'Perawatan']
    
    for idx, row in treatments.iterrows():
        product_name = row['product_name'].lower()
        
        # Jenis kulit
        skin_types = []
        if any(term in product_name for term in ['oily', 'minyak', 'berminyak', 'acne', 'jerawat']):
            skin_types.append('Berminyak')
        if any(term in product_name for term in ['dry', 'kering', 'moisturizing', 'hydrating']):
            skin_types.append('Kering')
        if any(term in product_name for term in ['sensitive', 'sensitif', 'calm', 'soothing']):
            skin_types.append('Sensitif')
        
        # Masalah kulit
        concerns = []
        if any(term in product_name for term in ['acne', 'jerawat', 'blemish', 'pimple']):
            concerns.append('Jerawat')
        if any(term in product_name for term in ['bright', 'cerah', 'glow', 'white', 'putih']):
            concerns.append('Kulit Kusam')
        if any(term in product_name for term in ['aging', 'anti-aging', 'wrinkle', 'keriput']):
            concerns.append('Penuaan Dini')
        if any(term in product_name for term in ['pigment', 'dark', 'spot', 'flek']):
            concerns.append('Hiperpigmentasi')
        if any(term in product_name for term in ['pore', 'pori']):
            concerns.append('Pori-pori Besar')
        if any(term in product_name for term in ['red', 'merah', 'calm', 'inflam']):
            concerns.append('Kemerahan')
        if any(term in product_name for term in ['texture', 'exfoliat', 'scrub', 'tekstur']):
            concerns.append('Tekstur Tidak Rata')
        
        # Bahan utama
        ingredients = []
        if 'salicylic' in product_name or 'bha' in product_name:
            ingredients.append('Salicylic Acid')
        if 'glycolic' in product_name or 'aha' in product_name:
            ingredients.append('Glycolic Acid')
        if 'retinol' in product_name or 'retin' in product_name:
            ingredients.append('Retinol')
        if 'vitamin c' in product_name or 'vit c' in product_name:
            ingredients.append('Vitamin C')
        if 'niacinamide' in product_name:
            ingredients.append('Niacinamide')
        if 'hyaluronic' in product_name or 'hyaluron' in product_name:
            ingredients.append('Hyaluronic Acid')
        if 'centella' in product_name or 'cica' in product_name:
            ingredients.append('Centella Asiatica')
        if 'peptide' in product_name:
            ingredients.append('Peptides')
        if 'tea tree' in product_name:
            ingredients.append('Tea Tree')
        
        # Update data
        enhanced_data.at[idx, 'suitable_skin_types'] = ', '.join(skin_types) if skin_types else 'Semua Jenis Kulit'
        enhanced_data.at[idx, 'targets_skin_concerns'] = ', '.join(concerns) if concerns else None
        enhanced_data.at[idx, 'key_ingredients'] = ', '.join(ingredients) if ingredients else None
    
    # ----- Masker -----
    masks = enhanced_data[enhanced_data['category'] == 'Masker']
    
    for idx, row in masks.iterrows():
        product_name = row['product_name'].lower()
        
        # Jenis kulit
        skin_types = []
        if any(term in product_name for term in ['oily', 'minyak', 'berminyak', 'clay', 'acne']):
            skin_types.append('Berminyak')
        if any(term in product_name for term in ['dry', 'kering', 'moisturizing', 'hydrating']):
            skin_types.append('Kering')
        if any(term in product_name for term in ['sensitive', 'sensitif', 'calm', 'soothing']):
            skin_types.append('Sensitif')
        
        # Default jika tidak ada yang terdeteksi
        if not skin_types:
            skin_types = ['Normal', 'Kombinasi']
        
        # Masalah kulit
        concerns = []
        if any(term in product_name for term in ['acne', 'jerawat', 'blemish']):
            concerns.append('Jerawat')
        if any(term in product_name for term in ['bright', 'cerah', 'glow', 'white']):
            concerns.append('Kulit Kusam')
        if any(term in product_name for term in ['aging', 'anti-aging', 'wrinkle']):
            concerns.append('Penuaan Dini')
        if any(term in product_name for term in ['pore', 'pori']):
            concerns.append('Pori-pori Besar')
        
        # Bahan utama
        ingredients = []
        if 'clay' in product_name or 'lempung' in product_name:
            ingredients.append('Clay')
        if 'mud' in product_name or 'lumpur' in product_name:
            ingredients.append('Mud')
        if 'charcoal' in product_name or 'arang' in product_name:
            ingredients.append('Charcoal')
        if 'sheet' in product_name:
            ingredients.append('Sheet Mask')
        
        # Update data
        enhanced_data.at[idx, 'suitable_skin_types'] = ', '.join(skin_types)
        enhanced_data.at[idx, 'targets_skin_concerns'] = ', '.join(concerns) if concerns else None
        enhanced_data.at[idx, 'key_ingredients'] = ', '.join(ingredients) if ingredients else None
    
    # Tambahkan atribut untuk produk yang belum tercakup
    null_skin_types = enhanced_data['suitable_skin_types'].isnull()
    enhanced_data.loc[null_skin_types, 'suitable_skin_types'] = 'Semua Jenis Kulit'
    
    return enhanced_data