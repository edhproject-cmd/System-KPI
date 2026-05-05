import pandas as pd
import numpy as np

class KPI:
    def __init__(self, name, weight, target, realisasi, score):
        self.name = name
        self.weight = weight # Contoh: 0.25 untuk 25%
        self.target = target
        self.realisasi = realisasi
        self.score = score # Skala 1 sampai 5
        self.final_value = self.weight * self.score

class AparaturDepartment:
    def __init__(self):
        self.kpis = []
        
    def add_kpi(self, kpi):
        self.kpis.append(kpi)
        
    def calculate_total_score(self):
        return sum(kpi.final_value for kpi in self.kpis)
        
    def print_report(self):
        print(f"{'Indikator (KPI)':<35} | {'Bobot':<6} | {'Skor':<4} | {'Nilai Akhir':<11}")
        print("-" * 65)
        for kpi in self.kpis:
            print(f"{kpi.name:<35} | {kpi.weight*100:>4.0f}% | {kpi.score:>4} | {kpi.final_value:>11.2f}")
        print("-" * 65)
        print(f"{'TOTAL NILAI':<35} | {'100%':<6} | {'':<4} | {self.calculate_total_score():>11.2f}")

    def evaluate_retention_warning(self, current_retention_rate, target_rate=0.90):
        print("\n--- Sistem Warning Retensi ---")
        if current_retention_rate < target_rate:
            print(f"[PERINGATAN]: Tingkat retensi saat ini ({current_retention_rate*100:.1f}%) berada di bawah target ({target_rate*100:.1f}%).")
            print("   Tindakan Disarankan: Segera lakukan intervensi personal (one-on-one session) dengan pengurus yang mulai pasif.")
        else:
            print(f"[AMAN] Tingkat retensi aman ({current_retention_rate*100:.1f}%).")

    def calculate_training_impact(self, pre_test_scores, post_test_scores):
        print("\n--- Evaluasi Dampak Pelatihan ---")
        if len(pre_test_scores) != len(post_test_scores):
            print("Error: Data pre-test dan post-test tidak seimbang.")
            return 0
        
        avg_pre = sum(pre_test_scores) / len(pre_test_scores)
        avg_post = sum(post_test_scores) / len(post_test_scores)
        
        # Hitung persentase peningkatan
        improvement = ((avg_post - avg_pre) / avg_pre) * 100 if avg_pre > 0 else 0
        
        print(f"Rata-rata Pre-Test : {avg_pre:.2f}")
        print(f"Rata-rata Post-Test: {avg_post:.2f}")
        print(f"Peningkatan        : {improvement:.2f}%")
        
        return improvement

# Simulasi Kasus
if __name__ == "__main__":
    dept = AparaturDepartment()
    
    # ID dari link Google Sheets Anda yang sudah diganti
    SHEET_ID = '1q9bqDXkXY1LvE4ywWWVHc_CYqd2iDwfe9uRMcvDrZg4'
    URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    
    print("Mencoba menarik data dari Google Sheets...")
    try:
        # Membaca data langsung dari link publik Google Sheets
        df = pd.read_csv(URL)
        
        # Menghapus baris yang kosong (jika ada)
        df = df.dropna(how='all')
        
        if df.empty:
            print("\n[WARNING] Berhasil terhubung ke spreadsheet, tetapi tabel masih kosong.")
            print("Silakan isi data di Google Sheets Anda terlebih dahulu.")
        else:
            print("[SUCCESS] Data berhasil ditarik dari Google Sheets!\n")
            
            # Kita menggunakan urutan kolom (index) agar lebih kebal dari typo nama kolom
            for index, row in df.iterrows():
                try:
                    name = str(row.iloc[0]) # Kolom Pertama: Nama
                    
                    # Memproses bobot dengan aman (bisa menangani teks "25", "25%", atau angka 25)
                    raw_weight = str(row.iloc[1]).replace('%', '').strip()
                    weight = float(raw_weight) / 100 if float(raw_weight) > 1 else float(raw_weight)
                    
                    target = str(row.iloc[2]) # Kolom Ketiga: Target
                    realisasi = str(row.iloc[3]) # Kolom Keempat: Realisasi
                    score = int(row.iloc[4]) # Kolom Kelima: Skor
                    
                    dept.add_kpi(KPI(name, weight, target, realisasi, score))
                except Exception as row_error:
                    # Lewati baris yang gagal di-parse tanpa memberhentikan program
                    continue
                
            # Menampilkan Rapor KPI
            print("=== RAPOR KPI DEPARTEMEN APARATUR ===")
            if len(dept.kpis) > 0:
                dept.print_report()
            else:
                print("Belum ada data KPI yang valid untuk dikalkulasi.")
            
            # Simulasi Sistem Warning (Contoh konstan)
            dept.evaluate_retention_warning(0.85, target_rate=0.90)
        
    except Exception as e:
        print(f"\n[ERROR] Gagal menarik data: {e}")
        print("Pastikan:")
        print("1. Anda sudah membagikan file menjadi 'Anyone with the link'.")
        print("2. URL benar dan ada koneksi internet.")
