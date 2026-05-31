import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP HALAMAN & TEMA UTAMA
st.set_page_config(page_title="1 Destiny - Client Management Dashboard", layout="wide", page_icon="👰")

# Custom CSS Estetika & Format Kardus Harga
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    div[data-testid="stMetricValue"] {font-size: 22px; color: #1E88E5;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px; width: 100%;}
    .price-tag { background-color: #E8F5E9; padding: 12px; border-left: 5px solid #2E7D32; font-weight: bold; font-size: 18px; color: #1B5E20; margin: 10px 0;}
    
    /* Trik CSS memaksa semua foto menjadi kotak / square simetris */
    img {
        width: 100% !important;
        height: 280px !important;
        object-fit: cover !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Fungsi pembantu untuk memformat angka menjadi Rupiah
def format_rupiah(angka):
    if isinstance(angka, (int, float)):
        return f"Rp {angka:,.0f}".replace(",", ".")
    return str(angka)

# 2. DATABASE INTERNAL PRICELIST 2026
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
    {"Kota": "Jakarta", "Nama": "D'Hall Kementerian Pertanian", "Prices": {"400pax": 163799000, "500pax": 173799000}, "Kapasitas": 700, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Soho Pancoran Ballroom", "Prices": {"400pax": 173799000, "500pax": 183799000}, "Kapasitas": 700, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Felfest UI", "Prices": {"400pax": 190799000, "500pax": 200799000}, "Kapasitas": 800, "Tipe": "Medium"},
    {"Kota": "Jakarta", "Nama": "Taman Kajoe", "Prices": {"400pax": 209799000, "500pax": 222799000}, "Kapasitas": 1000, "Tipe": "Medium"}
]

# 3. DATABASE VENDOR REKANAN DENGAN KOLOM DOKUMEN & PORTFOLIO GOOGLE DRIVE (SESUAI SCREENSHOT)
VENDOR_LIST = [
    {
        "Kategori": "Wedding planner/organizer", 
        "Nama Vendor": "1 Destiny Wedding Organizer", 
        "Instagram": "https://www.instagram.com/1destiny.wo/",
        "Dokumen / GDrive": "-"
    },
    {
        "Kategori": "Documentation", 
        "Nama Vendor": "Aestec", 
        "Instagram": "https://www.instagram.com/aestec.wedding/",
        "Dokumen / GDrive": '<a href="https://drive.google.com/drive/folders/10TcX5am4ZLWL_Umb1hG1zCHMkURq9u_i" target="_blank">📁 Buka Portfolio</a>'
    },
    {
        "Kategori": "Documentation", 
        "Nama Vendor": "Camonphoto", 
        "Instagram": "https://www.instagram.com/camonphoto/",
        "Dokumen / GDrive": '<a href="https://drive.google.com/drive/folders/1Lku_U-iZY3mh11m9i-BwH9LycXmSPnt" target="_blank">📁 Buka Portfolio</a>'
    },
    {
        "Kategori": "Decoration", 
        "Nama Vendor": "Fashdecor", 
        "Instagram": "https://www.instagram.com/fashdecor.id/?hl=en",
        "Dokumen / GDrive": "-"
    },
    {
        "Kategori": "MUA & Attire", 
        "Nama Vendor": "Micca Brides", 
        "Instagram": "https://www.instagram.com/miccabrides/",
        "Dokumen / GDrive": """
            <a href="https://drive.google.com/drive/folders/1N-GSGPwlCyhcUdlvSF1o1uPPgzcgkK_L/" target="_blank">📑 Catalog Micca</a><br>
            <a href="https://drive.google.com/drive/folders/10TcX5am4ZLWL_Umb1hG1zCHMkURq9u_i/" target="_blank">💄 MUA Bride</a><br>
            <a href="https://drive.google.com/drive/folders/1aLYchVrKgc54et_pEJF9j0XpBsuDc9Ly" target="_blank">👩 MUA Mom</a>
        """
    },
    {"Kategori": "MC", "Nama Vendor": "Mawadah", "Instagram": "https://www.instagram.com/mawadah_mc?igsh=Y2pkdXF0d2NlemQy/", "Dokumen / GDrive": "-"},
    {"Kategori": "MC", "Nama Vendor": "Mulyadi", "Instagram": "https://www.instagram.com/mulyadi_mc?igsh=NWY1ZWhpOWlkNGpk/", "Dokumen / GDrive": "-"},
    {"Kategori": "MC", "Nama Vendor": "Dewi MC", "Instagram": "https://www.instagram.com/dewinurmc?igsh=MW5xcjNiZGRldWxkeA==", "Dokumen / GDrive": "-"},
    {"Kategori": "MC", "Nama Vendor": "Uppeh", "Instagram": "https://www.instagram.com/uppeh.mc/", "Dokumen / GDrive": "-"},
    {"Kategori": "MC", "Nama Vendor": "Najibah", "Instagram": "https://www.instagram.com/najibahfauzii", "Dokumen / GDrive": "-"},
    {"Kategori": "Entertainment (Optional)", "Nama Vendor": "SWAG Project", "Instagram": "https://www.instagram.com/swag_project?igsh=a3A5YzgyZ3V3ZXBz", "Dokumen / GDrive": "-"}
]

# 4. INITIALIZE SIMULASI DATABASE KLIEN DI SESSION STATE
if 'client_db' not in st.session_state:
    st.session_state.client_db = [
        {
            "Nama Klien": "Skrining - Siti & Budi", "Pengantin Wanita": "Siti Aliyah", "Pengantin Pria": "Budi Santoso",
            "WhatsApp": "6281234567890", "Email": "siti.budi@email.com", "Instagram": "@siti_aliyah",
            "Tanggal Pernikahan": "2026-12-12", "Kota": "Jakarta", "Jenis Acara": "Akad Nikah - Resepsi",
            "Estimasi Tamu": "300", "Venue Status": "Sudah Survey Beberapa Venue", "Nama Venue": "Pejaten Terrace",
            "Preference Venue": "Semi Outdoor", "Notes": "Mencari dekorasi dengan tema floral natural."
        }
    ]

# 5. SIDEBAR NAVIGATION
st.sidebar.title("1 Destiny WO 2026")
menu = st.sidebar.radio("Navigasi Konten:", [
    "📋 Lihat Summary Kebutuhan Klien", 
    "➕ Input Klien Baru (Form Skrining Baru)", 
    "💰 Lihat Price List Resmi 2026",
    "🤝 Our Vendor List & Portfolio"
])

# ==================== MENU: OUR VENDOR LIST & PORTFOLIO (SUDAH DIBENAHI) ====================
if menu == "🤝 Our Vendor List & Portfolio":
    st.subheader("🤝 1 Destiny Official Vendor List & Portfolio (2026)")
    
    tab_list, tab_galeri = st.tabs(["📋 Daftar Vendor & Dokumen", "📸 Galeri Foto"])
    
    with tab_list:
        st.info("Klik tombol 'Buka Instagram' atau link Google Drive di sebelah kanan untuk melihat kelengkapan dokumen.")
        
        # Mapping struktur kolom sesuai instruksi spreadsheet baru
        formatted_vendors = []
        for vendor in VENDOR_LIST:
            formatted_vendors.append({
                "Kategori / Item": vendor["Kategori"],
                "Nama Vendor": vendor["Nama Vendor"],
                "Link Instagram": f'<a href="{vendor["Instagram"]}" target="_blank">🔗 Buka Instagram</a>',
                "Portfolio & Dokumen Resmi (Google Drive)": vendor["Dokumen / GDrive"]
            })
            
        df_vendor = pd.DataFrame(formatted_vendors)
        # Tampilkan tabel HTML interaktif agar link GDrive & IG bisa diklik langsung
        st.write(df_vendor.to_html(escape=False, index=False), unsafe_allow_html=True)
        
    with tab_galeri:
        st.markdown("### 🌟 Dokumentasi Real-Event Portfolio")
        st.write("")
        
        # Grid Foto Square
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.image("Dokumentasi1.jpg", use_container_width=True)
        with c2: st.image("Dokumentasi2.jpg", use_container_width=True)
        with c3: st.image("Dokumentasi3.jpg", use_container_width=True)
        with c4: st.image("Dokumentasi4.jpg", use_container_width=True)
        
        c5, c6, c7, c8 = st.columns(4)
        with c5: st.image("Dokumentasi5.jpg", use_container_width=True)
        with c6: st.image("Dokumentasi6.jpg", use_container_width=True)
        with c7: st.image("Dokumentasi7.jpg", use_container_width=True)
        with c8: st.image("Dokumentasi8.jpg", use_container_width=True)
        
        c9, c10, c11, c12 = st.columns(4)
        with c9: st.image("Dokumentasi9.jpg", use_container_width=True)
        with c10: st.image("Dokumentasi10.jpg", use_container_width=True)
        with c11: st.image("Dokumentasi12.jpg", use_container_width=True)
        with c12: st.image("Dokumentasi11.jpg", use_container_width=True)
        
        c13, c14, _, _ = st.columns(4)
        with c13: st.image("Dokumentasi13.jpg", use_container_width=True)
        with c14: st.image("Dokumentasi14.jpg", use_container_width=True)

# ==================== MENU: LIHAT PRICELIST RESMI ====================
elif menu == "💰 Lihat Price List Resmi 2026":
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

# ==================== MENU: FORM SKRINING BARU ====================
elif menu == "➕ Input Klien Baru (Form Skrining Baru)":
    st.subheader("📝 Form Skrining Klien Baru")
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
            kota = st.selectbox("Kota / Area Pernikahan", ["Jakarta", "Depok", "Tangerang & Tangsel"])
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
        if submit_btn and p_wanita and p_pria:
            auto_label = f"Skrining - {p_wanita.split()[0]} & {p_pria.split()[0]}"
            new_data = {
                "Nama Klien": auto_label, "Pengantin Wanita": p_wanita, "Pengantin Pria": p_pria,
                "WhatsApp": wa_aktif, "Email": email, "Instagram": instagram, 
                "Tanggal Pernikahan": str(tgl_nikah), "Kota": kota, "Jenis Acara": jenis_acara,
                "Estimasi Tamu": tamu, "Venue Status": venue_status, "Nama Venue": nama_venue,
                "Preference Venue": pref_venue, "Notes": notes
            }
            st.session_state.client_db.append(new_data)
            st.success(f"🎉 Sukses! Tersimpan otomatis dengan Label Klien: '{auto_label}'")

# ==================== MENU: LIHAT SUMMARY KEBUTUHAN KLIEN ====================
else:
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
        st.write(f"• **Instagram:** {client_data['Instagram']}")
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
    st.error(f"📝 **Notes Lainnya:** {client_data['Notes']}")
    
    # SYSTEM MATCHING PAKET REKOMENDASI OTOMATIS
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
            st.write("_Tidak ada venue Include Venue & Catering resmi di brosur yang masuk kriteria area & kapasitas ini._")
            
    with col_rec2:
        st.markdown("#### 📦 Pilihan Paket Exclude Venue & Catering")
        st.markdown("**👉 Intimate Package (Up to 300 guests)**")
        st.markdown(f"<div class='price-tag'>Harga Paket: {format_rupiah(51699000)}</div>", unsafe_allow_html=True)
        with st.expander("👁️ Detail Isi Paket Exclude"):
            for sub in PRICELIST_PACKAGES["Exclude Venue & Catering"][0]["Detail"]:
                st.markdown(sub)

    # BRIEF COPIER WA
    st.markdown("---")
    st.subheader("💬 Teks Briefing Siap Kirim ke WhatsApp Group Tim")
    brief_text = f"""*HASIL SKRINING KLIEN BARU - 1 DESTINY*
====================================
• *Label Klien* : {client_data['Nama Klien']}
• *Pasangan* : {client_data['Pengantin Wanita']} & {client_data['Pengantin Pria']}
• *WhatsApp* : https://wa.me/{client_data['WhatsApp']}
• *Rencana Tgl* : {client_data['Tanggal Pernikahan']}
• *Kota/Area* : {client_data['Kota']}
• *Jenis Acara* : {client_data['Jenis Acara']}
• *Estimasi Tamu*: {client_data['Estimasi Tamu']} Pax
• *Status Venue* : {client_data['Venue Status']} ({client_data['Nama Venue'] if client_data['Nama Venue'] else 'Belum ada'})
• *Pref. Venue* : {client_data['Preference Venue']}

*📝 Catatan Tambahan:*
"{client_data['Notes'] if client_data['Notes'] else '-'}"
====================================
_Auto-generated by 1 Destiny Wedding CRM_"""
    st.code(brief_text, language="text")
