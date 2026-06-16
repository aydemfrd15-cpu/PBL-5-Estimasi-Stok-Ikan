import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Estimasi Stok Ikan Laut Jawa", layout="wide", page_icon="🐟")

# CSS Dinamis
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
    .param-box {
        background-color: var(--secondary-background-color);
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #0077b6;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("📥 Data Input")
    uploaded_file = st.file_uploader("Unggah data GEE (.csv)", type=["csv"])
    
    st.markdown("---")
    st.header("⚙️ Parameter Analisis")
    
    # Pengaturan Model dengan Slider
    suhu_optimal = st.slider("Suhu Optimal (°C)", 20.0, 35.0, 28.50)
    faktor_klorofil = st.slider("Faktor Klorofil (α)", 1000, 5000, 3000)
    faktor_penalti = st.slider("Faktor Penalti (β)", 100, 1000, 500)
    
    # Grid Parameter Live
    st.write("")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown(f'<div class="param-box"><b>Suhu Opt.</b><br>{suhu_optimal} °C</div>', unsafe_allow_html=True)
    with col_p2:
        st.markdown(f'<div class="param-box"><b>Klorofil α</b><br>{faktor_klorofil}</div>', unsafe_allow_html=True)

# --- MAIN CONTENT ---
with st.container():
    col_logo, col_text = st.columns([1, 6])
    with col_logo:
        if os.path.exists("Logo Unisbaa.png"):
            st.image("Logo Unisbaa.png", width=110)
    with col_text:
        st.markdown('<div class="main-header"><h1>Estimasi Stok Ikan Laut Jawa</h1><h4>PBL 5 — Ekonomi Sumber Daya Ikan</h4></div>', unsafe_allow_html=True)

    col_kiri, col_kanan = st.columns([1, 1])
    with col_kiri:
        st.markdown("### 👥 Kelompok 4")
        st.write("• **Salsa Zahratul Aulia** (10090224004)")
        st.write("• **Aida Farida Kultsum** (10090224014)")
        st.write("• **Nabil Athala Naufal** (10090224022)")
    with col_kanan:
        st.markdown('<div class="info-card"><b>Mata Kuliah:</b> Ekonomi Sumber Daya Alam dan Lingkungan<br>'
                    '<b>Dosen Pengampu:</b> Yuhka Sundaya, S.E., M.Si.</div>', unsafe_allow_html=True)

st.markdown("---")

def get_data(file_obj):
    if file_obj is not None:
        # Membaca file CSV yang diunggah
        df = pd.read_csv(file_obj)
        # Menyesuaikan nama kolom sesuai dengan file yang Anda unggah
        # Asumsi: kolom suhu adalah 'C' dan klorofil adalah 'Clorophyll'
        df = df.rename(columns={'C': 'Suhu_Laut_C', 'Clorophyll': 'Klorofil_a'})
        # Membuat label bulan dummy jika belum ada
        df['Bulan'] = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]
        return df
    return pd.DataFrame()

df = get_data(uploaded_file)

if not df.empty:
    # LOGIKA PERHITUNGAN DINAMIS
    # Stok = (Klorofil * α) - (Selisih Suhu * β)
    selisih_suhu = abs(df["Suhu_Laut_C"] - suhu_optimal)
    df["Estimasi_Stok"] = (df["Klorofil_a"] * faktor_klorofil) - (selisih_suhu * faktor_penalti)
    
    col1, col2 = st.columns([2.5, 1.5]) 

    with col1:
        st.subheader("📊 Analisis Oseanografi")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Suhu_Laut_C"], name="Suhu (°C)", line=dict(color="#FF4136", width=3)), secondary_y=False)
        fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Klorofil_a"], name="Klorofil", line=dict(color="#2ECC40", width=3, dash="dot")), secondary_y=True)
        fig.update_layout(template=None, height=400, margin=dict(l=40, r=40, t=30, b=80), legend=dict(orientation="h", y=-0.3))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📈 Estimasi Stok")
        st.metric("Stok Puncak", f"{df['Estimasi_Stok'].max():,.0f} Ton")
        fig2 = go.Figure(go.Bar(x=df["Bulan"], y=df["Estimasi_Stok"], marker_color="#0077b6"))
        fig2.update_layout(template=None, height=300, margin=dict(l=60, r=20, t=20, b=80)) 
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📋 Lihat Detail Data Mentah"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("Silakan unggah file CSV 'SST and Clorophyll' untuk memulai analisis.")
