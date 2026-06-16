import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Estimasi Stok Ikan Laut Jawa", layout="wide", page_icon="🐟")

# CSS Dinamis: Menggunakan variabel warna tema Streamlit agar support Mode Gelap/Terang
st.markdown("""
    <style>
    .main-header { 
        background: linear-gradient(135deg, #003366 0%, #0077b6 100%); 
        padding: 25px; 
        border-radius: 15px; 
        color: white; 
        margin-bottom: 25px; 
    }
    .info-card { 
        background-color: var(--secondary-background-color); 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #0077b6; 
        color: var(--text-color); 
    }
    </style>
""", unsafe_allow_html=True)

# Header Informatif
with st.container():
    col_logo, col_text = st.columns([1, 6])
    with col_logo:
        if os.path.exists("Logo Unisbaa.png"):
            st.image("Logo Unisbaa.png", width=110)
    with col_text:
        st.markdown('<div class="main-header"><h1>Estimasi Stok Ikan Laut Jawa</h1><h4>PBL 5 — Ekonomi Sumber Daya Ikan</h4></div>', unsafe_allow_html=True)

    col_kiri, col_kanan = st.columns([1, 1])
    with col_kiri:
        st.markdown("### 👥 Tim Peneliti")
        st.write("• **Salsa Zahratul Aulia** (10090224004)")
        st.write("• **Aida Farida Kultsum** (10090224014)")
        st.write("• **Nabil Athala Naufal** (10090224022)")
    with col_kanan:
        st.markdown('<div class="info-card"><b>Mata Kuliah:</b> Ekonomi Sumber Daya Alam dan Lingkungan<br>'
                    '<b>Dosen Pengampu:</b> Yuhka Sundaya, S.E., M.Si.</div>', unsafe_allow_html=True)

st.markdown("---")

@st.cache_data(ttl=60)
def load_data():
    file_path = os.path.join("DATA", "Estimasi Stok Ikan Laut Jawa")
    df = pd.read_csv(file_path, sep='\s+', decimal=',')
    order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]
    df['Bulan'] = pd.Categorical(df['Bulan'], categories=order, ordered=True)
    return df.sort_values('Bulan')

try:
    df = load_data()
    col1, col2 = st.columns([2.5, 1])

    with col1:
        st.subheader("📊 Analisis Oseanografi")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Suhu_Laut_C"], name="Suhu (°C)", line=dict(color="#FF4136", width=3)), secondary_y=False)
        fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Klorofil_a"], name="Klorofil", line=dict(color="#2ECC40", width=3, dash="dot")), secondary_y=True)
        # Template diubah menjadi None agar mengikuti tema Streamlit (Gelap/Terang)
        fig.update_layout(template=None, height=400, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📈 Estimasi Stok")
        st.metric("Stok Puncak (Ton)", f"{df['Estimasi_Stok'].max():,.0f}")
        fig2 = go.Figure(go.Bar(x=df["Bulan"], y=df["Estimasi_Stok"], marker_color="#0077b6"))
        fig2.update_layout(template=None, height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📋 Lihat Detail Data Mentah"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}. Pastikan file 'Estimasi Stok Ikan Laut Jawa' ada di folder 'DATA'.")
