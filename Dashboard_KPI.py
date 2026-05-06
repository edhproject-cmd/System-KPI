import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json
import os
import datetime

# ==========================================
# KONSTANTA & KONFIGURASI GLOBAL
# ==========================================
CONFIG_FILE = "app_config.json"
SHEET_ID = '1q9bqDXkXY1LvE4ywWWVHc_CYqd2iDwfe9uRMcvDrZg4'
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

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
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"title": "Sistem Evaluasi Aparatur", "theme": "Biru Elegan", "logo_path": ""}

def save_config(config_data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f)

@st.cache_data(ttl=10)
def fetch_kpi_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df.dropna(how='all')
    except Exception:
        return pd.DataFrame()

def apply_custom_css(theme_name):
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
        }}
    </style>
    """, unsafe_allow_html=True)

def process_dataframe(df):
    """Memproses format Time-Series (Tanggal | Nama | KPI 1-5)."""
    kpi_data = []
    for index, row in df.iterrows():
        try:
            raw_date = row.iloc[0]
            if pd.isna(raw_date): continue
            
            try:
                tanggal = pd.to_datetime(raw_date).date()
            except:
                continue # Skip invalid dates
                
            nama_pengurus = str(row.iloc[1]).strip()
            if pd.isna(row.iloc[1]) or nama_pengurus.lower() == 'nan': continue
                
            scores = []
            total_akhir = 0
            for i in range(2, 7):
                try:
                    score = int(row.iloc[i]) if not pd.isna(row.iloc[i]) else 0
                except:
                    score = 0
                scores.append(score)
                total_akhir += (score * WEIGHT_PER_KPI)
                
            kpi_data.append({
                "Tanggal": tanggal,
                "Nama Pengurus": nama_pengurus,
                STANDARD_KPIS[0]: scores[0],
                STANDARD_KPIS[1]: scores[1],
                STANDARD_KPIS[2]: scores[2],
                STANDARD_KPIS[3]: scores[3],
                STANDARD_KPIS[4]: scores[4],
                "Nilai Akhir": round(total_akhir, 2)
            })
        except Exception:
            continue
            
    return pd.DataFrame(kpi_data)

# ==========================================
# FUNGSI RENDER HALAMAN
# ==========================================
def render_dashboard(config, df_raw, c_main, time_filter):
    if config.get("logo_path") and os.path.exists(config.get("logo_path")):
        st.image(config["logo_path"], width=80)
        
    st.markdown(f'<h1 class="premium-header">{config["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #475569; font-size: 1.1rem; margin-top: -10px; margin-bottom: 30px;">' + config.get("subtitle", "Dashboard analitik HRD modern untuk pelacakan performa dari waktu ke waktu.") + '</p>', unsafe_allow_html=True)

    if df_raw.empty:
        st.warning("⚠️ Data kosong atau Kolom 'Tanggal' belum ditambahkan di Google Sheets.")
        return

    df_clean = process_dataframe(df_raw)
    if df_clean.empty:
        st.error("Gagal memproses data. Pastikan format 7 Kolom: [Tanggal] | [Nama] | [KPI 1] s/d [KPI 5]")
        return

    # Menerapkan Filter Waktu
    today = datetime.date.today()
    start_date = None
    if time_filter == "1 Minggu Terakhir":
        start_date = today - datetime.timedelta(days=7)
    elif time_filter == "2 Minggu Terakhir":
        start_date = today - datetime.timedelta(days=14)
    elif time_filter == "1 Bulan Terakhir":
        start_date = (pd.to_datetime(today) - pd.DateOffset(months=1)).date()
    elif time_filter == "3 Bulan Terakhir":
        start_date = (pd.to_datetime(today) - pd.DateOffset(months=3)).date()
    elif time_filter == "6 Bulan Terakhir":
        start_date = (pd.to_datetime(today) - pd.DateOffset(months=6)).date()
    elif time_filter == "1 Tahun Terakhir":
        start_date = (pd.to_datetime(today) - pd.DateOffset(years=1)).date()
        
    if start_date:
        df_clean = df_clean[df_clean["Tanggal"] >= start_date]
        if df_clean.empty:
            st.info(f"Tidak ada data evaluasi pada rentang waktu: {time_filter}.")
            return

    list_pengurus = df_clean["Nama Pengurus"].unique().tolist()
    
    st.sidebar.markdown("### 🎛️ Filter Pengurus")
    selected_pengurus = st.sidebar.selectbox("🎯 Evaluasi Kinerja:", ["-- Papan Peringkat (Global) --"] + list_pengurus)
    
    if selected_pengurus == "-- Papan Peringkat (Global) --":
        render_global_view(df_clean, list_pengurus, c_main, config)
    else:
        render_individual_view(df_clean, selected_pengurus, c_main, config)

def render_global_view(df_clean, list_pengurus, c_main, config):
    # Hitung Rata-rata Skor per Pengurus selama rentang waktu
    leaderboard = df_clean.groupby("Nama Pengurus")["Nilai Akhir"].mean().reset_index()
    leaderboard["Nilai Akhir"] = leaderboard["Nilai Akhir"].round(2)
    leaderboard = leaderboard.sort_values(by="Nilai Akhir", ascending=False).reset_index(drop=True)
    leaderboard.index += 1
    
    st.markdown(f"### 🏆 {config.get('title_global', 'Peringkat Kinerja Global (Rata-rata)')}")
    top_scorer = leaderboard.iloc[0]["Nama Pengurus"] if not leaderboard.empty else "-"
    top_score = leaderboard.iloc[0]["Nilai Akhir"] if not leaderboard.empty else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Pengurus Aktif", value=len(list_pengurus))
    with col2:
        st.metric(label="Rata-rata Skor Divisi", value=f"{leaderboard['Nilai Akhir'].mean():.2f} / 5.0")
    with col3:
        st.metric(label="Peraih Skor Tertinggi", value=top_scorer, delta=f"{top_score:.2f} Poin")
        
    st.markdown("---")
    st.markdown(f"### 🏅 {config.get('title_podium', 'Podium Top 3 Pengurus Terbaik')}")
    
    podium_col1, podium_col2, podium_col3 = st.columns(3)
    
    if len(leaderboard) >= 1:
        with podium_col1:
            st.success(f"**🥇 Juara 1**\n### {leaderboard.iloc[0]['Nama Pengurus']}\n**Skor:** {leaderboard.iloc[0]['Nilai Akhir']:.2f}")
    if len(leaderboard) >= 2:
        with podium_col2:
            st.info(f"**🥈 Juara 2**\n### {leaderboard.iloc[1]['Nama Pengurus']}\n**Skor:** {leaderboard.iloc[1]['Nilai Akhir']:.2f}")
    if len(leaderboard) >= 3:
        with podium_col3:
            st.warning(f"**🥉 Juara 3**\n### {leaderboard.iloc[2]['Nama Pengurus']}\n**Skor:** {leaderboard.iloc[2]['Nilai Akhir']:.2f}")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    lb_col1, lb_col2 = st.columns([1, 1.2])
    with lb_col1:
        st.markdown(f"##### {config.get('title_table', 'Tabel Klasemen Akhir')}")
        st.dataframe(leaderboard, use_container_width=True)
    with lb_col2:
        st.markdown(f"##### 📈 {config.get('title_trend', 'Tren Performa Divisi (Rata-rata Harian)')}")
        trend_divisi = df_clean.groupby("Tanggal")["Nilai Akhir"].mean().reset_index()
        st.line_chart(trend_divisi.set_index("Tanggal")["Nilai Akhir"], color=c_main)

def render_individual_view(df_clean, selected_pengurus, c_main, config):
    df_filtered = df_clean[df_clean["Nama Pengurus"] == selected_pengurus].sort_values("Tanggal")
    
    # Ambil evaluasi terbaru dan sebelumnya (jika ada) untuk mengukur naik/turun
    latest_eval = df_filtered.iloc[-1]
    
    delta_str = "Evaluasi Perdana"
    if len(df_filtered) > 1:
        prev_eval = df_filtered.iloc[-2]
        delta_val = latest_eval['Nilai Akhir'] - prev_eval['Nilai Akhir']
        delta_str = f"{delta_val:+.2f} vs periode lalu"
        
    st.markdown(f"### 📄 {config.get('title_indiv', 'Rapor Kinerja')}: **{selected_pengurus}**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Skor Kinerja Terkini", value=f"{latest_eval['Nilai Akhir']:.2f} / 5.00", delta=delta_str)
    with col2:
        st.metric(label="Total Evaluasi", value=len(df_filtered), delta="Rekam Jejak")
    with col3:
        rata_rata = df_filtered["Nilai Akhir"].mean()
        status = "Konsisten Baik" if rata_rata >= 4 else "Fluktuatif/Cukup" if rata_rata >= 3 else "Perlu Bimbingan"
        st.metric(label="Status Kinerja", value=status)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    viz_col1, viz_col2 = st.columns([1, 1.2])
    with viz_col1:
        st.markdown("##### Riwayat Nilai Akhir")
        st.dataframe(df_filtered[["Tanggal", "Nilai Akhir"]].set_index("Tanggal"), use_container_width=True)
    with viz_col2:
        st.markdown("##### 📈 Tren Kinerja (Line Chart)")
        chart_data = df_filtered.set_index("Tanggal")[["Nilai Akhir"]]
        st.line_chart(chart_data, color=c_main)

def render_settings(config):
    st.markdown('<h1 class="premium-header">⚙️ Panel Admin</h1>', unsafe_allow_html=True)
    st.markdown("Halaman khusus untuk mengonfigurasi estetika dan identitas dasbor Anda.")
    st.markdown("---")
    
    new_title = st.text_input("1. 🏷️ Ganti Judul Utama Aplikasi:", value=config.get("title", ""))
    
    with st.expander("📝 Sesuaikan Teks & Sub-judul Dasbor"):
        new_subtitle = st.text_input("Deskripsi Dasbor (Bawah Judul):", value=config.get("subtitle", "Dashboard analitik HRD modern untuk pelacakan performa dari waktu ke waktu."))
        new_title_global = st.text_input("Sub-judul Peringkat Global:", value=config.get("title_global", "Peringkat Kinerja Global (Rata-rata)"))
        new_title_podium = st.text_input("Sub-judul Podium Top 3:", value=config.get("title_podium", "Podium Top 3 Pengurus Terbaik"))
        new_title_table = st.text_input("Sub-judul Tabel Klasemen:", value=config.get("title_table", "Tabel Klasemen Akhir"))
        new_title_trend = st.text_input("Sub-judul Tren Global:", value=config.get("title_trend", "Tren Performa Divisi (Rata-rata Harian)"))
        new_title_indiv = st.text_input("Sub-judul Rapor Individu:", value=config.get("title_indiv", "Rapor Kinerja"))
    
    tema_tersedia = list(THEME_COLORS.keys())
    idx_tema_saat_ini = tema_tersedia.index(config["theme"]) if config.get("theme") in tema_tersedia else 0
    new_theme = st.selectbox("2. 🎨 Ganti Tema Warna:", tema_tersedia, index=idx_tema_saat_ini)
    
    st.caption("3. 🖼️ Ganti Logo Organisasi (PNG/JPG Rasio 1:1)")
    uploaded_logo = st.file_uploader("Pilih file gambar", type=["png", "jpg", "jpeg"])
    
    if st.button("💾 SIMPAN PENGATURAN", type="primary"):
        config["title"] = new_title
        config["subtitle"] = new_subtitle
        config["title_global"] = new_title_global
        config["title_podium"] = new_title_podium
        config["title_table"] = new_title_table
        config["title_trend"] = new_title_trend
        config["title_indiv"] = new_title_indiv
        config["theme"] = new_theme
        if uploaded_logo is not None:
            save_path = f"custom_logo_{uploaded_logo.name}"
            with open(save_path, "wb") as f:
                f.write(uploaded_logo.getbuffer())
            config["logo_path"] = save_path
        save_config(config)
        st.success("✅ Pengaturan berhasil disimpan!")

# ==========================================
# MAIN EXECUTION (ENTRY POINT)
# ==========================================
def main():
    st.set_page_config(page_title="Dashboard KPI Aparatur", page_icon="📈", layout="wide")
    
    config = load_config()
    apply_custom_css(config.get("theme", "Biru Elegan"))
    _, c_main, _, _ = THEME_COLORS.get(config.get("theme", "Biru Elegan"), THEME_COLORS["Biru Elegan"])

    with st.sidebar:
        st.markdown("## 📱 Navigasi Sistem")
        menu_selection = st.radio("Pilih Halaman:", ["📊 Dashboard Utama", "⚙️ Pengaturan Tampilan"])
        st.markdown("---")
        
        # Tambahan Fitur Filter Waktu
        time_filter = "Semua Waktu"
        if menu_selection == "📊 Dashboard Utama":
            st.markdown("### ⏳ Filter Historis")
            time_filter = st.selectbox("Rentang Waktu:", [
                "Semua Waktu", 
                "1 Minggu Terakhir", 
                "2 Minggu Terakhir",
                "1 Bulan Terakhir", 
                "3 Bulan Terakhir", 
                "6 Bulan Terakhir", 
                "1 Tahun Terakhir"
            ])
            st.markdown("---")
            st.markdown("### 📝 Input Data")
            st.link_button("✍️ Isi Evaluasi Kinerja (GForm)", "https://forms.gle/fhSczw5yEhFyPeG46", use_container_width=True)
            st.markdown("---")
            if st.button("🔄 Segarkan Data", use_container_width=True, type="primary"):
                st.cache_data.clear()
                st.rerun()

    if menu_selection == "📊 Dashboard Utama":
        df_raw = fetch_kpi_data()
        render_dashboard(config, df_raw, c_main, time_filter)
    elif menu_selection == "⚙️ Pengaturan Tampilan":
        render_settings(config)

if __name__ == "__main__":
    main()
