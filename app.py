import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- KONFIGURASI PAGE ---
st.set_page_config(page_title="PBL 5 - Estimasi Stok Ikan", layout="wide")

# --- CSS CUSTOM UNTUK TAMPILAN PROFESIONAL ---
st.markdown("""
    <style>
    .main-header {background: linear-gradient(90deg, #004a99 0%, #0077b6 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 20px;}
    .stat-card {background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #004a99;}
    .academic-info {line-height: 1.6; font-size: 1.1em;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
with st.container():
    st.markdown("""<div class="main-header">
        <h1 style="text-align: center;">Estimasi Stok Ikan Laut Jawa</h1>
        <h3 style="text-align: center;">PBL 5 — Ekonomi Sumber Daya Ikan</h3>
    </div>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### **KELOMPOK 4**")
        st.markdown("• Salsa Zahratul Aulia (10090224004)<br>• Aida Farida Kultsum (10090224014)<br>• Nabil Athala Naufal (10090224022)", unsafe_allow_html=True)
    with col2:
        st.markdown("### **Informasi Akademik**")
        st.markdown('<div class="academic-info"><b>Mata Kuliah:</b> Ekonomi Sumber Daya Alam dan Lingkungan<br>'
                    '<b>Dosen Pengampu:</b> YUHKA SUNDAYA, S.E., M.Si.</div>', unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Konfigurasi Model")
suhu = st.sidebar.slider("Suhu Laut (°C)", 25.0, 32.0, 29.5)
klorofil = st.sidebar.slider("Klorofil-a (mg/m³)", 0.1, 1.0, 0.37)
mangrove = st.sidebar.number_input("Luas Mangrove (Ha)", value=207028)
terumbu = st.sidebar.number_input("Luas Terumbu Karang (Ha)", value=50000)
st.sidebar.markdown("---")
p = st.sidebar.slider("Harga Jual (Rp/kg)", 10000, 50000, 25000)
c = st.sidebar.slider("Biaya per Unit Effort (Juta Rp)", 100, 2000, 500)

# --- LOGIKA MODEL ---
def hitung_stok(suhu, klorofil, m, tk):
    K = 850000 + (m * 0.5) + (tk * 0.8)
    efek_lingkungan = np.exp(-0.5 * ((suhu - 29) / 2)**2) * (1 + (klorofil * 2))
    return K * efek_lingkungan

K_aktual = hitung_stok(suhu, klorofil, mangrove, terumbu)
r, q = 0.6, 0.00001 

# --- DATA ---
@st.cache_data
def get_data():
    return pd.DataFrame({
        "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt"],
        "Suhu": [28.9, 28.4, 29.6, 29.5, 30.3, 30.3, 29.1, 28.8, 28.5, 29.0],
        "Klorofil": [0.39, 0.27, 0.31, 0.26, 0.35, 0.30, 0.24, 0.46, 0.35, 0.30]
    })

data = get_data()
data["Estimasi Stok (Ton)"] = data.apply(lambda x: hitung_stok(x["Suhu"], x["Klorofil"], mangrove, terumbu), axis=1)

# --- DASHBOARD LAYOUT ---
st.subheader("📊 Analisis Oseanografi & Prediksi Biomassa")
col1, col2 = st.columns([1, 1])

with col1:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data["Bulan"], y=data["Suhu"], name="Suhu (°C)", line=dict(color='#d62828')), secondary_y=False)
    fig.add_trace(go.Scatter(x=data["Bulan"], y=data["Klorofil"], name="Klorofil", line=dict(color='#006d77')), secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = go.Figure(go.Bar(x=data["Bulan"], y=data["Estimasi Stok (Ton)"], marker_color='#264653'))
    st.plotly_chart(fig2, use_container_width=True)

# Tambahan Tabel Data Satelit vs Estimasi Stok
st.subheader("📋 Data Satelit vs Estimasi Stok Ikan")
st.dataframe(data.style.format({"Estimasi Stok (Ton)": "{:,.0f}"}), use_container_width=True)

st.markdown("---")

# --- SIMULASI BIOEKONOMI ---
st.subheader("🧪 Simulasi Bioekonomi Gordon-Schaefer")
E = np.linspace(0, 100000, 200)
Y = q * E * K_aktual * (1 - (q * E / r))
TR = (p * Y * 1000) / 1e9
TC = (c * E) / 1000

fig_bio = go.Figure()
fig_bio.add_trace(go.Scatter(x=E, y=TR, name="Total Revenue (Miliar Rp)", line=dict(width=4)))
fig_bio.add_trace(go.Scatter(x=E, y=TC, name="Total Cost (Miliar Rp)", line=dict(width=4, dash='dash')))
fig_bio.update_layout(xaxis_title="Upaya (Trip)", yaxis_title="Nilai (Miliar Rp)")
st.plotly_chart(fig_bio, use_container_width=True)

st.info(f"Estimasi Stok Ikan Laut Jawa: {int(K_aktual):,} Ton. Kapasitas ini sangat dipengaruhi oleh kelestarian ekosistem Mangrove & Terumbu Karang.")