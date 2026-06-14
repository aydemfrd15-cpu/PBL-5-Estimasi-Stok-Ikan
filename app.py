import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Konfigurasi Halaman
st.set_page_config(page_title="PBL 5 - Estimasi Stok Ikan", layout="wide")

# CSS untuk desain profesional
st.markdown("""
    <style>
    .main-header {background: linear-gradient(90deg, #004a99 0%, #0077b6 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 20px;}
    .info-box {background-color: rgba(0, 74, 153, 0.05); padding: 15px; border-radius: 10px; border-left: 5px solid #004a99;}
    </style>
""", unsafe_html=True)

# Header
with st.container():
    st.markdown("""<div class="main-header">
        <h1 style="text-align: center;">Estimasi Stok Ikan Laut Jawa</h1>
        <h3 style="text-align: center;">PBL 5 — Ekonomi Sumber Daya Ikan</h3>
    </div>""", unsafe_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👥 Kelompok 4")
        st.write("• **Salsa Zahratul Aulia** (10090224004)")
        st.write("• **Aida Farida Kultsum** (10090224014)")
        st.write("• **Nabil Athala Naufal** (10090224022)")
    with col2:
        st.markdown("### 🎓 Informasi Akademik")
        st.markdown('<div class="info-box"><b>Mata Kuliah:</b> Ekonomi Sumber Daya Alam dan Lingkungan<br>'
                    '<b>Dosen Pengampu:</b> YUHKA SUNDAYA, S.E., M.Si.</div>', unsafe_html=True)

st.markdown("---")

# Sidebar
# Menambahkan logo kampus
st.sidebar.image("Logo Unisbaa.png", width=200)
st.sidebar.header("⚙️ Konfigurasi Model")
suhu = st.sidebar.slider("Suhu Laut (°C)", 25.0, 32.0, 29.5)
klorofil = st.sidebar.slider("Klorofil-a (mg/m³)", 0.1, 1.0, 0.37)
mangrove = st.sidebar.number_input("Luas Mangrove (Ha)", value=207028)
terumbu = st.sidebar.number_input("Luas Terumbu Karang (Ha)", value=50000)
st.sidebar.markdown("---")
p = st.sidebar.slider("Harga Jual (Rp/kg)", 10000, 50000, 25000)
c = st.sidebar.slider("Biaya per Unit Effort (Juta Rp)", 100, 2000, 500)

# Logika Hitung
def hitung_stok(suhu, klorofil, m, tk):
    K = 850000 + (m * 0.5) + (tk * 0.8)
    efek_lingkungan = np.exp(-0.5 * ((suhu - 29) / 2)**2) * (1 + (klorofil * 2))
    return K * efek_lingkungan

K_aktual = hitung_stok(suhu, klorofil, mangrove, terumbu)
r, q = 0.6, 0.00001 

@st.cache_data
def get_data():
    return pd.DataFrame({
        "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt"],
        "Suhu": [28.9, 28.4, 29.6, 29.5, 30.3, 30.3, 29.1, 28.8, 28.5, 29.0],
        "Klorofil": [0.39, 0.27, 0.31, 0.26, 0.35, 0.30, 0.24, 0.46, 0.35, 0.30]
    })

data = get_data()
data["Estimasi Stok (Ton)"] = data.apply(lambda x: hitung_stok(x["Suhu"], x["Klorofil"], mangrove, terumbu), axis=1)

# Dashboard Grafik
st.subheader("📊 Analisis Oseanografi & Prediksi Biomassa")
col1, col2 = st.columns([1, 1])

with col1:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data["Bulan"], y=data["Suhu"], name="Suhu (°C)", line=dict(color='#EF553B')), secondary_y=False)
    fig.add_trace(go.Scatter(x=data["Bulan"], y=data["Klorofil"], name="Klorofil", line=dict(color='#00CC96')), secondary_y=True)
    fig.update_layout(template="plotly") 
    # Perbaikan: Mengganti use_container_width dengan width='100%' sesuai aturan terbaru
    st.plotly_chart(fig, width='100%')

with col2:
    fig2 = go.Figure(go.Bar(x=data["Bulan"], y=data["Estimasi Stok (Ton)"], marker_color='#636EFA'))
    fig2.update_layout(template="plotly")
    st.plotly_chart(fig2, width='100%')

st.subheader("📋 Data Satelit vs Estimasi Stok Ikan")
# Perbaikan: Menggunakan st.dataframe dengan argumen width yang tepat
st.dataframe(data.style.format({"Estimasi Stok (Ton)": "{:,.0f}"}), width=1000)

st.markdown("---")

# Simulasi
st.subheader("🧪 Simulasi Bioekonomi Gordon-Schaefer")
E = np.linspace(0, 100000, 200)
Y = q * E * K_aktual * (1 - (q * E / r))
TR = (p * Y * 1000) / 1e9
TC = (c * E) / 1000

fig_bio = go.Figure()
fig_bio.add_trace(go.Scatter(x=E, y=TR, name="Total Revenue", line=dict(width=4, color='#AB63FA')))
fig_bio.add_trace(go.Scatter(x=E, y=TC, name="Total Cost", line=dict(width=4, dash='dash', color='#FFA15A')))
fig_bio.update_layout(xaxis_title="Upaya (Trip)", yaxis_title="Nilai (Miliar Rp)", template="plotly")
st.plotly_chart(fig_bio, width='100%')

st.info(f"Estimasi Stok Ikan Laut Jawa: {int(K_aktual):,} Ton.")