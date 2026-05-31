import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP HALAMAN
st.set_page_config(page_title="1 Destiny - Client Management Dashboard", layout="wide", page_icon="👰")

# Custom CSS Estetika
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    div[data-testid="stMetricValue"] {font-size: 22px; color: #1E88E5;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px; width: 100%;}
    .price-tag { background-color: #E8F5E9; padding: 12px; border-left: 5px solid #2E7D32; font-weight: bold; font-size: 18px; color: #1B5E20; margin: 10px 0;}
    </style>
    """, unsafe_allow_html=True)

# Fungsi pembantu untuk memformat angka menjadi Rupiah
def format_rupiah(angka):
    if isinstance(angka, (int, float)):
        return f"Rp {angka:,.0f}".replace(",", ".")
    return str(angka)

# 2. DATA DATABASE INTERNAL PRICELIST 2026
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
    ]
}

DETAIL_ALLIN_SMALL = """• **Catering (Blessing Catering)**\n• **Decoration Backdrop/Pelaminan**\n• **MUA & Attire Pasangan + Orang Tua**\n• **Documentation 8 Hours Photosession**\n• **WO & MC On Day (1 Manager + 4 Crew)**"""
DETAIL_ALLIN_MEDIUM = """• **Catering Premium (Blessing Catering)**\n• **Decoration Pelaminan Premium 8m + Gazebo**\n• **MUA & Attire Premium Set**\n• **Documentation 2 Photo + 1 Video + Teaser + Album**\n• **Entertainment Live Acoustic by Soulbeat**\n• **WO & MC Full Team (1 Manager + 6-7 Crew)**"""

VENUE_PACKAGES = [
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
    {"Kota": "Jakarta", "Nama": "D'Hall Kementerian Pertanian", "Prices": {"400pax": 163799000, "500pax": 173799000}, "Kapasitas": 700, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Soho Pancoran Ballroom", "Prices": {"400pax": 173799000, "500pax": 183799000}, "Kapasitas": 700, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Aminta Hall", "Prices": {"400pax": 174200000, "500pax": 185200000}, "Kapasitas": 700, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Felfest UI", "Prices": {"400pax": 190799000, "500pax": 200799000}, "Kapasitas": 800, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Taman Kajoe", "Prices": {"400pax": 209799000, "500pax": 222799000}, "Kapasitas": 1000, "Tipe": "Medium"}
]

# 3. INITIALIZE DATABASE CLIENT DI MEMORI APP
if 'client_db' not in st.session_state:
    st.session_state.client_db = [
        {
            "Nama Klien": "Skrining - Siti & Budi",
            "Pengantin Wanita": "Siti Aliyah",
            "Pengantin Pria": "Budi Santoso",
            "WhatsApp": "6281234567890",
            "Email": "siti.budi@email.com",
            "Instagram": "@siti_aliyah",
            "Tanggal Pernikahan": "2026-12-12",
            "Kota": "Jakarta",
            "Jenis Acara": "Akad Nikah - Resepsi",
            "Estimasi Tamu": "300",
            "Venue Status": "Sudah Survey Beberapa Venue",
            "Nama Venue": "Pejaten Terrace",
            "Preference Venue": "Semi Outdoor",
            "Notes": "Butuh dekorasi bunga hidup dominan putih."
        }
    ]

# 4. STRUKTUR MENU DASHBOARD
st.sidebar.title("1 Destiny WO 2026")
menu = st.sidebar.radio("Navigasi Konten:", [
    "📋 Lihat Summary Kebutuhan Klien", 
    "➕ Input Klien Baru (Form Skrining Baru)", 
    "💰 Lihat Price List Resmi 2026"
])

# ==================== MENU 1: FORM SKRINING BARU (SESUAI SCREENSHOT) ====================
if menu == "➕ Input Klien Baru (Form Skrining Baru)":
    st.subheader("📝 Form Skrining Klien Baru")
    st.info("Nama Label Klien akan dibuat otomatis setelah Nama Pengantin Wanita & Pria diisi.")
    
    with st.form("screening_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Data Calon Pengantin")
            p_wanita = st.text_input("Nama Lengkap Calon Pengantin Wanita")
            p_pria = st.text_input("Nama Lengkap Calon Pengantin Pria")
            wa_aktif = st.text_input("Nomor WhatsApp Aktif")
            email = st.text_input("Email")
            instagram = st.text_input("Instagram (Opsional)")
            
            st.markdown("#### 📅 Informasi Pernikahan")
            tgl_nikah = st.date_input("Kapan rencana tanggal pernikahan?", min_value=datetime.today())
            kota = st.selectbox("Kota / Area Pernikahan", ["Jakarta", "Depok", "Tangerang & Tangsel", "Other:?"])
            jenis_acara = st.selectbox("Jenis acara yang direncanakan", ["Akad Nikah - Resepsi", "Pemberkatan - Resepsi", "Akad Ramah tamah Only", "Pemberkatan Ramah Tamah", "Resepsi Only"])

        with col2:
            st.markdown("#### 🏰 Detail Acara & Venue")
            tamu = st.selectbox("Estimasi jumlah tamu undangan", ["100", "200", "300", "400", "500"])
            venue_status = st.selectbox("Venue pernikahan", ["Sudah Booking Venue", "Sudah Survey Beberapa Venue", "Belum Mencari Venue"])
            nama_venue = st.text_input("Jika sudah memiliki venue, sebutkan nama venue")
            pref_venue = st.selectbox("Jika memiliki venue, preference seperti apa?", ["Indoor", "Semi Outdoor", "Full Outdoor"])
            
            st.markdown("#### 📝 Tambahan")
            notes = st.text_area("Notes lainnya")
            
        submit_btn = st.form_submit_button("🚀 Simpan Hasil Skrining")
        
        if submit_btn:
            if p_wanita and p_pria:
                # OTOMATISASI LABEL NAMA KLIEN
                auto_label = f"Skrining - {p_wanita.split()[0]} & {p_pria.split()[0]}"
                
                new_data = {
                    "Nama Klien": auto_label, "Pengantin Wanita": p_wanita, "Pengantin Pria": p_pria,
                    "WhatsApp": wa_aktif, "Email": email, "Instagram": instagram, 
                    "Tanggal Pernikahan": str(tgl_nikah), "Kota": kota, "Jenis Acara": jenis_acara,
                    "Estimasi Tamu": tamu, "Venue Status": venue_status, "Nama Venue": nama_venue,
                    "Preference Venue": pref_venue, "Notes": notes
                }
                st.session_state.client_db.append(new_data)
                st.success(f"🎉 Sukses! Data disimpan otomatis dengan Label: '{auto_label}'")
            else:
                st.error("Gagal! Nama Pengantin Wanita dan Pria harus diisi agar Label otomatis bisa dibuat.")

# ==================== MENU 2: LIHAT SUMMARY KEBUTUHAN KLIEN ====================
elif menu == "📋 Lihat Summary Kebutuhan Klien":
    client_list = [c["Nama Klien"] for c in st.session_state.client_db]
    selected_client_name = st.sidebar.selectbox("Pilih Klien untuk Ditampilkan:", client_list)
    client_data = next(c for c in st.session_state.client_db if c["Nama Klien"] == selected_client_name)
    
    st.subheader(f"📋 Summary Hasil Skrining: {client_data['Nama Klien']}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("👤 **Data Calon Pengantin**")
        st.write(f"• **Wanita:** {client_data['Pengantin Wanita']}")
        st.write(f"• **Pria:** {client_data['Pengantin Pria']}")
        st.write(f"• **WhatsApp:** {client_data['WhatsApp']}")
        st.write(f"• **Email:** {client_data['Email']}")
        st.write(f"• **Instagram:** {client_data['Instagram'] if client_data['Instagram'] else '-'}")
    with c2:
        st.success("📅 **Informasi Pernikahan**")
        st.write(f"• **Tanggal Rencana:** {client_data['Tanggal Pernikahan']}")
        st.write(f"• **Kota / Area:** {client_data['Kota']}")
        st.write(f"• **Jenis Acara:** {client_data['Jenis Acara']}")
    with c3:
        st.warning("🏰 **Detail Acara & Venue**")
        st.write(f"• **Estimasi Tamu:** {client_data['Estimasi Tamu']} pax")
        st.write(f"• **Status Venue:** {client_data['Venue Status']}")
        st.write(f"• **Nama Venue:** {client_data['Nama Venue'] if client_data['Nama Venue'] else '-'}")
        st.write(f"• **Preferensi Vibe:** `{client_data['Preference Venue']}`")
        
    st.markdown("---")
    st.error(f"📝 **Notes Lainnya:** {client_data['Notes'] if client_data['Notes'] else '-'}")
    
    # SYSTEM MATCHING PAKET OTOMATIS
    st.markdown("---")
    st.markdown("### 🤖 Hasil Analisis & Rekomendasi Paket 1 Destiny:")
    
    tamu_clean = f"{client_data['Estimasi Tamu']}pax"
    kota_klien = client_data['Kota']
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("#### 🏢 Pilihan Paket Include Venue & Catering")
        match_found = False
        for v in VENUE_PACKAGES:
            if v["Kota"] == kota_klien and tamu_clean in v["Prices"]:
                match_found = True
                harga_paket = v["Prices"][tamu_clean]
                st.markdown(f"⭐ **{v['Nama']}**")
                st.markdown(f"<div class='price-tag'>Harga Paket All-In: {format_rupiah(harga_paket)}</div>", unsafe_allow_html=True)
                with st.expander("👁️ Detail Isi Paket Include"):
                    st.markdown(DETAIL_ALLIN_MEDIUM if v["Tipe"] == "Medium" else DETAIL_ALLIN_SMALL)
        if not match_found:
            st.write("_Tidak ada venue All-In resmi di brosur yang masuk kriteria area & kapasitas ini._")
            
    with col_rec2:
        st.markdown("#### 📦 Pilihan Paket Exclude Venue & Catering")
        st.markdown("**👉 Intimate Package (Up to 300 guests)**")
        st.markdown(f"<div class='price-tag'>Harga Paket: {format_rupiah(51699000)}</div>", unsafe_allow_html=True)
        with st.expander("👁️ Detail Isi Paket Exclude"):
            for sub in PRICELIST_PACKAGES["Exclude Venue & Catering"][0]["Detail"]:
                st.markdown(sub)

    # RE-GENERATOR BRIEF WHATSAPP
    st.markdown("---")
    st.subheader("💬 Teks Briefing Siap Kirim ke WhatsApp Group Tim")
    brief_text = f"""*HASIL SKRINING KLIEN BARU - 1 DESTINY*
====================================
• *Label Klien*  : {client_data['Nama Klien']}
• *Pasangan*     : {client_data['Pengantin Wanita']} & {client_data['Pengantin Pria']}
• *WhatsApp*     : https://wa.me/{client_data['WhatsApp']}
• *Rencana Tgl*  : {client_data['Tanggal Pernikahan']}
• *Kota/Area*    : {client_data['Kota']}
• *Jenis Acara*  : {client_data['Jenis Acara']}
• *Estimasi Tamu*: {client_data['Estimasi Tamu']} Pax
• *Status Venue* : {client_data['Venue Status']} ({client_data['Nama Venue'] if client_data['Nama Venue'] else 'Belum ada'})
• *Pref. Venue*  : {client_data['Preference Venue']}

*📝 Catatan Tambahan:*
"{client_data['Notes'] if client_data['Notes'] else '-'}"
====================================
_Auto-generated by 1 Destiny Wedding CRM_"""
    st.code(brief_text, language="text")

# ==================== MENU 3: PRICE LIST KONSISTEN ====================
else:
    st.subheader("📑 Katalog & Price List Resmi 1 Destiny (2026)")
    t1, t2 = st.tabs(["📦 Exclude Venue & Catering", "🏢 Include Venue & Catering"])
    with t1:
        for kategori, item_list in PRICELIST_PACKAGES.items():
            st.markdown(f"### 🔹 {kategori}")
            for item in item_list:
                with st.expander(f"{item['Nama']} — {format_rupiah(item['Harga'])}"):
                    st.write(f"**Kapasitas:** {item['Tamu']}")
                    for sub_detail in item['Detail']:
                        st.markdown(sub_detail)
    with t2:
        rows = []
        for v in VENUE_PACKAGES:
            rows.append({
                "Wilayah": v["Kota"], "Nama Venue": v["Nama"],
                "100 Pax": format_rupiah(v["Prices"].get("100pax", "-")), "200 Pax": format_rupiah(v["Prices"].get("200pax", "-")),
                "300 Pax": format_rupiah(v["Prices"].get("300pax", "-")), "400 Pax": format_rupiah(v["Prices"].get("400pax", "-")),
                "500 Pax": format_rupiah(v["Prices"].get("500pax", "-")), "Max Kapasitas": f"{v['Kapasitas']} pax"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
