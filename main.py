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

# Warna abu-abu gelap untuk latar belakang kotak isian formulir input
WARNA_ENTRY_BG = "#384166"

# Warna teks utama putih bersih agar mudah dibaca di atas tema gelap
WARNA_TEKS = "#fffffe"

# Warna teks pendukung abu-abu kebiruan terang untuk label sekunder
WARNA_SUBTEKS = "#b8c1ec"

# Warna tombol reset abu-abu netral
WARNA_RESET = "#4b5563"

# Pemetaan warna status diagnosis untuk mengubah warna kotak diagnosis secara dinamis
WARNA_RISIKO = {
    "Rendah": "#10b981",        # Warna Hijau Zamrud (Kondisi Aman / Sehat)
    "Waspada": "#f59e0b",       # Warna Kuning Emas (Perhatian Khusus)
    "Sedang": "#f97316",        # Warna Oranye (Tingkat Risiko Moderat)
    "Tinggi": "#ef4444",        # Warna Merah Terang (Tingkat Risiko Bahaya)
    "Sangat Tinggi": "#b91c1c"  # Warna Merah Gelap Marun (Kondisi Kritis)
}


# ------------------------------------------------------------------------------
# [LAYER 4] USER INTERFACE (Membangun Tampilan Antarmuka GUI Tkinter)
# ------------------------------------------------------------------------------

# Inisialisasi basis data dan pembuatan tabel otomatis saat aplikasi dibuka
init_db()

# Membuat objek jendela utama Tkinter
app = tk.Tk()

# Menetapkan teks judul yang tampil di bilah atas (title bar) jendela
app.title("Prediksi Risiko Diabetes - Ilham Saputra (0118)")

# Menetapkan ukuran dimensi awal jendela aplikasi (lebar 540px, tinggi 860px)
app.geometry("540x860")

# Menyetel warna latar belakang seluruh jendela aplikasi
app.configure(bg=WARNA_BG)


# --- WIDGET HEADER APLIKASI ---

# Label judul aplikasi dengan simbol tanda tambah medis (+) warna pink rose
lbl_judul = tk.Label(
    app, 
    text="+ Prediksi Risiko Diabetes", 
    font=("Arial", 16, "bold"), 
    bg=WARNA_BG, 
    fg=WARNA_PINK
)
# Menempatkan widget label judul dengan jarak atas 15px dan jarak bawah 2px
lbl_judul.pack(pady=(15, 2))

# Label informasi identitas mahasiswa (Nama, NIM, Matakuliah)
lbl_identitas = tk.Label(
    app, 
    text="Ilham Saputra | 20240140118 | Pemrograman Multiplatform", 
    font=("Arial", 8), 
    bg=WARNA_BG, 
    fg=WARNA_SUBTEKS
)
# Menempatkan label identitas mahasiswa tepat di bawah judul aplikasi
lbl_identitas.pack(pady=(0, 12))


# --- WIDGET FORMULIR INPUT DATA PASIEN ---

# Frame penampung seluruh komponen input formulir
form_container = tk.Frame(app, bg=WARNA_BG)
# Menempatkan frame formulir dengan padding horizontal 35px agar simetris
form_container.pack(fill="x", padx=35)

# 1. Komponen Input Nama Pasien
# Label judul untuk kolom input nama pasien
lbl_nama = tk.Label(form_container, text="Nama Pasien", font=("Arial", 10, "bold"), bg=WARNA_BG, fg=WARNA_TEKS)
# Menempatkan label nama di tengah frame
lbl_nama.pack(anchor="center", pady=(4, 2))
# Kotak isian teks untuk memasukkan nama pasien
entry_nama = tk.Entry(form_container, width=38, font=("Arial", 10), bg=WARNA_ENTRY_BG, fg=WARNA_TEKS, insertbackground="white", bd=0, relief="flat")
# Menempatkan kotak entry nama dengan tinggi dalam (ipady) 5px
entry_nama.pack(ipady=5, pady=(0, 6))

# 2. Komponen Input Usia Pasien
# Label judul untuk kolom input usia pasien
lbl_usia = tk.Label(form_container, text="Usia (Tahun)", font=("Arial", 10, "bold"), bg=WARNA_BG, fg=WARNA_TEKS)
# Menempatkan label usia di tengah frame
lbl_usia.pack(anchor="center", pady=(4, 2))
# Kotak isian teks untuk memasukkan angka usia pasien
