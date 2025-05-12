import streamlit as st
import pandas as pd
import numpy as np
from config.constants import DATA_FILES, CSV_PARAMS
import re 
import plotly.graph_objects as go
from utils.data_enhancer import enhance_product_data

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


def clean_repurchase(x):
    """
    Membersihkan dan mengubah data pembelian ulang dari format 'Yes (87)' menjadi angka 87
    """
    try:
        if pd.isna(x) or str(x).lower() == 'null' or str(x).strip() == '':
            return 0
            
        # Ubah input ke string untuk memastikan
        nilai_str = str(x).strip()
        
        # Coba cari angka dalam kurung terlebih dahulu
        pola_kurung = re.search(r'\((\d+)\)', nilai_str)
        if pola_kurung:
            return int(pola_kurung.group(1))
        
        # Jika gagal, coba cari angka apapun
        angka = re.findall(r'\d+', nilai_str)
        if angka:
            return int(angka[0])
            
        # Jika Yes/No/Maybe tanpa angka, anggap 1
        if any(keyword in nilai_str.lower() for keyword in ['yes', 'no', 'maybe']):
            return 1
            
        return 0
        
    except Exception as e:
        print(f"Error dalam clean_repurchase untuk nilai '{x}': {str(e)}")
        return 0


def clean_data(df):
    """
    Membersihkan dan memproses DataFrame
    """
    try:
        # Print data awal
        print("\n=== Data Awal ===")
        print("Columns:", df.columns.tolist())
        print("\nData repurchase sebelum dibersihkan:")
        if 'repurchase_yes' in df.columns:
            print("\nSample repurchase_yes:", df['repurchase_yes'].head())
        if 'repurchase_no' in df.columns:
            print("\nSample repurchase_no:", df['repurchase_no'].head())
        if 'repurchase_maybe' in df.columns:
            print("\nSample repurchase_maybe:", df['repurchase_maybe'].head())

        # Bersihkan kolom string dasar
        string_columns = ['brand', 'product_name', 'category'] 
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace('null', '')

        # Simpan dan bersihkan harga
        if 'price' in df.columns:
            df['price_display'] = df['price'].astype(str)
            df['price_display'] = df['price_display'].apply(format_price)
            
            def extract_numeric_price(price_str):
                try:
                    price_str = str(price_str).replace('Rp', '').strip()
                    if '-' in price_str:
                        parts = price_str.split('-')
                        if len(parts) == 2:
                            low = float(''.join(c for c in parts[0] if c.isdigit() or c == '.'))
                            high = float(''.join(c for c in parts[1] if c.isdigit() or c == '.'))
                            return (low + high) / 2
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

        # Bersihkan number_of_reviews
        if 'number_of_reviews' in df.columns:
            df['number_of_reviews'] = df['number_of_reviews'].apply(clean_reviews)
            df['number_of_reviews'] = pd.to_numeric(df['number_of_reviews'], errors='coerce').fillna(0).astype(int)

        # Bersihkan repurchase columns

               # Bersihkan repurchase columns
        print("\nMembersihkan data repurchase...")
        repurchase_cols = ['repurchase_yes', 'repurchase_no', 'repurchase_maybe']
        for col in repurchase_cols:
            if col not in df.columns:
                print(f"Kolom {col} tidak ditemukan, membuat kolom baru")
                df[col] = 0
            else:
                print(f"\nMemproses {col}:")
                print("Sample data sebelum cleaning:")
                print(df[col].head())
                
                # Bersihkan data dengan menampilkan proses
                df[col] = df[col].apply(lambda x: print(f"Cleaning {x} -> {clean_repurchase(x)}") or clean_repurchase(x))
                
                # Pastikan tipe data integer
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                
                print("\nSample data setelah cleaning:")
                print(df[col].head())

        # Simpan data repurchase asli untuk debugging
        print("\nSample data final repurchase:")
        sample_data = df[['product_name'] + repurchase_cols].head()
        print(sample_data.to_string())

        # Perkaya data dengan atribut jenis kulit dan masalah kulit
        df = enhance_product_data(df)

        return df

    except Exception as e:
        print(f"Error dalam clean_data: {str(e)}")
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
                print(f"\nMembaca file: {file}")
                df = pd.read_csv(f'data/{file}', **CSV_PARAMS)
                df.columns = df.columns.str.strip()
                df['category'] = category
                print(f"Columns dalam {file}:", df.columns.tolist())
                dataframes[file] = df
                
            except Exception as e:
                st.error(f"Error membaca {file}: {str(e)}")
                print(f"Error lengkap membaca {file}: {str(e)}")
                continue

        if not dataframes:
            raise Exception("Tidak ada data yang bisa dimuat dari file manapun")

        # Gabung semua dataframe
        print("\nMenggabungkan dataframes...")
        all_data = pd.concat(dataframes.values(), ignore_index=True)
        
        # Bersihkan data
        print("\nMembersihkan data...")
        all_data = clean_data(all_data)

        return all_data

    except Exception as e:
        st.error(f"Error dalam load_data: {str(e)}")
        print(f"Error lengkap dalam load_data: {str(e)}")
        return None

        return None
