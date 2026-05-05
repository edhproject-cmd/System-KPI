# Rencana Integrasi GitHub

Anda ingin memublikasikan (*push*) proyek ini ke repositori GitHub `https://github.com/edhproject-cmd/System-KPI.git`. Langkah ini sangat tepat untuk menjaga dokumentasi dan *version control* kode Anda.

## Masalah Saat Ini
Saat ini, file kode Anda (seperti `Dashboard_KPI.py` dan `System KPI.py`) tercecer secara bebas di direktori akar/Home komputer Anda (`C:\Users\USer\`). 
Kita **sangat tidak disarankan** untuk menjalankan perintah `git init` langsung di folder tersebut karena itu akan membuat seluruh isi komputer Anda (termasuk dokumen pribadi, gambar, dll) terekam oleh GitHub.

## User Review Required

> [!IMPORTANT]
> **Strategi Migrasi Folder**
> Saya akan merapikan file-file Anda terlebih dahulu dengan membuatkan folder khusus untuk proyek ini, lalu memindahkan file yang berkaitan ke dalamnya sebelum diunggah ke GitHub.

File yang akan saya pindahkan/salin ke dalam folder proyek baru (`C:\Users\USer\System-KPI\`) adalah:
1. `Dashboard_KPI.py`
2. `System KPI.py` (Sebagai sejarah/referensi)
3. `app_config.json` (Konfigurasi dasbor)
4. Folder `.streamlit/` yang berisi `config.toml` (Tema warna)
5. File gambar logo organisasi.
6. Saya juga akan membuatkan file `requirements.txt` yang berisi daftar instalasi agar orang lain yang mengunduh repositori Anda bisa langsung menginstal pustaka yang dibutuhkan (pandas & streamlit).

## Open Questions

> [!WARNING]
> Terkait proses pengunggahan ke GitHub (`git push`), biasanya GitHub memerlukan Autentikasi (seperti *login* via browser atau memasukkan Personal Access Token). 
> 1. Apakah Anda setuju dengan pemindahan file ke dalam folder khusus `System-KPI`?
> 2. Apakah Anda sudah pernah *login* GitHub sebelumnya di terminal komputer ini? (Jika belum, saat perintah *push* dijalankan nanti, komputer Anda mungkin akan memunculkan jendela *browser* untuk meminta Anda menyetujui *login* GitHub).

## Proposed Changes
- Membuat direktori `C:\Users\USer\System-KPI`.
- Menyalin skrip dan aset yang relevan.
- Menulis file `requirements.txt` berisi `streamlit` dan `pandas`.
- Menjalankan urutan perintah Git: `git init`, `git add .`, `git commit -m "Initial commit Dashboard KPI"`, `git branch -M main`, `git remote add origin <link>`, dan `git push -u origin main`.

## Verification Plan
- Menjalankan status perintah Git (*command status*).
- Mengecek apakah ada peringatan autentikasi atau apakah pengunggahan berhasil (status *code 0*).
