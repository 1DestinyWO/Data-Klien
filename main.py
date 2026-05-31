import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP HALAMAN
st.set_page_config(page_title="1 Destiny - Client Management Dashboard", layout="wide", page_icon="👰")

# Custom CSS Estetika & Format Tampilan Kardus Rekomendasi
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    div[data-testid="stMetricValue"] {font-size: 22px; color: #1E88E5;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px; width: 100%;}
    .price-tag { background-color: #E8F5E9; padding: 12px; border-left: 5px solid #2E7D32; font-weight: bold; font-size: 18px; color: #1B5E20; margin: 10px 0;}
    .detail-box { background-color: #F5F5F5; padding: 12px; border-radius: 6px; margin-top: 5px; font-size: 14px;}
    </style>
    """, unsafe_allow_html=True)

# Fungsi pembantu untuk memformat angka menjadi Rupiah (Contoh: Rp 110.499.000)
def format_rupiah(angka):
    if isinstance(angka, (int, float)):
        return f"Rp {angka:,.0f}".replace(",", ".")
    return str(angka)

# 2. DATA DATABASE INTERNAL PRICELIST 2026 (Lengkap 100 - 700 PAX & Detail)
PRICELIST_PACKAGES = {
    "Exclude Venue & Catering (Paket Lepas)": [
        {
            "Nama": "Intimate Package", 
            "Harga": 51699000, 
            "Tamu": "Up to 300 guests", 
            "Detail": [
                "**Wedding Organizer & Planner:**\nProgress Meeting (3x), Offline Assist (3x), Technical Meeting (1x), Guidance Book, Rundown, Timeline, Unlimited consultation via WA, Snack TM, Handling KUA administration.\n*Wo The Day:* 1 Professional Wedding Manager + 4 Crew on the Day (6-8 Hours Worktime).",
                "**Decoration:**\nBackdrop up to 5m, Karpet permadani Set, Meja Kursi Akad, Standing Flower 2 pcs, Welcome Sign Kotak, Ampau 1 pcs, Bench Sofa Pengantin 1 pcs, Aisle Decoration (Wedding Gate), FREE Buku Tamu 2 pcs.",
                "**Documentation:**\n1 Photographer, 1 Videographer, 1 Crew, 6 hours Photosession, Editing Photo, Video 3 s/d 5 Menit, All file On Flashdisk.",
                "**MC:**\nMC Akad/Pemberkatan - Resepsi (4-5 hours worktime, Free Transport).",
                "**MUA & Attire:**\nMakeup & Hairdo/Hijabdo Bride, Makeup Touch Up Groom, Makeup & Hairdo 2 Moms, Retouch Resepsi, Sepasang Baju Akad & Resepsi, 2 Baju Ayah & 2 Baju Ibu, FREE Fake Nail Art & Softlense Normal."
            ]
        },
        {
            "Nama": "Full Wedding Package", 
            "Harga": 75999000, 
            "Tamu": "Up to 600 guests", 
            "Detail": [
                "**Wedding Organizer & Planner:**\nProgress Meeting (3x), Offline Assist (3x), Technical Meeting (1x), Guidance Book, Rundown, Timeline, Unlimited consultation via WA, Snack TM, Handling KUA administration.\n*Wo The Day:* 1 Professional Wedding Manager + 5-6 Crew on the Day (8 Hours Worktime).",
                "**Decoration (Pelaminan 8m):**\n- *Pelaminan:* Sofa Pelaminan 1 set, Pelaminan 8m, Karpet permadani, Tanaman pelaminan.\n- *Area Masuk:* Welcome Sign, Kotak Ampau 2 pcs, Backdrop penerima tamu 2m, Pergola pintu masuk.\n- *Area Tengah:* Set Meja kursi akad, Karpet jalan, Standing flower 6 pcs, Bunga pikok jalur jalan 8 titik, Lampu bunga 2 set, Lampu crystal 2 set, Photo Gallery 3 pcs.",
                "**Documentation:**\n1 Photographer, 1 Videographer, 1 Crew, 8 hours Photosession, Editing Photo, Video 3 s/d 5 Menit, All file On Flashdisk.",
                "**Entertainment:**\n1 Singer & 1 Keyboardist (atau 1 Singer & 1 Guitarist), Sound system 2000 watt.",
                "**MC:**\nMC Akad/Pemberkatan - Resepsi (4-5 hours worktime, Free Transport).",
                "**MUA & Attire:**\nMakeup & Hairdo Bride + Touch Up Groom, Makeup & Hairdo 2 Moms, Retouch Resepsi, Sepasang Baju Akad & Resepsi, 2 Baju Ayah & 2 Baju Ibu, FREE Fake Nail Art & Softlense Normal."
            ]
        }
    ],
    "On The Day WO Services Only": [
        {"Nama": "Before Wedding Services (Lamaran, Pengajian, Sangjit, etc.)", "Harga": 6500000, "Tamu": "Maximal 100 pax", "Detail": ["**Team Kerja:** 1 PL + 3 Crew", "**Konsultasi:** Progress Meeting (3x), TM (1x)", "**Hari H:** 5 Hours Worktime."]},
        {"Nama": "Intimate Wedding (Akad Intimate / Resepsi Only)", "Harga": 8000000, "Tamu": "Maximal 200 pax", "Detail": ["**Team Kerja:** 1 Wedding Manager + 4 Crew", "**Konsultasi:** Online Progress (3x), Offline Assist (2x), TM (1x)", "**Hari H:** 6 Hours Worktime."]},
        {"Nama": "Full Wedding (Akad & Resepsi)", "Harga": 10500000, "Tamu": "Maximal 800 pax", "Detail": ["**Team Kerja:** 1 Project Leader + 8 Crew", "**Konsultasi:** Online Progress (5x), Offline Assist (3x), TM (1x)", "**Hari H:** 8 Hours Worktime."]}
    ]
}

# DATABASE DETAIL BENEFIT PAKET ALL IN (100-300 Pax vs 400-700 Pax)
DETAIL_ALLIN_SMALL = """
• **Catering (Blessing Catering):** Nasi Putih, Nasi Goreng (Daging Asap/Thailand/Kari/Pandan), Sop/Soto (Kimlo/Ayam Kembang Tahu/Baso Lohua/Soto Ayam), Ayam (Lada Hitam/Kungpao/Saus Padang), Daging (Teriyaki/Lada Hitam/Yakiniku/Cabe Ijo), Sayur, Kerupuk, Dessert & Beverages, Gubukan/Stall. (>=300 Pax Free Makanan Akad)
• **Decoration:** Backdrop up to 6m, Karpet permadani Set, Meja Kursi Akad, Standing Flower 2 pcs, Welcome Sign, Ampau 1 pcs, Bench Sofa Pengantin, Wedding Gate, Free Buku Tamu 2 pcs.
• **MUA & Attire:** Makeup & Hairdo Bride + Touch Up Groom, Makeup & Hairdo 2 Moms, Retouch Resepsi, Sepasang Baju Akad & Resepsi, 2 Baju Ayah & Ibu, Free Fake Nail & Softlense.
• **Documentation:** 1 Photographer, 1 Videographer, 1 Crew, 8 hours Photosession, Editing Photo, Video 3-5 Menit, All file On Flashdisk.
• **WO & MC:** Progress Meeting (3x), Offline Assist (3x), TM (1x), Guidance Book, Rundown, Timeline. Hari H: 1 Manager + 4 Crew (8 Hours Worktime), MC Akad & Resepsi, Free Transport.
• **Limited Promo:** Digital Invitation + Free pengurusan dokumen KUA.
"""

DETAIL_ALLIN_MEDIUM = """
• **Catering (Blessing Catering):** Nasi Putih, Nasi Goreng Pilihan, Sop/Soto Pilihan, Ayam Pilihan, Daging Pilihan (Teriyaki/Lada Hitam/Yakiniku/Cabe Ijo), Sayur/Pendamping (Cah Brokoli/Sapo Tahu/Asinan/Mie/Soun), Kerupuk, Dessert, Beverages, & Gubukan/Stall. (>=300 Pax Free Makanan Akad)
• **Decoration (Pelaminan Premium 8m):** Sofa Pelaminan 1 set, Pelaminan 8m, Tanaman pelaminan, Karpet permadani. Area Masuk: Welcome Sign, Pergola Pintu Masuk, Kotak Ampau 2 pcs, Backdrop Penerima Tamu 2m, Backdrop Simple Entertainment. Area Tengah: Set Meja Kursi Akad, Karpet Jalan, Standing Flower 6 pcs, Bunga Pikok Jalur Jalan 16 Titik, Lampu Bunga 2 set, Lampu Crystal 2 set, Gazebo 1 pcs, Photo Gallery 3 pcs.
• **MUA & Attire (Premium):** Baju Akad & Resepsi Premium Pasangan, 2 Baju Ibu & Ayah Premium, Makeup Bride + Touch Up Groom, Makeup 2 Moms, Retouch Resepsi, Free Nail Art & Softlense.
• **Documentation (Premium):** 2 Photographer, 1 Videographer, 8 hours Photosession, Editing Photo, Video 3-5 Menit, Video Teaser, All file On Flashdisk, Free Album.
• **Entertainment:** by Soulbeat Entertainment (1 Singer & 1 Keyboardist/Guitarist + Sound System 2000 watt).
• **WO & MC:** Progress Meeting (3x), Offline Assist (3x), TM (1x), Guidance Book, Rundown, Timeline. Hari H: 1 Manager + 6-7 Crew (8 Hours Worktime), MC Akad & Resepsi, Free Transport.
• **Limited Promo:** Digital Invitation + Free pengurusan dokumen KUA.
"""

# DATABASE HARGA VENUE ALL IN (100-300 Pax & Tambahan 400-700 Pax)
VENUE_PACKAGES = [
    # Data Skala Kecil 100 - 300 Pax (Halaman 3)
    {"Kota": "Jakarta", "Nama": "Pejaten Terrace", "Prices": {"100pax": 87799000, "200pax": 99499000, "300pax": 110499000}, "Kapasitas": 300, "Tipe": "Small"},
    {"Kota": "Jakarta", "Nama": "Griyo Kulo *", "Prices": {"100pax": 71799000, "200pax": 80799000, "300pax": 89799000}, "Kapasitas": 500, "Tipe": "Small"},
    {"Kota": "Jakarta", "Nama": "Aroem Mahakam *", "Prices": {"100pax": 93549000, "200pax": 118149000, "300pax": 142749000}, "Kapasitas": 300, "Tipe": "Small"},
    {"Kota": "Jakarta", "Nama": "Aleesha", "Prices": {"100pax": 88500000, "200pax": 98500000, "300pax": 108500000}, "Kapasitas": 400, "Tipe": "Small"},
    {"Kota": "Jakarta", "Nama": "Casakhasa", "Prices": {"100pax": 153799000, "200pax": 163799000, "300pax": 173799000}, "Kapasitas": 400, "Tipe": "Small"},
    {"Kota": "Jakarta", "Nama": "Aroem Jakarta *", "Prices": {"100pax": 93549000, "200pax": 118149000, "300pax": 142749000}, "Kapasitas": 500, "Tipe": "Small"},
    {"Kota": "Jakarta", "Nama": "Pelindo (Indoor)", "Prices": {"100pax": 118799000, "200pax": 128799000, "300pax": 138799000}, "Kapasitas": 300, "Tipe": "Small"},
    {"Kota": "Jakarta", "Nama": "Heritage Garden", "Prices": {"100pax": 133799000, "200pax": 143799000, "300pax": 153799000}, "Kapasitas": 500, "Tipe": "Small"},
    {"Kota": "Depok", "Nama": "Tanavila", "Prices": {"100pax": 118799000, "200pax": 128799000, "300pax": 138799000}, "Kapasitas": 500, "Tipe": "Small"},
    {"Kota": "Depok", "Nama": "Rumah Keramik", "Prices": {"100pax": 122799000, "200pax": 132799000, "300pax": 142799000}, "Kapasitas": 500, "Tipe": "Small"},
    {"Kota": "Tangerang & Tangsel", "Nama": "Indy Bintaro (Indoor)", "Prices": {"200pax": 125439000, "300pax": 145439000}, "Kapasitas": 300, "Tipe": "Small"},
    {"Kota": "Tangerang & Tangsel", "Nama": "Aviary Bintaro *", "Prices": {"200pax": 154799000, "300pax": 191799000}, "Kapasitas": 500, "Tipe": "Small"},
    
    # Data Skala Medium 400 - 700 Pax (Halaman 8)
    {"Kota": "Jakarta", "Nama": "D'Hall Kementerian Pertanian", "Prices": {"400pax": 163799000, "500pax": 173799000, "600pax": 183799000, "700pax": 193799000}, "Kapasitas": 700, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Soho Pancoran Ballroom", "Prices": {"400pax": 173799000, "500pax": 183799000, "600pax": 193799000, "700pax": 203799000}, "Kapasitas": 700, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Aminta Hall", "Prices": {"400pax": 174200000, "500pax": 185200000, "600pax": 196200000, "700pax": 206200000}, "Kapasitas": 700, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Felfest UI", "Prices": {"400pax": 190799000, "500pax": 200799000, "600pax": 210799000, "700pax": 220799000}, "Kapasitas": 800, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Taman Kajoe", "Prices": {"400pax": 209799000, "500pax": 222799000, "600pax": 235799000, "700pax": 248799000}, "Kapasitas": 1000, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "SQ Dome", "Prices": {"400pax": 189300000, "500pax": 202300000, "600pax": 215300000, "700pax": 228300000}, "Kapasitas": 800, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "BRIN Lebak Bulus", "Prices": {"400pax": 173799000, "500pax": 183799000, "600pax": 193799000, "700pax": 203799000}, "Kapasitas": 800, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Calathea Lutea", "Prices": {"400pax": 192799000, "500pax": 202799000, "600pax": 212799000, "700pax": 222799000}, "Kapasitas": 800, "Tipe": "Medium"}
]

# 3. INITIALIZE DATABASE CLIENT DI MEMORI APP
if 'client_db' not in st.session_state:
    st.session_state.client_db = [
        {
            "Nama Klien": "Klien Contoh (Medium 500 Pax)",
            "Pengantin Wanita": "Rania Amanda",
            "Pengantin Pria": "Dimas Pratama",
            "WhatsApp": "628998888777",
            "Tanggal Pernikahan": "2026-11-21",
            "Kota": "Jakarta",
            "Estimasi Tamu": "500 pax",
            "Status Venue": "Belum Mencari Venue",
            "Nama Venue": "",
            "Konsep": ["Elegant", "Traditional/Adat"],
            "Budget": "200-300 Juta",
            "Layanan WO": ["Full Wedding Planning"],
            "Kendala": "Mencari ballroom kapasitas besar daerah Jakarta Selatan yang sepaket dengan katering."
        }
    ]

# 4. STRUKTUR MENU UTAMA
st.sidebar.title("1 Destiny WO 2026")
menu = st.sidebar.radio("Navigasi Konten:", [
    "📋 Lihat Summary Kebutuhan Klien", 
    "➕ Input Klien Baru (Tanpa Excel)", 
    "💰 Lihat Price List Resmi 2026"
])

# ==================== MENU: LIHAT PRICELIST RESMI ====================
if menu == "💰 Lihat Price List Resmi 2026":
    st
