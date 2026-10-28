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

