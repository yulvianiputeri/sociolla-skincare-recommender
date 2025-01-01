# Definisi kategori produk
PRODUCT_CATEGORIES = {
    "Pembersih Wajah": {
        "icon": "🧼",
        "description": "Produk untuk membersihkan wajah dari kotoran, minyak, dan makeup",
        "benefits": [
            "Mengangkat kotoran dan minyak berlebih",
            "Membersihkan sisa makeup",
            "Menjaga pH kulit tetap seimbang",
            "Membantu mencegah jerawat"
        ]
    },
    "Masker": {
        "icon": "🎭",
        "description": "Perawatan intensif untuk berbagai masalah kulit",
        "benefits": [
            "Memberikan nutrisi pada kulit",
            "Mengangkat sel kulit mati",
            "Mencerahkan dan melembutkan kulit",
            "Mengecilkan pori-pori"
        ]
    },
    "Pelembab": {
        "icon": "💧",
        "description": "Menjaga kelembaban dan kesehatan kulit",
        "benefits": [
            "Melembabkan kulit secara optimal",
            "Mencegah kulit kering dan kusam",
            "Menjaga elastisitas kulit",
            "Memperkuat skin barrier"
        ]
    },
    "Sunscreen": {
        "icon": "☀️",
        "description": "Perlindungan kulit dari sinar UV berbahaya",
        "benefits": [
            "Melindungi dari UVA dan UVB",
            "Mencegah hyperpigmentasi",
            "Mengurangi risiko kanker kulit",
            "Mencegah penuaan dini"
        ]
    },
    "Perawatan": {
        "icon": "✨",
        "description": "Produk treatment untuk masalah kulit spesifik",
        "benefits": [
            "Mencerahkan noda hitam",
            "Mengatasi jerawat dan bekasnya",
            "Menghaluskan tekstur kulit",
            "Mengurangi tanda penuaan"
        ]
    }
}
# File paths
DATA_FILES = {
    'skincare_cleanser.csv': 'Pembersih Wajah',
    'skincare_mask.csv': 'Masker',
    'skincare_moisturizer.csv': 'Pelembab',
    'skincare_suncare.csv': 'Sunscreen',
    'skincare_treatment.csv': 'Perawatan'
}

# CSV parameters
CSV_PARAMS = {
    'encoding': 'utf-8',
    'sep': ';',
    'on_bad_lines': 'skip',
    'low_memory': False
}