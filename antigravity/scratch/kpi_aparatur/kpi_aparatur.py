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
    
    # 1. Menambahkan data KPI sesuai tabel simulasi
    dept.add_kpi(KPI("Ketercapaian Modul Pelatihan", 0.25, "3 modul", "3 modul terealisasi", 4))
    dept.add_kpi(KPI("Dampak Pelatihan (Pre/Post-Test)", 0.15, "Naik 20%", "Skor rata-rata naik 25%", 5))
    dept.add_kpi(KPI("Tingkat Retensi Pengurus", 0.20, "Minimal 90%", "85% pengurus bertahan", 3))
    dept.add_kpi(KPI("Tingkat Kehadiran Bonding", 0.10, "Rata-rata 80%", "Rata-rata 82% hadir", 4))
    dept.add_kpi(KPI("Ketepatan Laporan Evaluasi", 0.20, "100% tepat waktu", "Telat 1 kali di kuartal kedua", 3))
    dept.add_kpi(KPI("Inovasi Metode Pembelajaran", 0.10, "1 model baru", "1 model diterapkan", 4))
    
    # 2. Menampilkan Rapor KPI
    print("=== RAPOR KPI DEPARTEMEN APARATUR ===")
    dept.print_report()
    
    # 3. Simulasi Sistem Warning
    # Misalnya di pertengahan periode retensi turun menjadi 85%
    dept.evaluate_retention_warning(0.85, target_rate=0.90)
    
    # 4. Simulasi Perhitungan Dampak Pelatihan (Baseline Data)
    # Contoh nilai dari 5 pengurus sebelum dan sesudah pelatihan
    pre_test_data = [60, 55, 70, 65, 50]
    post_test_data = [75, 70, 85, 80, 75]
    dept.calculate_training_impact(pre_test_data, post_test_data)
