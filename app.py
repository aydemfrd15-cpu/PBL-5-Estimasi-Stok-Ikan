import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Estimasi Stok Ikan Laut Jawa", layout="wide")

# 2. CSS untuk Tampilan Profesional
st.markdown("""
    <style>
    .main-header { 
        background: linear-gradient(90deg, #001f3f 0%, #0077b6 100%); 
        padding: 25px; 
        border-radius: 10px; 
        color: white; 
        margin-bottom: 20px; 
    }
    .info-card { 
        background-color: #f0f2f6; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #0077b6; 
        color: #333; 
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Informatif
with st.container():
    st.markdown('<div class="main-header"><h1>Estimasi Stok Ikan Laut Jawa</h1><h3>PBL 5 — Ekonomi Sumber Daya Ikan</h3></div>', unsafe_allow_html=True)
    
    col_kiri, col_kanan = st.columns([1, 1])
    with col_kiri:
        st.markdown("### 👥 KELOMPOK 4")
        st.write("• **Salsa Zahratul Aulia** (10090224004)")
        st.write("• **Aida Farida Kultsum** (10090224014)")
        st.write("• **Nabil Athala Naufal** (10090224022)")
    with col_kanan:
        st.markdown('<div class="info-card"><b>Mata Kuliah:</b> Ekonomi Sumber Daya Alam dan Lingkungan<br>'
                    '<b>Dosen Pengampu:</b> Yuhka Sundaya, S.E., M.Si.</div>', unsafe_allow_html=True)

st.markdown("---")

# 4. Fungsi Data yang Stabil
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("2026-06-16T05-00_export.csv")
    if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
    order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]
    df['Bulan'] = pd.Categorical(df['Bulan'], categories=order, ordered=True)
    return df.sort_values('Bulan')

try:
    df = load_data()

    # 5. Dashboard Utama
    col_grafik, col_sidebar = st.columns([2.5, 1])

    with col_grafik:
        st.subheader("📊 Analisis Oseanografi & Biomassa")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Suhu_Laut_C"], name="Suhu (°C)", line=dict(color="#d62728", width=3)), secondary_y=False)
        fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Klorofil_a"], name="Klorofil", line=dict(color="#2ca02c", width=3, dash="dot")), secondary_y=True)
        fig.update_layout(template="plotly_white", height=450, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_sidebar:
        st.subheader("📈 Estimasi Stok")
        st.metric("Stok Puncak", f"{df['Estimasi_Stok'].max():,.0f} Ton")
        fig2 = go.Figure(go.Bar(x=df["Bulan"], y=df["Estimasi_Stok"], marker_color="#1f77b4"))
        fig2.update_layout(template="plotly_white", height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    # 6. Tabel Data
    st.subheader("📋 Detail Data Mentah")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
