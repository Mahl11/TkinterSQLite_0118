# ==============================================================================
# TUGAS PRAKTIKUM: APLIKASI PREDIKSI RISIKO DIABETES (TKINTER + SQLITE)
# ------------------------------------------------------------------------------
# Nama Mahasiswa : Ilham Saputra
# NIM            : 20240140118
# Matakuliah     : Pemrograman Multiplatform
# Repository     : TkinterSQLite_0118
# ==============================================================================

# Mengimpor modul dasar tkinter untuk membangun antarmuka grafis desktop
import tkinter as tk

# Mengimpor widget modern ttk dan modul messagebox untuk pesan pop-up dialog
from tkinter import ttk, messagebox

# Mengimpor modul bawaan sqlite3 untuk berinteraksi dengan database lokal
import sqlite3

# Mengimpor modul os untuk membaca path file sistem secara dinamis dan portabel
import os


# ------------------------------------------------------------------------------
# [KONFIGURASI JALUR BASIS DATA]
# ------------------------------------------------------------------------------

# Mendapatkan path absolut dari direktori tempat script main.py ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Menggabungkan path direktori dengan nama file database SQLite yang digunakan
DB_NAME = os.path.join(BASE_DIR, "prediksi_diabetes.db")


# ------------------------------------------------------------------------------
# [LAYER 1] DATA ACCESS LAYER (Operasi Basis Data SQLite)
# ------------------------------------------------------------------------------

def buat_koneksi():
    """Membuka dan mengembalikan objek koneksi aktif ke file database SQLite."""
    # Membuka koneksi ke file database prediksi_diabetes.db
    return sqlite3.connect(DB_NAME)

def init_db():
    """Membuat tabel 'riwayat_pasien' di database jika tabel tersebut belum ada."""
    # 1. Buka koneksi ke basis data
    conn = buat_koneksi()
    # 2. Buat objek kursor untuk mengeksekusi perintah SQL
    cur = conn.cursor()
    # 3. Jalankan perintah DDL CREATE TABLE dengan 7 kolom sesuai spesifikasi kasus
    cur.execute("""
        CREATE TABLE IF NOT EXISTS riwayat_pasien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pasien TEXT NOT NULL,
            usia INTEGER NOT NULL,
            gula_darah REAL NOT NULL,
            bmi REAL NOT NULL,
            riwayat_ortu TEXT NOT NULL,
            hasil_prediksi TEXT NOT NULL
        )
    """)
    # 4. Simpan (commit) transaksi perubahan skema ke file fisik basis data
    conn.commit()
    # 5. Tutup koneksi basis data untuk menghemat sumber daya memori
    conn.close()

def ambil_semua_data():
    """Mengambil seluruh riwayat data pasien dari tabel riwayat_pasien."""
    # 1. Buka koneksi ke basis data
    conn = buat_koneksi()
    # 2. Buat objek kursor pengeksekusi query
    cur = conn.cursor()
    # 3. Eksekusi query SELECT semua kolom yang diurutkan dari id terbaru (DESC)
    cur.execute("SELECT id, nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi FROM riwayat_pasien ORDER BY id DESC")
    # 4. Ambil semua baris hasil query ke dalam list tuple Python
    rows = cur.fetchall()
    # 5. Tutup koneksi basis data setelah data selesai dibaca
    conn.close()
    # 6. Mengembalikan list data pasien ke pemanggil fungsi
    return rows


# ------------------------------------------------------------------------------
# [LAYER 2] BUSINESS LOGIC (Aturan Klasifikasi Risiko Diabetes)
# ------------------------------------------------------------------------------

def hitung_prediksi_risiko(gula, bmi, riwayat_ortu):
    """
    Menghitung tingkat risiko diabetes berdasarkan 5 kategori aturan keputusan:
    - Gula darah >= 200: Sangat Tinggi (jika BMI >= 30 atau riwayat Ya), selain itu Tinggi.
    - Gula darah 140-199: Tinggi (jika BMI >= 30 atau riwayat Ya), selain itu Sedang.
    - Gula darah < 140 dan BMI >= 30: Sedang (jika riwayat Ya), selain itu Waspada.
    - Gula darah < 140, BMI < 30, riwayat Ya: Waspada.
    - Gula darah < 140, BMI < 30, riwayat Tidak: Rendah.
    """
    # Mengecek apakah pasien memiliki riwayat diabetes keluarga (nilai 'Ya')
    riwayat_ya = (riwayat_ortu.strip().lower() == "ya")

    # Kasus 1: Gula darah tinggi >= 200 mg/dL (Kondisi Hiperglikemia Berat)
    if gula >= 200:
        # Jika obesitas (BMI >= 30) atau ada riwayat keluarga
        if bmi >= 30 or riwayat_ya:
            # Tingkat risiko paling kritis
            return "Sangat Tinggi"
        # Jika kadar gula tinggi tanpa komplikasi faktor lainnya
        return "Tinggi"

    # Kasus 2: Gula darah pra-diabetes rentang 140 sampai 199 mg/dL
    elif 140 <= gula <= 199:
        # Jika memiliki faktor pemberat BMI tinggi atau faktor keturunan
        if bmi >= 30 or riwayat_ya:
            # Tingkat risiko tinggi
            return "Tinggi"
        # Jika tidak ada faktor risiko obesitas atau keturunan
        return "Sedang"

    # Kasus 3, 4, dan 5: Kadar gula darah sewaktu normal (< 140 mg/dL)
    else:
        # Pengecekan kondisi berat badan apakah tergolong obesitas (BMI >= 30)
        if bmi >= 30:
            # Obesitas dengan faktor genetik menghasilkan risiko sedang, tanpa genetik waspada
            return "Sedang" if riwayat_ya else "Waspada"
        # Kondisi berat badan normal (BMI < 30)
        else:
            # Normal dengan faktor genetik waspada, jika bersih maka rendah (aman)
            return "Waspada" if riwayat_ya else "Rendah"


# ------------------------------------------------------------------------------
# [LAYER 3] KONFIGURASI TEMA WARNA (DARK SLATE & PINK ROSE HEALTH ACCENT)
# ------------------------------------------------------------------------------

# Warna latar belakang jendela utama (Navy Slate gelap yang modern)
WARNA_BG = "#232946"

# Warna aksen pink rose untuk judul dan identitas tema kesehatan
WARNA_PINK = "#ff7597"

# Warna biru cerah untuk tombol aksi utama Cek Risiko
WARNA_BIRU = "#5b8def"

