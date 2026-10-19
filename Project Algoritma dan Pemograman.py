import sqlite3
from datetime import date

# =====================================
# 1. DATABASE
# =====================================

DB_NAME = "finance.db"


def koneksi_database():
    return sqlite3.connect(DB_NAME)


def buat_tabel():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            jenis TEXT NOT NULL,
            kategori TEXT NOT NULL,
            nominal REAL NOT NULL,
            keterangan TEXT
        )
    """)

    conn.commit()
    conn.close()


# =====================================
# 2. FUNGSI FORMAT RUPIAH
# =====================================

def rupiah(nominal):
    return "Rp " + format(nominal, ",.0f").replace(",", ".")


# =====================================
# 3. TAMBAH TRANSAKSI
# =====================================

def tambah_transaksi():
    print("\n=== TAMBAH TRANSAKSI ===")

    print("1. Pemasukan")
    print("2. Pengeluaran")

    pilihan = input("Pilih jenis transaksi: ")

    if pilihan == "1":
        jenis = "Pemasukan"
        kategori_list = [
            "Gaji", "Uang Saku", "Bisnis",
            "Hadiah", "Lainnya"
        ]
    elif pilihan == "2":
        jenis = "Pengeluaran"
        kategori_list = [
            "Makanan", "Transportasi", "Pendidikan",
            "Belanja", "Tagihan", "Hiburan",
            "Kesehatan", "Lainnya"
        ]
    else:
        print("Pilihan tidak valid!")
        return

    print("\nKategori:")
    for i, kategori in enumerate(kategori_list, 1):
        print(f"{i}. {kategori}")

    try:
        nomor = int(input("Pilih kategori: "))

        if nomor < 1 or nomor > len(kategori_list):
            print("Kategori tidak valid!")
            return

        kategori = kategori_list[nomor - 1]
        nominal = float(input("Masukkan nominal (Rp): "))

        if nominal <= 0:
            print("Nominal harus lebih dari nol!")
            return

        keterangan = input("Keterangan: ")
        tanggal = date.today().isoformat()

        conn = koneksi_database()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transaksi
            (tanggal, jenis, kategori, nominal, keterangan)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tanggal, jenis, kategori, nominal, keterangan
        ))

        conn.commit()
        conn.close()

        print("\nTransaksi berhasil disimpan!")

    except ValueError:
        print("Input harus berupa angka yang valid!")


# =====================================
# 4. MENGHITUNG KEUANGAN
# =====================================

def hitung_keuangan():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT jenis, SUM(nominal)
        FROM transaksi
        GROUP BY jenis
    """)

    data = cursor.fetchall()
    conn.close()

    pemasukan = 0
    pengeluaran = 0

    for jenis, total in data:
        if jenis == "Pemasukan":
            pemasukan = total or 0
        elif jenis == "Pengeluaran":
            pengeluaran = total or 0

    saldo = pemasukan - pengeluaran

    return pemasukan, pengeluaran, saldo


# =====================================
# 5. DASHBOARD
# =====================================

def dashboard():
    pemasukan, pengeluaran, saldo = hitung_keuangan()

    print("\n" + "=" * 40)
    print("                U-Bank")
    print("=" * 40)

    print("Total Pemasukan   :", rupiah(pemasukan))
    print("Total Pengeluaran :", rupiah(pengeluaran))
    print("Saldo Saat Ini    :", rupiah(saldo))

    print("=" * 40)


# =====================================
# 6. RIWAYAT TRANSAKSI
# =====================================

def riwayat_transaksi():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM transaksi
        ORDER BY tanggal DESC, id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    print("\n=== RIWAYAT TRANSAKSI ===")

    if not data:
        print("Belum ada transaksi.")
        return

    for item in data:
        print("-" * 40)
        print("NOMOR     :", item[0])
        print("Tanggal   :", item[1])
        print("Jenis     :", item[2])
        print("Kategori  :", item[3])
        print("Nominal   :", rupiah(item[4]))
        print("Keterangan:", item[5])


# =====================================
# 7. HAPUS TRANSAKSI
# =====================================

def hapus_transaksi():
    riwayat_transaksi()

    try:
        id_transaksi = int(
            input("\nMasukkan NOMOR transaksi yang dihapus: ")
        )
    except ValueError:
        print("NOMOR harus berupa angka!")
        return

    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM transaksi WHERE id = ?",
        (id_transaksi,)
    )

    ditemukan = cursor.fetchone()

    if ditemukan:
        konfirmasi = input(
            "Yakin ingin menghapus? (yes/no): "
        ).lower()

        if konfirmasi == "yes":
            cursor.execute(
                "DELETE FROM transaksi WHERE NOMOR = ?",
                (id_transaksi,)
            )
            conn.commit()
            print("Transaksi berhasil dihapus!")
        else:
            print("Penghapusan dibatalkan.")
    else:
        print("NOMOR transaksi tidak ditemukan.")

    conn.close()

# =====================================
# 9. MENU UTAMA
# =====================================

def menu_utama():
    buat_tabel()

    while True:
        print("\n====== MENU UTAMA ======")
        print("1. Dashboard Keuangan")
        print("2. Tambah Transaksi")
        print("3. Riwayat Transaksi")
        print("4. Hapus Transaksi")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            dashboard()
        elif pilihan == "2":
            tambah_transaksi()
        elif pilihan == "3":
            riwayat_transaksi()
        elif pilihan == "4":
            hapus_transaksi()
        elif pilihan == "5":
            print("Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("Pilihan tidak valid! Silakan coba lagi.")


# =====================================
# 10. MENJALANKAN PROGRAM
# =====================================

if __name__ == "__main__":
    menu_utama()
