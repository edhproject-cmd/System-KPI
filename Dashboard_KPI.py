import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json
import os

# ==========================================
# KONSTANTA & KONFIGURASI GLOBAL
# ==========================================
CONFIG_FILE = "app_config.json"
SHEET_ID = '1q9bqDXkXY1LvE4ywWWVHc_CYqd2iDwfe9uRMcvDrZg4'
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
EMBED_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit?rm=minimal"

STANDARD_KPIS = [
    "Kehadiran & Kedisiplinan", 
    "Kualitas & Hasil Kerja", 
    "Komunikasi & Kerjasama", 
    "Inisiatif & Kreativitas", 
    "Tanggung Jawab & Waktu"
]
WEIGHT_PER_KPI = 0.20

THEME_COLORS = {
    "Biru Elegan": ("#1e3a8a", "#2563eb", "#bfdbfe", "#3b82f6"),
    "Hijau Segar": ("#14532d", "#16a34a", "#bbf7d0", "#22c55e"),
    "Merah Berani": ("#7f1d1d", "#dc2626", "#fecaca", "#ef4444"),
    "Gelap Modern": ("#0f172a", "#334155", "#94a3b8", "#64748b")
}

# ==========================================
# FUNGSI BANTUAN (HELPER FUNCTIONS)
# ==========================================
def load_config():
    """Membaca file konfigurasi lokal, mengembalikan konfigurasi default jika tidak ada."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"title": "Sistem Evaluasi Aparatur", "theme": "Biru Elegan", "logo_path": ""}

def save_config(config_data):
    """Menyimpan dictionary konfigurasi ke dalam file JSON."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f)

@st.cache_data
def fetch_kpi_data():
    """Mengunduh dan mengembalikan dataframe dari Google Sheets."""
    try:
        df = pd.read_csv(CSV_URL)
        return df.dropna(how='all')
    except Exception:
        return pd.DataFrame()

def apply_custom_css(theme_name):
    """Menyuntikkan kode CSS untuk tampilan Premium (Glassmorphism & Gradient)."""
    c_dark, c_main, c_light, c_hover = THEME_COLORS.get(theme_name, THEME_COLORS["Biru Elegan"])
    
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

def process_dataframe(df):
    """Memproses format raw (Wide Format) menjadi dataframe yang siap divisualisasikan."""
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
            
    return pd.DataFrame(kpi_data)

# ==========================================
# FUNGSI RENDER HALAMAN
# ==========================================
def render_dashboard(config, df_raw, c_main):
    """Menampilkan halaman utama Dashboard."""
    # Header
    if config.get("logo_path") and os.path.exists(config["logo_path"]):
        st.image(config["logo_path"], width=80)
        
    st.markdown(f'<h1 class="premium-header">{config["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #475569; font-size: 1.1rem; margin-top: -10px; margin-bottom: 30px;">Dashboard analitik HRD modern untuk pelacakan performa secara real-time.</p>', unsafe_allow_html=True)

    if df_raw.empty:
        st.warning("⚠️ Data kosong. Pastikan Anda sudah mengisi Google Sheets dengan format 1 Nama = 5 Skor KPI.")
        render_iframe_editor()
        return

    # Pemrosesan Data
    df_clean = process_dataframe(df_raw)
    if df_clean.empty:
        st.error("Gagal memproses data. Mohon pastikan Google Sheets Anda sudah diatur ke format 6 kolom.")
        render_iframe_editor()
        return

    # Persiapan Leaderboard
    leaderboard = df_clean.groupby("Nama Pengurus")["Nilai Akhir"].sum().reset_index()
    leaderboard = leaderboard.sort_values(by="Nilai Akhir", ascending=False).reset_index(drop=True)
    leaderboard.index += 1
    
    list_pengurus = df_clean["Nama Pengurus"].unique().tolist()
    
    # Filter Sidebar
    st.sidebar.markdown("### 🎛️ Filter Dasbor")
    selected_pengurus = st.sidebar.selectbox("🎯 Evaluasi Kinerja:", ["-- Papan Peringkat (Global) --"] + list_pengurus)
    
    if st.sidebar.button("🔄 Perbarui Data Sekarang", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()

    # Logika Tampilan (Global vs Individu)
    if selected_pengurus == "-- Papan Peringkat (Global) --":
        render_global_view(leaderboard, list_pengurus, c_main)
    else:
        render_individual_view(df_clean, selected_pengurus, c_main)

    render_iframe_editor()

def render_global_view(leaderboard, list_pengurus, c_main):
    """Menampilkan papan peringkat gabungan."""
    st.markdown("### 🏆 Peringkat Kinerja Global")
    top_scorer = leaderboard.iloc[0]["Nama Pengurus"] if not leaderboard.empty else "-"
    top_score = leaderboard.iloc[0]["Nilai Akhir"] if not leaderboard.empty else 0
    
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
        st.markdown("##### 📈 Statistik Distribusi Kinerja")
        
        # Kalkulasi Statistik Divisi
        mean_score = leaderboard['Nilai Akhir'].mean()
        median_score = leaderboard['Nilai Akhir'].median()
        max_score = leaderboard['Nilai Akhir'].max()
        min_score = leaderboard['Nilai Akhir'].min()
        
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.info(f"**Rata-rata (Mean):** {mean_score:.2f}")
            st.info(f"**Nilai Tengah (Median):** {median_score:.2f}")
        with stat_col2:
            st.success(f"**Skor Tertinggi:** {max_score:.2f}")
            st.error(f"**Skor Terendah:** {min_score:.2f}")
            
        st.markdown("##### 📊 Tren Statistik")
        # Menggunakan Area Chart sebagai representasi tren statistik (bukan sekadar batang)
        st.area_chart(leaderboard.set_index("Nama Pengurus")["Nilai Akhir"], color=c_main)

def render_individual_view(df_clean, selected_pengurus, c_main):
    """Menampilkan rapor kinerja individu spesifik."""
    df_filtered = df_clean[df_clean["Nama Pengurus"] == selected_pengurus]
    total_score = df_filtered["Nilai Akhir"].sum()
    
    st.markdown(f"### 📄 Rapor Kinerja: **{selected_pengurus}**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Skor Kinerja Total", value=f"{total_score:.2f} / 5.00")
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
        st.markdown("##### 🎯 Analisis Statistik Individu")
        
        # Kalkulasi Kekuatan & Kelemahan
        idx_max = df_filtered["Skor (1-5)"].idxmax()
        idx_min = df_filtered["Skor (1-5)"].idxmin()
        
        kekuatan = df_filtered.loc[idx_max, "Indikator (KPI)"]
        kelemahan = df_filtered.loc[idx_min, "Indikator (KPI)"]
        
        # Menghitung Standar Deviasi (Konsistensi)
        std_dev = df_filtered["Skor (1-5)"].std()
        konsistensi = "Sangat Konsisten" if std_dev < 1.0 else "Kurang Konsisten"
        
        st.success(f"**⭐ Kekuatan Utama:** {kekuatan} (Skor: {df_filtered.loc[idx_max, 'Skor (1-5)']})")
        st.warning(f"**⚠️ Area Perbaikan:** {kelemahan} (Skor: {df_filtered.loc[idx_min, 'Skor (1-5)']})")
        st.info(f"**📊 Tingkat Konsistensi:** {konsistensi} (Standar Deviasi: {std_dev:.2f})")
        
        # Menampilkan line chart sebagai profil distribusi statistik
        st.line_chart(df_filtered.set_index("Indikator (KPI)")["Skor (1-5)"], color=c_main)

def render_iframe_editor():
    """Menampilkan jendela editor Google Sheets di bagian bawah."""
    st.markdown("---")
    st.markdown("### 📝 Live Data Editor (Input & Hapus Data)")
    st.caption("Ketik atau hapus data langsung di kotak di bawah ini. Semua akan tersimpan ke Google Drive Anda secara otomatis. **Pastikan klik tombol 'Perbarui Data Sekarang' di menu samping setelah selesai mengedit.**")
    components.iframe(EMBED_URL, height=450, scrolling=True)

def render_settings(config):
    """Menampilkan halaman pengaturan aplikasi (CMS)."""
    st.markdown('<h1 class="premium-header">⚙️ Panel Admin</h1>', unsafe_allow_html=True)
    st.markdown("Halaman khusus untuk mengonfigurasi estetika dan identitas dasbor Anda.")
    st.markdown("---")
    
    st.subheader("1. 🏷️ Ganti Judul Aplikasi")
    new_title = st.text_input("Masukkan Judul Dasbor Baru:", value=config.get("title", ""))
    
    st.subheader("2. 🎨 Ganti Tema Warna")
    tema_tersedia = list(THEME_COLORS.keys())
    idx_tema_saat_ini = tema_tersedia.index(config["theme"]) if config.get("theme") in tema_tersedia else 0
    new_theme = st.selectbox("Pilih Palet Warna:", tema_tersedia, index=idx_tema_saat_ini)
    
    st.subheader("3. 🖼️ Ganti Logo Organisasi")
    st.caption("Unggah file gambar (PNG/JPG). Ukuran rasio 1:1 (persegi) direkomendasikan.")
    uploaded_logo = st.file_uploader("Pilih file gambar", type=["png", "jpg", "jpeg"])
    
    if st.button("💾 SIMPAN PENGATURAN", type="primary"):
        config["title"] = new_title
        config["theme"] = new_theme
        
        if uploaded_logo is not None:
            # BUGFIX Cloud-Ready: Simpan file sebagai path relatif agar bisa di-hosting di manapun
            save_path = f"custom_logo_{uploaded_logo.name}"
            with open(save_path, "wb") as f:
                f.write(uploaded_logo.getbuffer())
            config["logo_path"] = save_path
            
        save_config(config)
        st.success("✅ Pengaturan berhasil disimpan! Silakan klik menu 'Dashboard Utama' di samping kiri untuk melihat perubahannya.")

# ==========================================
# MAIN EXECUTION (ENTRY POINT)
# ==========================================
def main():
    st.set_page_config(page_title="Dashboard KPI Aparatur", page_icon="📈", layout="wide")
    
    config = load_config()
    apply_custom_css(config.get("theme", "Biru Elegan"))
    
    # Ambil warna primary untuk komponen Chart
    _, c_main, _, _ = THEME_COLORS.get(config.get("theme", "Biru Elegan"), THEME_COLORS["Biru Elegan"])

    # Navigasi Sidebar
    with st.sidebar:
        st.markdown("## 📱 Navigasi Sistem")
        menu_selection = st.radio("Pilih Halaman:", ["📊 Dashboard Utama", "⚙️ Pengaturan Tampilan"])
        st.markdown("---")
        # Catatan: Link repositori GitHub telah dihapus berdasarkan permintaan

    if menu_selection == "📊 Dashboard Utama":
        df_raw = fetch_kpi_data()
        render_dashboard(config, df_raw, c_main)
    elif menu_selection == "⚙️ Pengaturan Tampilan":
        render_settings(config)

if __name__ == "__main__":
    main()
