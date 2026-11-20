"""
Sistem Perpustakaan Sederhana
Menerapkan konsep OOP: class, object, constructor, attribute, method,
encapsulation, property/setter, classmethod, dan staticmethod.
"""


class Buku:
    """Class untuk merepresentasikan sebuah buku."""

    jumlah_buku = 0  # class attribute

    def __init__(self, kode, judul, penulis, stok):
        # Attribute private (encapsulation)
        self.__kode = kode
        self.__judul = judul
        self.__penulis = penulis
        self.__stok = 0
        self.stok = stok  # memakai setter agar tervalidasi
        Buku.jumlah_buku += 1

    # ---------- Property & Setter ----------
    @property
    def kode(self):
        return self.__kode

    @property
    def judul(self):
        return self.__judul

    @property
    def penulis(self):
        return self.__penulis

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai):
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif!")
        self.__stok = nilai

    # ---------- Method ----------
    def tersedia(self):
        return self.__stok > 0

    def kurangi_stok(self):
        self.stok = self.__stok - 1

    def tambah_stok(self):
        self.stok = self.__stok + 1

    def info(self):
        status = "Tersedia" if self.tersedia() else "Habis"
        return (f"[{self.__kode}] {self.__judul} - {self.__penulis} "
                f"| Stok: {self.__stok} ({status})")

    # ---------- Class Method ----------
    @classmethod
    def dari_string(cls, teks):
        """Membuat objek Buku dari string 'kode;judul;penulis;stok'."""
        kode, judul, penulis, stok = teks.split(";")
        return cls(kode.strip(), judul.strip(), penulis.strip(), int(stok))

    @classmethod
    def total_buku(cls):
        return cls.jumlah_buku

    # ---------- Static Method ----------
    @staticmethod
    def validasi_kode(kode):
        """Kode buku valid jika diawali 'B' diikuti 3 digit, contoh: B001."""
        return len(kode) == 4 and kode[0].upper() == "B" and kode[1:].isdigit()


class Anggota:
    """Class untuk merepresentasikan anggota perpustakaan."""

    BATAS_PINJAM = 3  # class attribute

    def __init__(self, nim, nama):
        self.__nim = nim
        self.__nama = nama
        self.__buku_dipinjam = []

    @property
    def nim(self):
        return self.__nim

    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, nilai):
        if not nilai.strip():
            raise ValueError("Nama tidak boleh kosong!")
        self.__nama = nilai

    @property
    def buku_dipinjam(self):
        return list(self.__buku_dipinjam)  # salinan, agar list asli aman

    def bisa_pinjam(self):
        return len(self.__buku_dipinjam) < Anggota.BATAS_PINJAM

    def tambah_pinjaman(self, buku):
        self.__buku_dipinjam.append(buku)

    def hapus_pinjaman(self, buku):
        self.__buku_dipinjam.remove(buku)

    def info(self):
        daftar = ", ".join(b.judul for b in self.__buku_dipinjam) or "-"
        return f"{self.__nim} | {self.__nama} | Pinjaman: {daftar}"


class Perpustakaan:
    """Class yang mengelola buku dan anggota."""

    def __init__(self, nama):
        self.nama = nama
        self.__daftar_buku = {}
        self.__daftar_anggota = {}

    def tambah_buku(self, buku):
        if not Buku.validasi_kode(buku.kode):
            print(f"Kode '{buku.kode}' tidak valid (format: B001).")
            return
        self.__daftar_buku[buku.kode] = buku

    def tambah_anggota(self, anggota):
        self.__daftar_anggota[anggota.nim] = anggota

    def tampilkan_buku(self):
        print(f"\n=== Daftar Buku {self.nama} ===")
        for buku in self.__daftar_buku.values():
            print(buku.info())

    def tampilkan_anggota(self):
        print("\n=== Daftar Anggota ===")
        for anggota in self.__daftar_anggota.values():
            print(anggota.info())

    def pinjam_buku(self, nim, kode):
        anggota = self.__daftar_anggota.get(nim)
        buku = self.__daftar_buku.get(kode)
        if anggota is None or buku is None:
            print("Anggota atau buku tidak ditemukan.")
        elif not buku.tersedia():
            print(f"Maaf, buku '{buku.judul}' sedang habis.")
        elif not anggota.bisa_pinjam():
            print(f"{anggota.nama} sudah mencapai batas pinjam "
                  f"({Anggota.BATAS_PINJAM} buku).")
        else:
            buku.kurangi_stok()
            anggota.tambah_pinjaman(buku)
            print(f"{anggota.nama} berhasil meminjam '{buku.judul}'.")

    def kembalikan_buku(self, nim, kode):
        anggota = self.__daftar_anggota.get(nim)
        buku = self.__daftar_buku.get(kode)
        if anggota is None or buku is None or buku not in anggota.buku_dipinjam:
            print("Data peminjaman tidak ditemukan.")
        else:
            buku.tambah_stok()
            anggota.hapus_pinjaman(buku)
            print(f"{anggota.nama} mengembalikan '{buku.judul}'.")


def main():
    # Membuat object Perpustakaan
    perpus = Perpustakaan("Perpustakaan Kampus")

    # Membuat object Buku (constructor biasa & classmethod)
    perpus.tambah_buku(Buku("B001", "Pemrograman Python", "Budi Raharjo", 2))
    perpus.tambah_buku(Buku("B002", "Struktur Data", "Rinaldi Munir", 1))
    perpus.tambah_buku(Buku.dari_string("B003; Basis Data; Fathansyah; 3"))
    perpus.tambah_buku(Buku("XYZ", "Kode Salah", "Tidak Ada", 1))  # ditolak

    # Membuat object Anggota
    perpus.tambah_anggota(Anggota("2024001", "Andi"))
    perpus.tambah_anggota(Anggota("2024002", "Sari"))

    perpus.tampilkan_buku()

    print("\n=== Simulasi Transaksi ===")
    perpus.pinjam_buku("2024001", "B001")
    perpus.pinjam_buku("2024002", "B002")
    perpus.pinjam_buku("2024001", "B002")  # stok habis
    perpus.kembalikan_buku("2024002", "B002")
    perpus.pinjam_buku("2024001", "B002")

    perpus.tampilkan_buku()
    perpus.tampilkan_anggota()

    print(f"\nTotal judul buku terdaftar: {Buku.total_buku()}")

    # Demonstrasi setter dengan validasi
    try:
        buku = Buku("B004", "Tes", "Penulis", 1)
        buku.stok = -5
    except ValueError as e:
        print(f"Error setter: {e}")


if __name__ == "__main__":
    main()