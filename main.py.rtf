{\rtf1\ansi\ansicpg1252\cocoartf2869
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww16760\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
from datetime import datetime\
\
# Konfigurasi Halaman & Tema Web\
st.set_page_config(page_title="1 Destiny - Client Screening Dashboard", layout="wide", page_icon="\uc0\u55357 \u56432 ")\
\
# Custom CSS untuk mempercantik tampilan UI\
st.markdown("""\
    <style>\
    .main \{background-color: #f8f9fa;\}\
    div[data-testid="stMetricValue"] \{font-size: 24px; color: #2E7D32;\}\
    .stButton>button \{background-color: #4CAF50; color: white; border-radius: 8px;\}\
    </style>\
    """, unsafe_allow_html=True)\
\
# Database internal menggunakan Session State agar data tidak hilang selama aplikasi berjalan\
if 'client_db' not in st.session_state:\
    st.session_state.client_db = [\
        \{\
            "Nama Klien": "Klien Contoh (Pejaten 1)",\
            "Pengantin Wanita": "Siti Aliyah",\
            "Pengantin Pria": "Budi Santoso",\
            "WhatsApp": "6281234567890",\
            "Tanggal Pernikahan": "2026-10-12",\
            "Kota": "Jakarta Selatan",\
            "Estimasi Tamu": "300-500 pax",\
            "Status Venue": "Sudah Survey Beberapa Venue",\
            "Nama Venue": "Gedung Pejaten Barat",\
            "Konsep": ["Modern", "Intimate"],\
            "Budget": "200-300 Juta",\
            "Layanan WO": ["Full Wedding Planning", "Vendor Recommendation"],\
            "Kendala": "Bingung mencocokkan jadwal keluarga besar untuk akad dan mencari dekorasi adat modern."\
        \}\
    ]\
\
st.title("\uc0\u55357 \u56432  1 Destiny - Client Screening & Needs Dashboard")\
st.caption("Kelola data skrining kuesioner klien dan hasilkan summary kebutuhan dalam satu halaman praktis.")\
st.markdown("---")\
\
# ==================== SIDEBAR NAVIGATION ====================\
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3656/3656836.png", width=100)\
st.sidebar.header("\uc0\u55356 \u57263  Menu Dashboard")\
menu = st.sidebar.radio("Pilih Aktivitas:", ["\uc0\u55357 \u56523  Lihat Summary Kebutuhan Klien", "\u10133  Input Klien Baru (Tanpa Excel)"])\
\
# ==================== MENU 1: INPUT KLIEN BARU ====================\
if menu == "\uc0\u10133  Input Klien Baru (Tanpa Excel)":\
    st.subheader("\uc0\u55357 \u56541  Form Skrining Klien Baru")\
    st.info("Isi form di bawah ini berdasarkan hasil kuesioner atau wawancara klien. Data akan langsung terangkum di dashboard.")\
    \
    with st.form("screening_form", clear_on_submit=True):\
        col1, col2 = st.columns(2)\
        \
        with col1:\
            st.markdown("#### \uc0\u55357 \u56420  Data Calon Pengantin")\
            nama_klien = st.text_input("Nama Label Klien *", placeholder="Contoh: Klien Pejaten - Rahma & Dika")\
            p_wanita = st.text_input("Nama Lengkap Calon Pengantin Wanita")\
            p_pria = st.text_input("Nama Lengkap Calon Pengantin Pria")\
            wa_aktif = st.text_input("Nomor WhatsApp (Gunakan format 62... tanpa spasi)")\
            \
            st.markdown("#### \uc0\u55357 \u56517  Informasi Pernikahan")\
            tgl_nikah = st.date_input("Kapan rencana tanggal pernikahan?", min_value=datetime.today())\
            kota = st.selectbox("Kota / Area Pernikahan", ["Jakarta Selatan", "Jakarta Barat", "Jakarta Timur", "Jakarta Utara", "Jakarta Pusat", "Tangerang", "BSD", "Depok", "Bekasi", "Bogor", "Lainnya"])\
            tamu = st.selectbox("Estimasi Jumlah Tamu Undangan", ["<100 pax", "100-300 pax", "300-500 pax", "500-800 pax", "800-1000 pax", ">1000 pax"])\
\
        with col2:\
            st.markdown("#### \uc0\u55356 \u57328  Detail Venue & Konsep")\
            venue_status = st.selectbox("Status Venue Pernikahan", ["Belum Mencari Venue", "Sudah Survey Beberapa Venue", "Sudah Booking Venue"])\
            nama_venue = st.text_input("Jika sudah memiliki venue, sebutkan nama venue")\
            konsep = st.multiselect("Konsep pernikahan yang diinginkan (Bisa pilih beberapa)", ["Modern", "Elegant", "Garden", "Intimate", "Luxury", "Traditional/Adat", "International Wedding", "Belum Menentukan"])\
            \
            st.markdown("#### \uc0\u55357 \u56496  Budget & Kebutuhan WO")\
            budget = st.selectbox("Kisaran Budget Keseluruhan", ["<100 Juta", "100-200 Juta", "200-300 Juta", "300-500 Juta", "500-750 Juta", "750 Juta-1 Miliar", ">1 Miliar", "Masih dalam tahap perhitungan"])\
            layanan = st.multiselect("Layanan WO yang dicari", ["Full Wedding Planning", "Wedding Day Service", "Vendor Recommendation", "Venue Recommendation", "Konsultasi Persiapan Pernikahan"])\
            kendala = st.text_area("Apa kendala terbesar yang sedang dihadapi?")\
            \
        submit_btn = st.form_submit_button("\uc0\u55357 \u56960  Simpan Data Klien ke Dashboard")\
        \
        if submit_btn:\
            if nama_klien:\
                new_client = \{\
                    "Nama Klien": nama_klien, "Pengantin Wanita": p_wanita, "Pengantin Pria": p_pria,\
                    "WhatsApp": wa_aktif, "Tanggal Pernikahan": str(tgl_nikah), "Kota": kota,\
                    "Estimasi Tamu": tamu, "Status Venue": venue_status, "Nama Venue": nama_venue,\
                    "Konsep": konsep, "Budget": budget, "Layanan WO": layanan, "Kendala": kendala\
                \}\
                st.session_state.client_db.append(new_client)\
                st.success(f"\uc0\u55356 \u57225  Sukses! Data untuk '\{nama_klien\}' telah berhasil direkam. Silakan kembali ke menu 'Lihat Summary Kebutuhan Klien'.")\
            else:\
                st.error("Gagal menyimpan! 'Nama Label Klien' wajib diisi sebagai penanda.")\
\
# ==================== MENU 2: LIHAT SUMMARY KEBUTUHAN KLIEN ====================\
else:\
    client_list = [c["Nama Klien"] for c in st.session_state.client_db]\
    selected_client_name = st.sidebar.selectbox("Pilih Klien untuk Ditampilkan:", client_list)\
    \
    # Ambil data klien terpilih\
    client_data = next(c for c in st.session_state.client_db if c["Nama Klien"] == selected_client_name)\
    \
    st.subheader(f"\uc0\u55357 \u56523  Client Needs Summary: \{client_data['Nama Klien']\}")\
    \
    # Tampilan Indikator Utama ala Dashboard Eksekutif\
    c1, c2, c3 = st.columns(3)\
    with c1:\
        st.info("\uc0\u55357 \u56420  **Profil Utama Pasangan**")\
        st.write(f"\'95 **Calon Wanita:** \{client_data['Pengantin Wanita'] if client_data['Pengantin Wanita'] else '-'\}")\
        st.write(f"\'95 **Calon Pria:** \{client_data['Pengantin Pria'] if client_data['Pengantin Pria'] else '-'\}")\
        if client_data['WhatsApp']:\
            st.write(f"\'95 **WhatsApp:** [\{client_data['WhatsApp']\}](https://wa.me/\{client_data['WhatsApp']\})")\
        else:\
            st.write("\'95 **WhatsApp:** -")\
            \
    with c2:\
        st.success("\uc0\u55357 \u56517  **Rencana Acara & Logistik**")\
        st.write(f"\'95 **Tanggal Acara:** \{client_data['Tanggal Pernikahan']\}")\
        st.write(f"\'95 **Area/Kota:** \{client_data['Kota']\}")\
        st.write(f"\'95 **Skala Tamu:** \{client_data['Estimasi Tamu']\}")\
        \
    with c3:\
        st.warning("\uc0\u55357 \u56496  **Alokasi Budget & Solusi**")\
        st.write(f"\'95 **Target Anggaran:** \{client_data['Budget']\}")\
        layanan_str = ", ".join(client_data['Layanan WO']) if client_data['Layanan WO'] else "-"\
        st.write(f"\'95 **Layanan Dicari:** \{layanan_str\}")\
\
    st.markdown("---")\
    \
    col_detail1, col_detail2 = st.columns(2)\
    with col_detail1:\
        st.markdown("### \uc0\u55356 \u57328  Informasi Lokasi & Estetika")\
        st.markdown(f"**Status Lokasi Acara:** `\{client_data['Status Venue']\}`")\
        if client_data['Nama Venue']:\
            st.markdown(f"**Nama Tempat/Venue:** \{client_data['Nama Venue']\}")\
        konsep_str = ", ".join(client_data['Konsep']) if client_data['Konsep'] else "Belum Menentukan"\
        st.markdown(f"**Vibe & Konsep Acara:** \{konsep_str\}")\
        \
    with col_detail2:\
        st.error("\uc0\u9888 \u65039  **Pain Points / Kendala Terbesar Klien**")\
        st.write(client_data['Kendala'] if client_data['Kendala'] else "Tidak ada kendala spesifik yang diinput.")\
\
    # Otomatisasi teks siap kirim ke grup WhatsApp internal Koordinasi Tim WO\
    st.markdown("---")\
    st.subheader("\uc0\u55357 \u56492  Auto-Brief Teks Siap Kirim (Tinggal Copy ke WhatsApp Tim)")\
    \
    brief_text = f"""*BRIEF KLIEN BARU - 1 DESTINY*\
====================================\
\'95 *Nama Klien*   : \{client_data['Nama Klien']\}\
\'95 *Nama Pasangan*: \{client_data['Pengantin Wanita']\} & \{client_data['Pengantin Pria']\}\
\'95 *Tanggal Acara*: \{client_data['Tanggal Pernikahan']\}\
\'95 *Lokasi/Area*  : \{client_data['Kota']\} (\{client_data['Nama Venue'] if client_data['Nama Venue'] else 'Venue belum fix'\})\
\'95 *Estimasi Tamu*: \{client_data['Estimasi Tamu']\}\
\'95 *Konsep Impian*: \{konsep_str\}\
\'95 *Range Budget* : \{client_data['Budget']\}\
\'95 *Layanan Dicari*: \{layanan_str\}\
\
*\uc0\u9888 \u65039  Kendala Utama Klien:*\
"\{client_data['Kendala'] if client_data['Kendala'] else '-'\}"\
====================================\
_Dibuat otomatis oleh Wedding CRM Dashboard_"""\
    \
    st.code(brief_text, language="text")}