import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Konfigurasi Halaman (Wide Layout)
st.set_page_config(page_title="Estimasi Stok Ikan Laut Jawa", layout="wide")

# 2. CSS untuk Tampilan Profesional
st.markdown("""
    <style>
    .header-box { background: linear-gradient(135deg, #001f3f, #0074D9); padding: 25px; border-radius: 15px; color: white; margin-bottom: 25px; }
    .info-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #0074D9; color: #333; }
    h1 { margin: 0; }
    </style>
""", unsafe_allow_html=True)

# 3. Header dengan Informasi Tetap
with st.container():
    st.markdown('<div class="header-box"><h1>Estimasi Stok Ikan Laut Jawa</h1><h3>PBL 5 — Ekonomi Sumber Daya Ikan</h3></div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 👥 KELOMPOK 4")
        st.write("• **Salsa Zahratul Aulia** (10090224004)")
        st.write("• **Aida Farida Kultsum** (10090224014)")
        st.write("• **Nabil Athala Naufal** (10090224022)")
    with col_b:
        st.markdown('<div class="info-card"><b>Mata Kuliah:</b> Ekonomi Sumber Daya Alam dan Lingkungan<br>'
                    '<b>Dosen Pengampu:</b> Yuhka Sundaya, S.E., M.Si.</div>', unsafe_allow_html=True)

st.markdown("---")

# 4. Fungsi Data (Pembersihan Otomatis)
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("2026-06-16T05-00_export.csv")
    if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
    order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]
    df['Bulan'] = pd.Categorical(df['Bulan'], categories=order, ordered=True)
    return df.sort_values('Bulan')

df = load_data()

# 5. Dashboard Utama
st.subheader("📊 Analisis Data Oseanografi & Biomassa")
c1, c2 = st.columns([2, 1])

with c1:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Suhu_Laut_C"], name="Suhu (°C)", mode='lines+markers', line=dict(color="#FF4136", width=3)), secondary_y=False)
    fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Klorofil_a"], name="Klorofil (mg/m³)", mode='lines+markers', line=dict(color="#2ECC40", width=3, dash="dot")), secondary_y=True)
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20), height=400)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.metric("Total Estimasi Stok", f"{df['Estimasi_Stok'].sum():,.0f} Ton")
    fig2 = go.Figure(go.Bar(x=df["Bulan"], y=df["Estimasi_Stok"], marker_color="#0074D9"))
    fig2.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20), height=300)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📋 Detail Data")
st.dataframe(df, use_container_width=True)
