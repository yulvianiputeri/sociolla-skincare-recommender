import streamlit as st
import pandas as pd
import numpy as np
from config.constants import DATA_FILES, CSV_PARAMS
import re 
import plotly.graph_objects as go

def clean_reviews(review_str):
    """
    Membersihkan dan mengkonversi string review ke angka
    """
    try:
        if pd.isna(review_str) or str(review_str).lower() == 'null' or str(review_str).strip() == '':
            return 0
            
        review_str = str(review_str).strip()
        
        # Hapus tanda kurung jika ada
        review_str = review_str.replace('(', '').replace(')', '')
        
        # Jika ada 'k', konversi ke ribuan
        if 'k' in review_str.lower():
            # Hapus 'k' dan konversi ke float dulu
            num = float(review_str.lower().replace('k', '').replace(',', '.'))
            # Kalikan dengan 1000
            return int(num * 1000)
        
        # Jika format biasa, bersihkan dan konversi
        cleaned_str = ''.join(c for c in review_str if c.isdigit() or c in '.,')
        if cleaned_str:
            return int(float(cleaned_str.replace(',', '')))
        return 0
    except:
        return 0


def format_price(price_str):
    """
    Format harga ke format yang lebih rapi
    """
    try:
        if pd.isna(price_str):
            return "Harga tidak tersedia"
            
        # Bersihkan string harga
        price_str = str(price_str).strip()
        
        # Jika ada 'Rp' ganda, ini adalah range harga
        if price_str.count('Rp') > 1:
            # Split berdasarkan Rp dan bersihkan
            parts = [p.strip() for p in price_str.split('Rp') if p.strip()]
            if len(parts) >= 2:
                return f"Rp {parts[0].strip()} - Rp {parts[1].strip()}"
        
        # Jika tidak ada 'Rp'
        if 'Rp' not in price_str:
            # Cek apakah ada range dengan tanda -
            if '-' in price_str:
                low, high = price_str.split('-')
                return f"Rp {low.strip()} - Rp {high.strip()}"
            return f"Rp {price_str}"
            
        return price_str
    except:
        return price_str

def clean_data(df):
    """
    Membersihkan dan memproses DataFrame
    """
    try:
        # Bersihkan kolom string dasar
        string_columns = ['brand', 'product_name', 'category'] 
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace('null', '')

        # Simpan dan bersihkan harga
        if 'price' in df.columns:
            # Simpan format display original
            df['price_display'] = df['price'].astype(str)
            df['price_display'] = df['price_display'].apply(format_price)
            
            # Bersihkan nilai numerik untuk perhitungan
            def extract_numeric_price(price_str):
                try:
                    # Hapus 'Rp' dan karakter non-numerik
                    price_str = str(price_str).replace('Rp', '').strip()
                    if '-' in price_str:
                        # Jika range, ambil nilai tengah
                        parts = price_str.split('-')
                        if len(parts) == 2:
                            low = float(''.join(c for c in parts[0] if c.isdigit() or c == '.'))
                            high = float(''.join(c for c in parts[1] if c.isdigit() or c == '.'))
                            return (low + high) / 2
                    # Jika single price
                    return float(''.join(c for c in price_str if c.isdigit() or c == '.'))
                except:
                    return np.nan
                    
            df['price'] = df['price'].apply(extract_numeric_price)
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            median_price = df['price'].median()
            df['price'] = df['price'].fillna(median_price)

        # Bersihkan rating
        if 'rating' in df.columns:
            def clean_rating(x):
                if pd.isna(x) or str(x).lower() == 'null' or str(x).strip() == '':
                    return np.nan
                try:
                    cleaned = str(x).lstrip('0') or '0'
                    if '.' not in cleaned:
                        cleaned = f"{cleaned[0]}.{cleaned[1:]}"
                    return float(cleaned) 
                except:
                    return np.nan

            df['rating'] = df['rating'].apply(clean_rating)
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            median_rating = df['rating'].median()
            df['rating'] = df['rating'].fillna(median_rating)

        # Bersihkan number_of_reviews menggunakan fungsi global
        if 'number_of_reviews' in df.columns:
            df['number_of_reviews'] = df['number_of_reviews'].apply(clean_reviews)
            df['number_of_reviews'] = pd.to_numeric(df['number_of_reviews'], errors='coerce').fillna(0).astype(int)

        # Bersihkan repurchase columns
        repurchase_cols = ['repurchase_yes', 'repurchase_no', 'repurchase_maybe']
        for col in repurchase_cols:
            if col not in df.columns:
                df[col] = 0  # Buat kolom baru jika belum ada
            
            def clean_repurchase(x):
                try:
                    if pd.isna(x) or str(x).lower() == 'null':
                        return 0
                    if isinstance(x, str):
                        match = re.search(r'\((\d+)\)', x)
                        return int(match.group(1)) if match else 0
                    return int(abs(float(x)))
                except:
                    return 0
                
            df[col] = df[col].apply(clean_repurchase)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # Hitung repurchase rate
        total_repurchase = df['repurchase_yes'] + df['repurchase_no'] + df['repurchase_maybe']
        df['repurchase_rate'] = np.where(total_repurchase > 0,
                                        (df['repurchase_yes'] / total_repurchase) * 100,
                                        0)

        return df

    except Exception as e:
        st.error(f"Error dalam clean_data: {str(e)}")
        return df

@st.cache_data(ttl=3600)  
def load_data():
    """
    Memuat dan memproses data skincare dari file CSV
    """
    try:
        dataframes = {}

        # Muat setiap file CSV
        for file, category in DATA_FILES.items():
            try:
                # Baca file CSV
                df = pd.read_csv(f'data/{file}', **CSV_PARAMS)
                df.columns = df.columns.str.strip()
                df['category'] = category
                dataframes[file] = df
                
            except Exception as e:
                st.error(f"Error membaca {file}: {str(e)}")
                continue

        if not dataframes:
            raise Exception("Tidak ada data yang bisa dimuat dari file manapun")

        # Gabung semua dataframe
        all_data = pd.concat(dataframes.values(), ignore_index=True)
        
        # Bersihkan data
        all_data = clean_data(all_data)

        return all_data

    except Exception as e:
        st.error(f"Error dalam load_data: {str(e)}")
        return None