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
    st.subheader("📑 Katalog & Price List Resmi 1 Destiny (2026)")
    
    tab1, tab2 = st.tabs(["📦 Paket Lepas Venue (Exclude)", "🏢 Paket All-In (Include Venue & Catering)"])
    
    with tab1:
        for kategori, item_list in PRICELIST_PACKAGES.items():
            st.markdown(f"### 🔹 {kategori}")
            for item in item_list:
                with st.expander(f"{item['Nama']} — {format_rupiah(item['Harga'])}"):
                    st.write(f"**Kapasitas:** {item['Tamu']}")
                    st.markdown("**Detail Paket Resmi:**")
                    for sub_detail in item['Detail']:
                        st.markdown(sub_detail)
                        st.write("")
                    
    with tab2:
        st.markdown("### 🏢 Matriks Paket All-In (Venue + Catering Blessing)")
        
        # Grid Tabel Rapi untuk All-In
        rows = []
        for v in VENUE_PACKAGES:
            rows.append({
                "Wilayah": v["Kota"],
                "Nama Venue": v["Nama"],
                "100 Pax": format_rupiah(v["Prices"].get("100pax", "-")),
                "200 Pax": format_rupiah(v["Prices"].get("200pax", "-")),
                "300 Pax": format_rupiah(v["Prices"].get("300pax", "-")),
                "400 Pax": format_rupiah(v["Prices"].get("400pax", "-")),
                "500 Pax": format_rupiah(v["Prices"].get("500pax", "-")),
                "600 Pax": format_rupiah(v["Prices"].get("600pax", "-")),
                "700 Pax": format_rupiah(v["Prices"].get("700pax", "-")),
                "Max Kapasitas": f"{v['Kapasitas']} pax"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ==================== MENU: INPUT KLIEN BARU ====================
elif menu == "➕ Input Klien Baru (Tanpa Excel)":
    st.subheader("📝 Form Masuk Klien Baru")
    with st.form("screening_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 👤 Biodata")
            nama_klien = st.text_input("Nama Label Klien *", placeholder="Contoh: Klien Pancoran - Rania")
            p_wanita = st.text_input("Nama Pengantin Wanita")
            p_pria = st.text_input("Nama Pengantin Pria")
            wa_aktif = st.text_input("Nomor WhatsApp (Gunakan format 62...)")
            
            st.markdown("#### 📅 Logistik Acara")
            tgl_nikah = st.date_input("Rencana tanggal pernikahan", min_value=datetime.today())
            kota = st.selectbox("Wilayah / Kota Acara", ["Jakarta", "Depok", "Tangerang & Tangsel"])
            tamu = st.selectbox("Estimasi Jumlah Undangan", ["100 pax", "200 pax", "300 pax", "400 pax", "500 pax", "600 pax", "700 pax"])
        with col2:
            st.markdown("#### 🏰 Preferensi Venue & Desain")
            venue_status = st.selectbox("Status Lokasi/Venue", ["Belum Mencari Venue", "Sudah Survey Beberapa Venue", "Sudah Booking Venue"])
            nama_venue = st.text_input("Nama Venue (Jika sudah ada)")
            konsep = st.multiselect("Konsep Acara", ["Modern", "Elegant", "Garden", "Intimate", "Traditional/Adat"])
            
            st.markdown("#### 💰 Komitmen Finansial")
            budget = st.selectbox("Kisaran Budget Anggaran", ["<100 Juta", "100-200 Juta", "200-300 Juta", "300-500 Juta", ">500 Juta"])
            layanan = st.multiselect("Layanan yang Dicari Klien", ["Full Wedding Planning", "Wedding Day Service", "Vendor Recommendation", "Venue Recommendation"])
            kendala = st.text_area("Kendala Terbesar Klien")
            
        submit_btn = st.form_submit_button("🚀 Simpan Data Klien")
        if submit_btn and nama_klien:
            new_data = {
                "Nama Klien": nama_klien, "Pengantin Wanita": p_wanita, "Pengantin Pria": p_pria,
                "WhatsApp": wa_aktif, "Tanggal Pernikahan": str(tgl_nikah), "Kota": kota,
                "Estimasi Tamu": tamu, "Status Venue": venue_status, "Nama Venue": nama_venue,
                "Konsep": konsep, "Budget": budget, "Layanan WO": layanan, "Kendala": kendala
            }
            st.session_state.client_db.append(new_data)
            st.success(f"🎉 Sukses menyimpan data {nama_klien}!")

# ==================== MENU: LIHAT SUMMARY KEBUTUHAN KLIEN ====================
else:
    client_list = [c["Nama Klien"] for c in st.session_state.client_db]
    selected_client_name = st.sidebar.selectbox("Pilih Klien untuk Ditampilkan:", client_list)
    client_data = next(c for c in st.session_state.client_db if c["Nama Klien"] == selected_client_name)
    
    st.subheader(f"📋 Client Needs Summary: {client_data['Nama Klien']}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("👤 **Profil Pasangan**")
        st.write(f"• **Wanita:** {client_data['Pengantin Wanita']}")
        st.write(f"• **Pria:** {client_data['Pengantin Pria']}")
        st.write(f"• **WhatsApp:** {client_data['WhatsApp']}")
    with c2:
        st.success("📅 **Rencana Logistik**")
        st.write(f"• **Tanggal:** {client_data['Tanggal Pernikahan']}")
        st.write(f"• **Kota:** {client_data['Kota']}")
        st.write(f"• **Tamu:** {client_data['Estimasi Tamu']}")
    with c3:
        st.warning("💰 **Ekspektasi Budget**")
        st.write(f"• **Budget Klien:** {client_data['Budget']}")
        st.write(f"• **Layanan Dicari:** {', '.join(client_data['Layanan WO'])}")
        
    st.markdown("---")
    
    # 🤖 CORE ENGINE PERBAIKAN: AUTO RECOMENDER & DETAIL EMIT
    st.markdown("### 🤖 Rekomendasi Paket Otomatis Berdasarkan Jumlah Tamu:")
    
    tamu_clean = client_data['Estimasi Tamu']  # Contoh: "500 pax"
    key_pax = tamu_clean.replace(" ", "")      # Mengubah menjadi "500pax"
    kota_klien = client_data['Kota']
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("#### 🏢 Rekomendasi Paket All-In (Include Venue & Catering)")
        match_found = False
        
        for v in VENUE_PACKAGES:
            if v["Kota"] == kota_klien and key_pax in v["Prices"]:
                match_found = True
                harga_paket = v["Prices"][key_pax]
                
                st.markdown(f"⭐ **{v['Nama']} ({v['Kota']})**")
                st.markdown(f"<div class='price-tag'>Harga All-In untuk {tamu_clean}: {format_rupiah(harga_paket)}</div>", unsafe_allow_html=True)
                
                # Tampilkan detail isi paket secara dinamis sesuai skalanya
                with st.expander(f"👁️ Lihat Detail Spesifikasi Paket {v['Nama']}"):
                    if v["Tipe"] == "Medium":
                        st.markdown("**💎 Detail Keuntungan Paket Medium Scale (400-700 Pax):**")
                        st.markdown(DETAIL_ALLIN_MEDIUM)
                    else:
                        st.markdown("**✨ Detail Keuntungan Paket Intimate Scale (100-300 Pax):**")
                        st.markdown(DETAIL_ALLIN_SMALL)
                        
        if not match_found:
            st.write(f"_Tidak ada data venue All-In resmi di file brosur yang cocok untuk wilayah {kota_klien} dengan kapasitas {tamu_clean}._")
            
    with col_rec2:
        st.markdown("#### 📦 Rekomendasi Paket Lepas (Exclude Venue & Catering)")
        # Deteksi otomatis skala paket lepas
        is_intimate = any(x in tamu_clean for x in ["100", "200", "300"])
        
        if is_intimate:
            st.markdown("**👉 Intimate Package (Up to 300 guests)**")
            st.markdown(f"<div class='price-tag'>Harga Paket: {format_rupiah(51699000)}</div>", unsafe_allow_html=True)
            with st.expander("👁️ Lihat Detail Spesifikasi Intimate Package"):
                for sub in PRICELIST_PACKAGES["Exclude Venue & Catering (Paket Lepas)"][0]["Detail"]:
                    st.markdown(sub)
        else:
            st.markdown("**👉 Full Wedding Package (Up to 600 guests)**")
            st.markdown(f"<div class='price-tag'>Harga Paket: {format_rupiah(75999000)}</div>", unsafe_allow_html=True)
            with st.expander("👁️ Lihat Detail Spesifikasi Full Wedding Package"):
                for sub in PRICELIST_PACKAGES["Exclude Venue & Catering (Paket Lepas)"][1]["Detail"]:
                    st.markdown(sub)
            
    st.markdown("---")
    st.subheader("💬 Auto-Brief Teks Siap Kirim ke WhatsApp Tim WO")
    konsep_str = ", ".join(client_data['Konsep']) if client_data['Konsep'] else "Belum Menentukan"
    layanan_str = ", ".join(client_data['Layanan WO']) if client_data['Layanan WO'] else "-"
    
    brief_text = f"""*BRIEF KLIEN BARU - 1 DESTINY*
====================================
• *Nama Pasangan*: {client_data['Pengantin Wanita']} & {client_data['Pengantin Pria']}
• *Tanggal Acara*: {client_data['Tanggal Pernikahan']}
• *Lokasi/Area* : {client_data['Kota']}
• *Estimasi Tamu*: {client_data['Estimasi Tamu']}
• *Konsep Impian*: {konsep_str}
• *Range Budget* : {client_data['Budget']}
• *Layanan Dicari*: {layanan_str}

*⚠️ Kendala Utama Klien:*
"{client_data['Kendala'] if client_data['Kendala'] else '-'}"
====================================
_Dibuat otomatis oleh Wedding CRM Dashboard_"""
    st.code(brief_text, language="text")
