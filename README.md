# sociolla-skincare-recommender

# Sistem Rekomendasi Skincare Menggunakan Metode Hybrid Filtering pada Ecommerce Sociolla

Aplikasi rekomendasi skincare berbasis web yang menggunakan pendekatan hybrid filtering untuk memberikan rekomendasi produk skincare yang personal dan relevan dari platform Sociolla.

## 🌟 Fitur Utama

- **Jelajahi Produk** - Filter dan cari produk skincare berdasarkan kategori, brand, dan harga
- **Rekomendasi Cerdas** - Dapatkan rekomendasi produk serupa berdasarkan teknologi machine learning
- **Analisis Data** - Visualisasi data dan insight tentang tren produk skincare
- **Preferensi Personal** - Tentukan jenis kulit dan permasalahan kulit untuk rekomendasi yang lebih personal

## 🧠 Teknologi Machine Learning

Aplikasi ini menggunakan pendekatan **hybrid recommendation system** yang mengkombinasikan:

1. **Content-Based Filtering (40% bobot)** - Merekomendasikan produk berdasarkan karakteristik dan fitur produk
2. **Similarity-Based Filtering (60% bobot)** - Merekomendasikan produk berdasarkan rating dan popularitas
3. **Preference-Based Personalization** - Menyesuaikan rekomendasi berdasarkan jenis kulit dan kebutuhan pengguna

## 📊 Tampilan Aplikasi

Aplikasi web ini terdiri dari beberapa halaman utama:

- **Home Page** - Halaman utama dengan pengenalan dan preferensi pengguna
- **Explore Page** - Untuk mencari dan filter produk
- **Recommendation Page** - Untuk mendapatkan rekomendasi produk
- **Analysis Page** - Untuk melihat analisis data dan insight

## 🧬 Personalisasi Preferensi

Fitur personalisasi preferensi memungkinkan pengguna untuk:

- Memilih jenis kulit (Normal, Kering, Berminyak, dll)
- Memilih permasalahan kulit (Jerawat, Penuaan Dini, dll)
- Memilih bahan yang disukai (Niacinamide, Hyaluronic Acid, dll)
- Memilih bahan yang dihindari (Alcohol, Fragrance, dll)

Algoritma kami akan memberikan bobot tambahan pada produk berdasarkan:
- Kesesuaian dengan jenis kulit (30% bobot preferensi)
- Mengatasi masalah kulit yang dipilih (15% bobot per masalah)
- Mengandung bahan yang disukai (10% bobot per bahan)
- Tidak mengandung bahan yang dihindari (filter)

## 🗂️ Struktur Proyek

```
sociolla-skincare-recommender/
├── app.py                    # Aplikasi utama (alternatif)
├── Home.py                   # Halaman utama (main entry point)
├── requirements.txt          # Dependensi package
├── README.md                 # Dokumentasi proyek
├── config/
│   └── constants.py          # Konstanta dan konfigurasi
├── data/
│   ├── skincare_cleanser.csv
│   ├── skincare_mask.csv
│   ├── skincare_moisturizer.csv
│   ├── skincare_suncare.csv
│   └── skincare_treatment.csv
├── pages/
│   ├── __init__.py
│   ├── 1_🔍_Explore_Page.py
│   ├── 2_💫_Recommendation_Page.py
│   └── 3_📊_Analysis_Page.py
└── utils/
    ├── __init__.py
    ├── charts.py             # Fungsi visualisasi data
    ├── data_loader.py        # Fungsi loading dan processing data
    ├── data_enhancer.py      # Pengayaan data produk
    ├── display.py            # Fungsi tampilan UI
    ├── recommender.py        # Algoritma rekomendasi
    └── user_preferences.py   # Pengelolaan preferensi pengguna
```

## 📦 Cara Instalasi

1. Clone repository:
```bash
git clone https://github.com/yourusername/sociolla-skincare-recommender.git
cd sociolla-skincare-recommender
```

2. Buat virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # untuk Linux/Mac
# atau
venv\Scripts\activate  # untuk Windows
```

3. Install dependensi:
```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi:
```bash
streamlit run Home.py
```

## 🚀 Teknologi yang Digunakan

- **Streamlit** - Framework aplikasi web
- **Pandas & NumPy** - Manipulasi dan analisis data
- **Scikit-learn** - Algoritma machine learning
- **Plotly** - Visualisasi data interaktif

## 📝 Catatan Pengembangan

Proyek ini menunjukkan evolusi dari pendekatan Item-Based Collaborative Filtering menjadi Hybrid Filtering untuk meningkatkan kualitas rekomendasi. Komponen utama dalam sistem baru ini:

- Content-Based Filtering: Menganalisis kesamaan fitur produk (kategori, brand)
- Similarity-Based Filtering: Menganalisis rating dan jumlah review
- Pendekatan hybrid memberikan rekomendasi yang lebih komprehensif dan akurat
- Penambahan fitur personalisasi preferensi pengguna untuk rekomendasi yang lebih relevan

## 📄 Lisensi

Proyek ini dilisensikan di bawah lisensi MIT - lihat file [LICENSE](LICENSE) untuk detail.
