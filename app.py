import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Konfigurasi Halaman
st.set_page_config(page_title="PBL 5 - Estimasi Stok Ikan", layout="wide")

# CSS
st.markdown("""
    <style>
    .main-header { background: linear-gradient(90deg, #004a99 0%, #0077b6 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px; }
    .info-box { background-color: var(--secondary-background-color); padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; }
    </style>
""", unsafe_allow_html=True)

# Header
with st.container():
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        if os.path.exists("Logo Unisbaa.png"): st.image("Logo Unisbaa.png", width=120)
    with col_title:
        st.markdown("<h1 style='color: white; margin: 0;'>Estimasi Stok Ikan Laut Jawa</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: white; margin: 0;'>PBL 5 — Ekonomi Sumber Daya Ikan</h3>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👥 Kelompok 4")
        st.write("• **Salsa Zahratul Aulia** (10090224004)")
        st.write("• **Aida Farida Kultsum** (10090224014)")
        st.write("• **Nabil Athala Naufal** (10090224022)")
    with col2:
        st.markdown("### 🎓 Informasi Akademik")
        st.markdown('<div class="info-box"><b>Mata Kuliah:</b> Ekonomi Sumber Daya Alam dan Lingkungan<br>'
                    '<b>Dosen Pengampu:</b> YUHKA SUNDAYA, S.E., M.Si.</div>', unsafe_allow_html=True)

st.markdown("---")

# Fungsi Data dengan perbaikan index
@st.cache_data(ttl=10)
def get_data():
    # index_col=0 digunakan untuk mengabaikan kolom angka (0,1,2,3...) yang tidak perlu
    df = pd.read_csv("2026-06-16T05-00_export.csv", index_col=0)
    df.columns = df.columns.str.strip()
    
    # Pastikan urutan benar
    order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]
    df['Bulan'] = pd.Categorical(df['Bulan'], categories=order, ordered=True)
    return df.sort_values('Bulan')

# Load Data
data = get_data()

# Debugging (bisa dihapus nanti)
# st.write(f"Data terbaca: {len(data)} baris") 

# Dashboard Grafik
st.subheader("📊 Analisis Oseanografi & Prediksi Biomassa")
col1, col2 = st.columns(2)

with col1:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data["Bulan"], y=data["Suhu_Laut_C"], name="Suhu (°C)", mode='lines+markers', line=dict(color="red")), secondary_y=False)
    fig.add_trace(go.Scatter(x=data["Bulan"], y=data["Klorofil_a"], name="Klorofil (mg/m³)", mode='lines+markers', line=dict(color="green", dash="dash")), secondary_y=True)
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = go.Figure(go.Bar(x=data["Bulan"], y=data["Estimasi_Stok"], marker_color="#4682B4", name="Estimasi Stok"))
    fig2.add_trace(go.Scatter(x=data["Bulan"], y=data["Estimasi_Stok"], line=dict(color="orange", width=3), name="Tren"))
    fig2.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig2, use_container_width=True)

# Tabel Data
st.subheader("📋 Detail Data Mentah")
st.dataframe(data, use_container_width=True)
