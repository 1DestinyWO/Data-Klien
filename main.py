import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="1 Destiny - Client Screening Dashboard", layout="wide", page_icon="👰")

st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    div[data-testid="stMetricValue"] {font-size: 24px; color: #2E7D32;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px;}
    </style>
    """, unsafe_allow_html=True)

if 'client_db' not in st.session_state:
    st.session_state.client_db = [
        {
            "Nama Klien": "Klien Contoh (Pejaten 1)",
            "Pengantin Wanita": "Siti Aliyah",
            "Pengantin Pria": "Budi Santoso",
            "WhatsApp": "6281234567890",
            "Tanggal Pernikahan": "2026-10-12",
            "Kota": "Jakarta Selatan",
            "Estimasi Tamu": "300-500 pax",
            "Status Venue": "Sudah Survey Beberapa Venue",
            "Nama Venue": "Gedung Pejaten Barat",
            "Konsep": ["Modern", "Intimate"],
            "Budget": "200-300 Juta",
            "Layanan WO": ["Full Wedding Planning", "Vendor Recommendation"],
            "Kendala": "Bingung mencocokkan jadwal keluarga besar untuk akad dan mencari dekorasi adat modern."
        }
    ]

st.title("👰 1 Destiny - Client Screening & Needs Dashboard")
st.caption("Kelola data skrining kuesioner klien dan hasilkan summary kebutuhan dalam satu halaman praktis.")
st.markdown("---")

menu = st.sidebar.radio("Pilih Aktivitas:", ["📋 Lihat Summary Kebutuhan Klien", "➕ Input Klien Baru (Tanpa Excel)"])

if menu == "➕ Input Klien Baru (Tanpa Excel)":
    st.subheader("📝 Form Skrining Klien Baru")
    with st.form("screening_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 👤 Data Calon Pengantin")
            nama_klien = st.text_input("Nama Label Klien *", placeholder="Contoh: Klien Pejaten - Rahma & Dika")
            p_wanita = st.text_input("Nama Lengkap Calon Pengantin Wanita")
            p_pria = st.text_input("Nama Lengkap Calon Pengantin Pria")
            wa_aktif = st.text_input("Nomor WhatsApp (Gunakan format 62... tanpa spasi)")
            st.markdown("#### 📅 Informasi Pernikahan")
            tgl_nikah = st.date_input("Kapan rencana tanggal pernikahan?", min_value=datetime.today())
            kota = st.selectbox("Kota / Area Pernikahan", ["Jakarta Selatan", "Jakarta Barat", "Jakarta Timur", "Jakarta Utara", "Jakarta Pusat", "Tangerang", "BSD", "Depok", "Bekasi", "Bogor", "Lainnya"])
            tamu = st.selectbox("Estimasi Jumlah Tamu Undangan", ["<100 pax", "100-300 pax", "300-500 pax", "500-800 pax", "800-1000 pax", ">1000 pax"])
        with col2:
            st.markdown("#### 🏰 Detail Venue & Konsep")
            venue_status = st.selectbox("Status Venue Pernikahan", ["Belum Mencari Venue", "Sudah Survey Beberapa Venue", "Sudah Booking Venue"])
            nama_venue = st.text_input("Jika sudah memiliki venue, sebutkan nama venue")
            konsep = st.multiselect("Konsep pernikahan yang diinginkan", ["Modern", "Elegant", "Garden", "Intimate", "Luxury", "Traditional/Adat", "International Wedding", "Belum Menentukan"])
            st.markdown("#### 💰 Budget & Kebutuhan WO")
            budget = st.selectbox("Kisaran Budget Keseluruhan", ["<100 Juta", "100-200 Juta", "200-300 Juta", "300-500 Juta", "500-750 Juta", "750 Juta-1 Miliar", ">1 Miliar", "Masih dalam tahap perhitungan"])
            layanan = st.multiselect("Layanan WO yang dicari", ["Full Wedding Planning", "Wedding Day Service", "Vendor Recommendation", "Venue Recommendation", "Konsultasi Persiapan Pernikahan"])
            kendala = st.text_area("Apa kendala terbesar yang sedang dihadapi?")
        submit_btn = st.form_submit_button("🚀 Simpan Data Klien ke Dashboard")
        if submit_btn:
            if nama_klien:
                new_client = {
                    "Nama Klien": nama_klien, "Pengantin Wanita": p_wanita, "Pengantin Pria": p_pria,
                    "WhatsApp": wa_aktif, "Tanggal Pernikahan": str(tgl_nikah), "Kota": kota,
                    "Estimasi Tamu": tamu, "Status Venue": venue_status, "Nama Venue": nama_venue,
                    "Konsep": konsep, "Budget": budget, "Layanan WO": layanan, "Kendala": kendala
                }
                st.session_state.client_db.append(new_client)
                st.success(f"🎉 Sukses! Data untuk '{nama_klien}' telah berhasil direkam.")
            else:
                st.error("Gagal menyimpan! 'Nama Label Klien' wajib diisi.")
else:
    client_list = [c["Nama Klien"] for c in st.session_state.client_db]
    selected_client_name = st.sidebar.selectbox("Pilih Klien untuk Ditampilkan:", client_list)
    client_data = next(c for c in st.session_state.client_db if c["Nama Klien"] == selected_client_name)
    st.subheader(f"📋 Client Needs Summary: {client_data['Nama Klien']}")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("👤 **Profil Utama Pasangan**")
        st.write(f"• **Calon Wanita:** {client_data['Pengantin Wanita'] if client_data['Pengantin Wanita'] else '-'}")
        st.write(f"• **Calon Pria:** {client_data['Pengantin Pria'] if client_data['Pengantin Pria'] else '-'}")
        st.write(f"• **WhatsApp:** {client_data['WhatsApp'] if client_data['WhatsApp'] else '-'}")
    with c2:
        st.success("📅 **Rencana Acara & Logistik**")
        st.write(f"• **Tanggal Acara:** {client_data['Tanggal Pernikahan']}")
        st.write(f"• **Area/Kota:** {client_data['Kota']}")
        st.write(f"• **Skala Tamu:** {client_data['Estimasi Tamu']}")
    with c3:
        st.warning("💰 **Alokasi Budget & Solusi**")
        st.write(f"• **Target Anggaran:** {client_data['Budget']}")
        layanan_str = ", ".join(client_data['Layanan WO']) if client_data['Layanan WO'] else "-"
        st.write(f"• **Layanan Dicari:** {layanan_str}")
    st.markdown("---")
    col_detail1, col_detail2 = st.columns(2)
    with col_detail1:
        st.markdown("### 🏰 Informasi Lokasi & Estetika")
        st.markdown(f"**Status Lokasi Acara:** `{client_data['Status Venue']}`")
        if client_data['Nama Venue']:
            st.markdown(f"**Nama Tempat/Venue:** {client_data['Nama Venue']}")
        konsep_str = ", ".join(client_data['Konsep']) if client_data['Konsep'] else "Belum Menentukan"
        st.markdown(f"**Vibe & Konsep Acara:** {konsep_str}")
    with col_detail2:
        st.error("⚠️ **Pain Points / Kendala Terbesar Klien**")
        st.write(client_data['Kendala'] if client_data['Kendala'] else "-")
    st.markdown("---")
    st.subheader("💬 Auto-Brief Teks Siap Kirim (Tinggal Copy ke WhatsApp Tim)")
    brief_text = f"""*BRIEF KLIEN BARU - 1 DESTINY*
====================================
• *Nama Klien*   : {client_data['Nama Klien']}
• *Nama Pasangan*: {client_data['Pengantin Wanita']} & {client_data['Pengantin Pria']}
• *Tanggal Acara*: {client_data['Tanggal Pernikahan']}
• *Lokasi/Area*  : {client_data['Kota']} ({client_data['Nama Venue'] if client_data['Nama Venue'] else 'Venue belum fix'})
• *Estimasi Tamu*: {client_data['Estimasi Tamu']}
• *Konsep Impian*: {konsep_str}
• *Range Budget* : {client_data['Budget']}
• *Layanan Dicari*: {layanan_str}

*⚠️ Kendala Utama Klien:*
"{client_data['Kendala'] if client_data['Kendala'] else '-'}"
====================================
_Dibuat otomatis oleh Wedding CRM Dashboard_"""
    st.code(brief_text, language="text")
