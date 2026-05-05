import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json
import os

# ==========================================
# KONFIGURASI DASAR & MANAJEMEN APLIKASI
# ==========================================
st.set_page_config(page_title="Dashboard KPI Aparatur", page_icon="📈", layout="wide")

CONFIG_FILE = "app_config.json"

# Fungsi membaca konfigurasi
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"title": "Sistem Evaluasi Aparatur", "theme": "Biru Elegan", "logo_path": ""}

# Fungsi menyimpan konfigurasi
def save_config(config_data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f)

config = load_config()

# Pemilihan Warna CSS berdasarkan Tema
theme_colors = {
    "Biru Elegan": ("#1e3a8a", "#2563eb", "#bfdbfe", "#3b82f6"),
    "Hijau Segar": ("#14532d", "#16a34a", "#bbf7d0", "#22c55e"),
    "Merah Berani": ("#7f1d1d", "#dc2626", "#fecaca", "#ef4444"),
    "Gelap Modern": ("#0f172a", "#334155", "#94a3b8", "#64748b")
}
c_dark, c_main, c_light, c_hover = theme_colors.get(config["theme"], theme_colors["Biru Elegan"])

# ==========================================
# INJEKSI CSS PREMIUM (Sesuai Tema Terpilih)
# ==========================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    [data-testid="stMetric"] {{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: fadeIn 0.5s ease-out;
    }}
    [data-testid="stMetric"]:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: {c_light};
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 16px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 36px;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, {c_dark}, {c_main});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .premium-header {{
        background: linear-gradient(90deg, {c_dark} 0%, {c_main} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }}
    .stButton>button {{
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
</style>
""", unsafe_allow_html=True)

# ID Google Sheets yang sudah disepakati
SHEET_ID = '1q9bqDXkXY1LvE4ywWWVHc_CYqd2iDwfe9uRMcvDrZg4'
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
STANDARD_KPIS = ["Kehadiran & Kedisiplinan", "Kualitas & Hasil Kerja", "Komunikasi & Kerjasama", "Inisiatif & Kreativitas", "Tanggung Jawab & Waktu"]
WEIGHT_PER_KPI = 0.20

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df.dropna(how='all')
    except Exception:
        return pd.DataFrame()

# ==========================================
# SIDEBAR: NAVIGASI MENU
# ==========================================
with st.sidebar:
    st.markdown(f"## 📱 Navigasi Sistem")
    menu_selection = st.radio("Pilih Halaman:", ["📊 Dashboard Utama", "⚙️ Pengaturan Tampilan"])
    st.markdown("---")
    st.markdown("[🔗 Kunjungi Repositori GitHub](https://github.com/edhproject-cmd/System-KPI)")
    st.markdown("---")
    
    if menu_selection == "📊 Dashboard Utama":
        st.markdown("### 🎛️ Filter Dasbor")
        df_temp = load_data()
        list_pengurus = []
        if not df_temp.empty:
            list_pengurus = [str(name).strip() for name in df_temp.iloc[:, 0].dropna().unique() if str(name).strip().lower() != 'nan']
        
        selected_pengurus = st.selectbox("🎯 Evaluasi Kinerja:", ["-- Papan Peringkat (Global) --"] + list_pengurus)
        
        if st.button("🔄 Perbarui Data Sekarang", use_container_width=True, type="primary"):
            st.cache_data.clear()
            st.rerun()

# ==========================================
# HALAMAN 1: DASHBOARD UTAMA
# ==========================================
if menu_selection == "📊 Dashboard Utama":
    
    # Render Logo & Judul Dinamis
    if config["logo_path"] and os.path.exists(config["logo_path"]):
        st.image(config["logo_path"], width=80)
        
    st.markdown(f'<h1 class="premium-header">{config["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #475569; font-size: 1.1rem; margin-top: -10px; margin-bottom: 30px;">Dashboard analitik HRD modern untuk pelacakan performa secara real-time.</p>', unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.warning("⚠️ Data kosong. Pastikan Anda sudah mengisi Google Sheets dengan format 1 Nama = 5 Skor KPI.")
    else:
        kpi_data = []
        for index, row in df.iterrows():
            try:
                nama_pengurus = str(row.iloc[0]).strip()
                if pd.isna(row.iloc[0]) or nama_pengurus.lower() == 'nan':
                    continue
                    
                scores = []
                for i in range(1, 6):
                    try:
                        score = int(row.iloc[i]) if not pd.isna(row.iloc[i]) else 0
                    except:
                        score = 0
                    scores.append(score)
                    
                for i in range(5):
                    final_val = WEIGHT_PER_KPI * scores[i]
                    kpi_data.append({
                        "Nama Pengurus": nama_pengurus,
                        "Indikator (KPI)": STANDARD_KPIS[i],
                        "Bobot": f"{WEIGHT_PER_KPI*100:.0f}%",
                        "Skor (1-5)": scores[i],
                        "Nilai Akhir": round(final_val, 2)
                    })
            except Exception:
                continue
                
        df_clean = pd.DataFrame(kpi_data)
        
        if not df_clean.empty:
            leaderboard = df_clean.groupby("Nama Pengurus")["Nilai Akhir"].sum().reset_index()
            leaderboard = leaderboard.sort_values(by="Nilai Akhir", ascending=False).reset_index(drop=True)
            leaderboard.index += 1
            
            if selected_pengurus == "-- Papan Peringkat (Global) --":
                st.markdown("### 🏆 Peringkat Kinerja Global")
                top_scorer = leaderboard.iloc[0]["Nama Pengurus"] if len(leaderboard) > 0 else "-"
                top_score = leaderboard.iloc[0]["Nilai Akhir"] if len(leaderboard) > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Total Pengurus Aktif", value=len(list_pengurus))
                with col2:
                    st.metric(label="Rata-rata Skor Divisi", value=f"{leaderboard['Nilai Akhir'].mean():.2f} / 5.0")
                with col3:
                    st.metric(label="Peraih Skor Tertinggi", value=top_scorer, delta=f"{top_score:.2f} Poin")
                    
                st.markdown("<br>", unsafe_allow_html=True)
                
                lb_col1, lb_col2 = st.columns([1, 1.2])
                with lb_col1:
                    st.markdown("##### Tabel Klasemen Akhir")
                    st.dataframe(leaderboard, use_container_width=True)
                with lb_col2:
                    st.markdown("##### Perbandingan Poin Antar Pengurus")
                    chart_global = leaderboard.set_index("Nama Pengurus")["Nilai Akhir"]
                    st.bar_chart(chart_global, color=c_main)
                    
            else:
                df_filtered = df_clean[df_clean["Nama Pengurus"] == selected_pengurus]
                total_score_individu = df_filtered["Nilai Akhir"].sum()
                
                st.markdown(f"### 📄 Rapor Kinerja: **{selected_pengurus}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Skor Kinerja Total", value=f"{total_score_individu:.2f} / 5.00")
                with col2:
                    sempurna = len(df_filtered[df_filtered["Skor (1-5)"] == 5])
                    st.metric(label="Aspek Bernilai Sempurna", value=sempurna, delta="Unggulan")
                with col3:
                    rata_rata = df_filtered["Skor (1-5)"].mean()
                    status = "Memuaskan" if rata_rata >= 4 else "Cukup" if rata_rata >= 3 else "Perlu Bimbingan"
                    st.metric(label="Status Kinerja", value=status)
                    
                st.markdown("<br>", unsafe_allow_html=True)
                
                viz_col1, viz_col2 = st.columns([1, 1.2])
                with viz_col1:
                    st.markdown("##### Rincian 5 Indikator HRD")
                    st.dataframe(df_filtered.drop(columns=["Nama Pengurus"]), use_container_width=True, hide_index=True)
                with viz_col2:
                    st.markdown("##### Analisis Kekuatan & Kelemahan")
                    chart_individu = df_filtered.set_index("Indikator (KPI)")["Skor (1-5)"]
                    st.bar_chart(chart_individu, color=c_main)

    st.markdown("---")
    st.markdown("### 📝 Live Data Editor (Input & Hapus Data)")
    st.caption("Ketik atau hapus data langsung di kotak di bawah ini. Semua akan tersimpan ke Google Drive Anda secara otomatis. **Pastikan klik tombol 'Perbarui Data Sekarang' di menu samping setelah selesai mengedit.**")

    EMBED_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit?rm=minimal"
    components.iframe(EMBED_URL, height=450, scrolling=True)


# ==========================================
# HALAMAN 2: PENGATURAN TAMPILAN (CMS)
# ==========================================
elif menu_selection == "⚙️ Pengaturan Tampilan":
    st.markdown(f'<h1 class="premium-header">⚙️ Panel Admin</h1>', unsafe_allow_html=True)
    st.markdown("Halaman khusus untuk mengonfigurasi estetika dan identitas dasbor Anda.")
    st.markdown("---")
    
    # 1. Ganti Judul
    st.subheader("1. 🏷️ Ganti Judul Aplikasi")
    new_title = st.text_input("Masukkan Judul Dasbor Baru:", value=config["title"])
    
    # 2. Ganti Tema
    st.subheader("2. 🎨 Ganti Tema Warna")
    tema_tersedia = list(theme_colors.keys())
    idx_tema_saat_ini = tema_tersedia.index(config["theme"]) if config["theme"] in tema_tersedia else 0
    new_theme = st.selectbox("Pilih Palet Warna:", tema_tersedia, index=idx_tema_saat_ini)
    
    # 3. Ganti Logo
    st.subheader("3. 🖼️ Ganti Logo Organisasi")
    st.caption("Unggah file gambar (PNG/JPG). Ukuran rasio 1:1 (persegi) direkomendasikan.")
    uploaded_logo = st.file_uploader("Pilih file gambar", type=["png", "jpg", "jpeg"])
    
    if st.button("💾 SIMPAN PENGATURAN", type="primary"):
        config["title"] = new_title
        config["theme"] = new_theme
        
        if uploaded_logo is not None:
            # Simpan file yang diupload secara lokal
            save_path = f"c:\\Users\\USer\\custom_logo_{uploaded_logo.name}"
            with open(save_path, "wb") as f:
                f.write(uploaded_logo.getbuffer())
            config["logo_path"] = save_path
            
        save_config(config)
        st.success("✅ Pengaturan berhasil disimpan! Silakan klik menu 'Dashboard Utama' di samping kiri untuk melihat perubahannya.")
