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
    </style>
    """, unsafe_allow_html=True)

# Fungsi pembantu untuk memformat angka menjadi Rupiah (Contoh: Rp110.499.000)
def format_rupiah(angka):
    if isinstance(angka, (int, float)):
        return f"Rp {angka:,.0f}".replace(",", ".")
    return angka

# 2. DATA DATABASE INTERNAL PRICELIST 2026 (Diperbaiki agar barisnya pecah ke bawah dengan rapi)
PRICELIST_PACKAGES = {
    "Exclude Venue & Catering": [
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
        {
            "Nama": "Before Wedding Services (Lamaran, Pengajian, Sangjit, etc.)", 
            "Harga": 6500000, 
            "Tamu": "Maximal 100 pax", 
            "Detail": [
                "**Team Kerja:** 1 Professional Project Leader + 3 Project Crew",
                "**Konsultasi:** Progress Meeting (3x), Technical Meeting (1x)",
                "**Logistik:** Transport (Jabodetabek), Guidance Book Included",
                "**Durasi Hari H:** 5 Hours Worktime on Wedding Day."
            ]
        },
        {
            "Nama": "Intimate Wedding (Akad Intimate / Resepsi Only)", 
            "Harga": 8000000, 
            "Tamu": "Maximal 200 pax", 
            "Detail": [
                "**Periode Kerja:** Worked closely for two months prior.",
                "**Team Kerja:** 1 Professional Wedding Manager + 4 Wedding Crew",
                "**Konsultasi:** Online Progress Meeting (3x), Offline Assist (2x), Technical Meeting (1x)",
                "**Logistik:** Snack & Transport (Jabodetabek), Guidance Book & Wedding Report",
                "**Durasi Hari H:** 6 Hours Worktime on Wedding Day."
            ]
        },
        {
            "Nama": "Full Wedding (Akad & Resepsi)", 
            "Harga": 10500000, 
            "Tamu": "Maximal 800 pax", 
            "Detail": [
                "**Periode Kerja:** Worked closely for two months prior.",
                "**Team Kerja:** 1 Professional Project Leader + 8 Project Crew",
                "**Konsultasi:** Online Progress Meeting (5x), Offline Assist (3x), Technical Meeting (1x)",
                "**Logistik:** Snack & Transport (Jabodetabek), Guidance Book Included",
                "**Durasi Hari H:** 8 Hours Worktime on Wedding Day."
            ]
        }
    ],
    "Wedding Planner Only": [
        {
            "Nama": "Full Wedding Planner Service", 
            "Harga": 36499000, 
            "Tamu": "Maximal 1000 pax", 
            "Detail": [
                "**Periode Kerja:** Worked closely for 6-7 months prior.",
                "**Preparation & Planning:** Progress Meeting by Online (3x), Assisting survey venue (3x), Assisting fitting attire (2x), Assisting concepting decor offline (1x), Assisting test food (2x).",
                "**Vendor & Dokumen:** Provide max 3 options for each vendor, Technical Meeting (1x), Guidance Book, Drafting Rundown, Project Timeline, Budget plan (RAB), Vendor management, Handling KUA administration, Unlimited consultation via WA, Snack TM.",
                "**On The Day Services:** 1 Professional Wedding Manager + 8 Wedding Manpower, 10 Hours Service, Wedding Report, Marriage Document Handling (KUA Jabodetabek City Only).",
                "**EXTRA BONUS:** 1 Night Stay at Four Season/Langham, 100 pax hype stall Teazzi."
            ]
        }
    ]
}

VENUE_PACKAGES = [
    {"Kota": "Jakarta", "Nama": "Pejaten Terrace", "100pax": 87799000, "200pax": 99499000, "300pax": 110499000, "Kapasitas": 300},
    {"Kota": "Jakarta", "Nama": "Griyo Kulo *", "100pax": 71799000, "200pax": 80799000, "300pax": 89799000, "Kapasitas": 500},
    {"Kota": "Jakarta", "Nama": "Aroem Mahakam *", "100pax": 93549000, "200pax": 118149000, "300pax": 142749000, "Kapasitas": 300},
    {"Kota": "Jakarta", "Nama": "Aleesha", "100pax": 88500000, "200pax": 98500000, "300pax": 108500000, "Kapasitas": 400},
    {"Kota": "Jakarta", "Nama": "Casakhasa", "100pax": 153799000, "200pax": 163799000, "300pax": 173799000, "Kapasitas": 400},
    {"Kota": "Depok", "Nama": "Tanavila", "100pax": 118799000, "200pax": 128799000, "300pax": 138799000, "Kapasitas": 500},
    {"Kota": "Depok", "Nama": "Rumah Keramik", "100pax": 122799000, "200pax": 132799000, "300pax": 142799000, "Kapasitas": 500},
    {"Kota": "Tangerang & Tangsel", "Nama": "Indy Bintaro (Indoor)", "100pax": 125439000, "200pax": 135439000, "300pax": 145439000, "Kapasitas": 300},
    {"Kota": "Tangerang & Tangsel", "Nama": "Aviary Bintaro *", "100pax": 154799000, "200pax": 154799000, "300pax": 191799000, "Kapasitas": 500}
]

# 3. INITIALIZE DATABASE CLIENT DI MEMORI APP
if 'client_db' not in st.session_state:
    st.session_state.client_db = [
        {
            "Nama Klien": "Klien Contoh (Pejaten 1)",
            "Pengantin Wanita": "Siti Aliyah",
            "Pengantin Pria": "Budi Santoso",
            "WhatsApp": "6281234567890",
            "Tanggal Pernikahan": "2026-10-12",
            "Kota": "Jakarta",
            "Estimasi Tamu": "300 pax",
            "Status Venue": "Belum Mencari Venue",
            "Nama Venue": "Pejaten Terrace",
            "Konsep": ["Modern"],
            "Budget": "100-200 Juta",
            "Layanan WO": ["Full Wedding Planning"],
            "Kendala": "Butuh rekomendasi venue All-In di daerah Jakarta Selatan."
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
                    # looping poin agar terpisah menjadi paragraf baru ke bawah
                    for sub_detail in item['Detail']:
                        st.markdown(sub_detail)
                        st.write("") # memberi jarak antar paragraf
                    
    with tab2:
        st.markdown("### 🏨 Daftar Venue & Harga Paket All-In (100 - 300 PAX)")
        st.caption("*Catatan: Tanda bintang (*) menunjukkan venue hotel/resto dengan catering in-house.")
        
        formatted_venues = []
        for v in VENUE_PACKAGES:
            formatted_venues.append({
                "Wilayah": v["Kota"],
                "Nama Venue / Hotel": v["Nama"],
                "Paket 100 Pax": format_rupiah(v["100pax"]),
                "Paket 200 Pax": format_rupiah(v["200pax"]),
                "Paket 300 Pax": format_rupiah(v["300pax"]),
                "Max Kapasitas": f"{v['Kapasitas']} pax"
            })
        df_venue = pd.DataFrame(formatted_venues)
        st.dataframe(df_venue, use_container_width=True, hide_index=True)

# ==================== MENU: INPUT KLIEN BARU ====================
elif menu == "➕ Input Klien Baru (Tanpa Excel)":
    st.subheader("📝 Form Masuk Klien Baru")
    with st.form("screening_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 👤 Biodata")
            nama_klien = st.text_input("Nama Label Klien *", placeholder="Contoh: Klien Pejaten - Rahma")
            p_wanita = st.text_input("Nama Pengantin Wanita")
            p_pria = st.text_input("Nama Pengantin Pria")
            wa_aktif = st.text_input("Nomor WhatsApp (Gunakan format 62...)")
            
            st.markdown("#### 📅 Logistik Acara")
            tgl_nikah = st.date_input("Rencana tanggal pernikahan", min_value=datetime.today())
            kota = st.selectbox("Wilayah / Kota Acara", ["Jakarta", "Depok", "Tangerang & Tangsel", "Lainnya"])
            tamu = st.selectbox("Estimasi Jumlah Undangan", ["100 pax", "200 pax", "300 pax", "400 pax", "500 pax"])
        with col2:
            st.markdown("#### 🏰 Preferensi Venue & Desain")
            venue_status = st.selectbox("Status Lokasi/Venue", ["Belum Mencari Venue", "Sudah Survey Beberapa Venue", "Sudah Booking Venue"])
            nama_venue = st.text_input("Nama Venue (Jika sudah ada)")
            konsep = st.multiselect("Konsep Acara", ["Modern", "Elegant", "Garden", "Intimate", "Traditional/Adat"])
            
            st.markdown("#### 💰 Komitmen Finansial")
            budget = st.selectbox("Kisaran Budget Anggaran", ["<100 Juta", "100-200 Juta", "200-300 Juta", "300-500 Juta", ">500 Juta"])
            layanan = st.multiselect("Layanan yang Dicari Klien", ["Full Wedding Planning", "Wedding Day Service", "Vendor Recommendation", "Venue Recommendation"])
            kendala = st.text_area("Kendala Terbesar Klien")
            
        submit_btn = st.form_submit_button("🚀 Simpan Data & Buat Analisis Rekomendasi")
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
    
    st.markdown("### 🤖 Rekomendasi Paket Otomatis dari 1 Destiny untuk Klien Ini:")
    
    tamu_clean = client_data['Estimasi Tamu'] 
    kota_klien = client_data['Kota']
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("#### 🏢 Pilihan Paket All-In (Include Venue & Catering)")
        match_found = False
        for v in VENUE_PACKAGES:
            if v["Kota"] == kota_klien:
                match_found = True
                key_pax = tamu_clean.replace(" ", "") 
                harga_paket = v.get(key_pax, None)
                
                if harga_paket:
                    st.markdown(f"⭐ **{v['Nama']} ({v['Kota']})**")
                    st.markdown(f"<div class='price-tag'>Harga Paket All-In: {format_rupiah(harga_paket)}</div>", unsafe_allow_html=True)
        if not match_found or "400" in tamu_clean or "500" in tamu_clean:
            st.write("_Paket venue All-In saat ini tersedia untuk opsi wilayah Jakarta/Depok/Tangerang skala 100-300 pax._")
            
    with col_rec2:
        st.markdown("#### 📦 Pilihan Paket Lepas (Exclude Venue & Catering)")
        if "100" in tamu_clean or "200" in tamu_clean or "300" in tamu_clean:
            st.markdown("**👉 Intimate Package (Up to 300 guests)**")
            st.markdown(f"<div class='price-tag'>Harga Paket: {format_rupiah(51699000)}</div>", unsafe_allow_html=True)
        else:
            st.markdown("**👉 Full Wedding Package (Up to 600 guests)**")
            st.markdown(f"<div class='price-tag'>Harga Paket: {format_rupiah(75999000)}</div>", unsafe_allow_html=True)
            
    st.markdown("---")
    st.subheader("💬 Auto-Brief Teks Siap Kirim ke WhatsApp Tim WO")
    
    konsep_str = ", ".join(client_data['Konsep']) if client_data['Konsep'] else "Belum Menentukan"
    layanan_str = ", ".join(client_data['Layanan WO']) if client_data['Layanan WO'] else "-"
    
    brief_text = f"""*BRIEF KLIEN BARU - 1 DESTINY*
====================================
• *Nama Pasangan*: {client_data['Pengantin Wanita']} & {client_data['Pengantin Pria']}
• *Tanggal Acara*: {client_data['Tanggal Pernikahan']}
• *Lokasi/Area*  : {client_data['Kota']}
• *Estimasi Tamu*: {client_data['Estimasi Tamu']}
• *Konsep Impian*: {konsep_str}
• *Range Budget* : {client_data['Budget']}
• *Layanan Dicari*: {layanan_str}

*⚠️ Kendala Utama Klien:*
"{client_data['Kendala'] if client_data['Kendala'] else '-'}"
====================================
_Dibuat otomatis oleh Wedding CRM Dashboard_"""
    st.code(brief_text, language="text")
