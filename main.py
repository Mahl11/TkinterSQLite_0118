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
entry_usia = tk.Entry(form_container, width=38, font=("Arial", 10), bg=WARNA_ENTRY_BG, fg=WARNA_TEKS, insertbackground="white", bd=0, relief="flat")
# Menempatkan kotak entry usia
entry_usia.pack(ipady=5, pady=(0, 6))

# 3. Komponen Input Kadar Gula Darah Sewaktu
# Label judul untuk kolom input kadar gula darah
lbl_gula = tk.Label(form_container, text="Gula Darah Sewaktu (mg/dL)", font=("Arial", 10, "bold"), bg=WARNA_BG, fg=WARNA_TEKS)
# Menempatkan label gula darah di tengah frame
lbl_gula.pack(anchor="center", pady=(4, 2))
# Kotak isian teks untuk memasukkan nilai kadar gula darah pasien
entry_gula = tk.Entry(form_container, width=38, font=("Arial", 10), bg=WARNA_ENTRY_BG, fg=WARNA_TEKS, insertbackground="white", bd=0, relief="flat")
# Menempatkan kotak entry gula darah
entry_gula.pack(ipady=5, pady=(0, 6))

# 4. Komponen Input Indeks Massa Tubuh (BMI)
# Label judul untuk kolom input indeks massa tubuh
lbl_bmi = tk.Label(form_container, text="Indeks Massa Tubuh / BMI (kg/m2)", font=("Arial", 10, "bold"), bg=WARNA_BG, fg=WARNA_TEKS)
# Menempatkan label BMI di tengah frame
lbl_bmi.pack(anchor="center", pady=(4, 2))
# Kotak isian teks untuk memasukkan angka indeks massa tubuh pasien
entry_bmi = tk.Entry(form_container, width=38, font=("Arial", 10), bg=WARNA_ENTRY_BG, fg=WARNA_TEKS, insertbackground="white", bd=0, relief="flat")
# Menempatkan kotak entry BMI
entry_bmi.pack(ipady=5, pady=(0, 6))

# 5. Komponen Dropdown Pilihan Riwayat Diabetes Orang Tua
# Label judul untuk opsi pilihan riwayat diabetes orang tua
lbl_riwayat = tk.Label(form_container, text="Riwayat Diabetes Orang Tua", font=("Arial", 10, "bold"), bg=WARNA_BG, fg=WARNA_TEKS)
# Menempatkan label riwayat orang tua di tengah frame
lbl_riwayat.pack(anchor="center", pady=(4, 2))
# Widget Combobox untuk memilih opsi Ya atau Tidak secara dropdown
combo_riwayat = ttk.Combobox(form_container, values=["Ya", "Tidak"], state="readonly", width=36, font=("Arial", 10))
# Menyetel pilihan bawaan pertama combobox menjadi 'Tidak'
combo_riwayat.set("Tidak")
# Menempatkan widget combobox ke dalam frame formulir
combo_riwayat.pack(ipady=4, pady=(0, 10))


# --- FUNGSI-FUNGSI PENGENDALI EVENT (CONTROLLER) ---

def muat_tabel():
    """Mengambil seluruh data terbaru dari database SQLite dan menampilkannya pada tabel Treeview."""
    # 1. Melakukan perulangan untuk menghapus setiap baris data lama yang ada di tabel Treeview
    for item in tree.get_children():
        # Menghapus item baris satu per satu dari tampilan tabel
        tree.delete(item)

    # 2. Mengambil data pasien terbaru dari tabel riwayat_pasien di database
    rows = ambil_semua_data()

    # 3. Melakukan perulangan untuk memasukkan setiap baris data baru ke dalam tabel Treeview
    for row in rows:
        # Memasukkan nilai baris ke posisi paling bawah tabel Treeview
        tree.insert("", tk.END, values=row)

    # 4. Memperbarui teks label statistik total data pasien yang tersimpan
    lbl_total_data.config(text=f"Total Riwayat: {len(rows)} data pasien")

def reset_form():
    """Mengosongkan seluruh kolom input formulir dan mereset status kotak diagnosis ke kondisi awal."""
    # Menghapus teks pada kotak isian nama pasien dari indeks 0 sampai akhir
    entry_nama.delete(0, tk.END)
    # Menghapus teks pada kotak isian usia pasien dari indeks 0 sampai akhir
    entry_usia.delete(0, tk.END)
    # Menghapus teks pada kotak isian kadar gula darah dari indeks 0 sampai akhir
    entry_gula.delete(0, tk.END)
    # Menghapus teks pada kotak isian BMI dari indeks 0 sampai akhir
    entry_bmi.delete(0, tk.END)
    # Mengembalikan nilai combobox riwayat orang tua ke pilihan default 'Tidak'
    combo_riwayat.set("Tidak")
    # Mengembalikan warna latar kotak hasil diagnosis ke warna gelap semula
    box_hasil.config(bg="#2d3559")
    # Mengembalikan teks judul kotak diagnosis
    lbl_hasil_head.config(bg="#2d3559", text="HASIL DIAGNOSIS")
    # Mengembalikan teks isi kotak diagnosis ke status default
    lbl_hasil_teks.config(bg="#2d3559", text="Belum Ada Data Dianalisis", fg=WARNA_SUBTEKS)
    # Memindahkan fokus kursor keyboard kembali ke input nama pasien
    entry_nama.focus()

def aksi_cek_risiko():
    """Memvalidasi data input, menghitung tingkat risiko, dan menyimpannya ke database SQLite."""
    # Mengambil teks nama pasien dan menghapus spasi di awal/akhir
    nama = entry_nama.get().strip()
    # Mengambil teks usia pasien dan menghapus spasi
    usia_str = entry_usia.get().strip()
    # Mengambil teks kadar gula darah dan menghapus spasi
    gula_str = entry_gula.get().strip()
    # Mengambil teks indeks massa tubuh dan menghapus spasi
    bmi_str = entry_bmi.get().strip()
    # Mengambil nilai pilihan riwayat orang tua dari combobox
    riwayat = combo_riwayat.get().strip()

    # Tahap Validasi 1: Memeriksa apakah ada kolom input yang masih kosong
    if not nama or not usia_str or not gula_str or not bmi_str:
        # Menampilkan pesan peringatan jika ada data yang belum diisi
        messagebox.showwarning("Data Belum Lengkap", "Seluruh kolom formulir data pasien wajib diisi!")
        # Menghentikan eksekusi fungsi agar tidak melanjutkan ke proses simpan
        return

    # Tahap Validasi 2: Memeriksa kesesuaian tipe data angka dan memastikan bernilai positif
    try:
        # Mengonversi teks input usia menjadi tipe data integer
        usia = int(usia_str)
        # Mengonversi teks input kadar gula darah menjadi tipe data float
        gula = float(gula_str)
        # Mengonversi teks input BMI menjadi tipe data float
        bmi = float(bmi_str)

        # Memastikan semua nilai numerik tidak boleh bernilai nol atau negatif
        if usia <= 0 or gula <= 0 or bmi <= 0:
            # Menampilkan pesan kesalahan jika nilai angka tidak logis
            messagebox.showerror("Nilai Tidak Valid", "Usia, kadar gula, dan BMI harus berupa angka positif!")
            # Menghentikan eksekusi fungsi
            return
    except ValueError:
        # Menampilkan pesan kesalahan jika user memasukkan teks bukan angka
        messagebox.showerror("Format Salah", "Usia harus berupa angka bulat, Gula Darah dan BMI berupa angka desimal!")
        # Menghentikan eksekusi fungsi
        return

    # Tahap Perhitungan: Menghitung tingkat risiko diabetes melalui business logic
    hasil = hitung_prediksi_risiko(gula, bmi, riwayat)

    # Tahap Penyimpanan: Membuka koneksi basis data SQLite
    conn = buat_koneksi()
    # Membuat kursor query SQL
    cur = conn.cursor()
    # Menjalankan query INSERT dengan parameter binding (?) untuk mencegah celah SQL Injection
    cur.execute("""
        INSERT INTO riwayat_pasien (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nama, usia, gula, bmi, riwayat, hasil))
    # Menyimpan transaksi data secara permanen ke file database
    conn.commit()
    # Menutup koneksi basis data setelah proses simpan berhasil
    conn.close()

    # Tahap Tampilan: Menyesuaikan warna kotak diagnosis berdasarkan tingkat risiko pasien
    warna = WARNA_RISIKO.get(hasil, WARNA_BIRU)
    # Mengubah warna latar frame kotak hasil diagnosis
    box_hasil.config(bg=warna)
    # Mengubah warna latar dan teks judul kotak hasil diagnosis
    lbl_hasil_head.config(bg=warna, text="HASIL DIAGNOSIS PASIEN")
    # Mengubah teks hasil diagnosis dengan nama tingkat risiko kapital dan warna putih
    lbl_hasil_teks.config(bg=warna, text=f"TINGKAT RISIKO: {hasil.upper()}", fg="#ffffff")

    # Menampilkan notifikasi popup sukses kepada pengguna
    messagebox.showinfo("Analisis Selesai", f"Data pasien '{nama}' berhasil disimpan!\nHasil Prediksi: Risiko {hasil}")

    # Memperbarui isi tabel Treeview agar data baru yang tersimpan langsung muncul
    muat_tabel()
