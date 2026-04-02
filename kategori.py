class Kategori:
    """
    Model data untuk kategori produk di DigiMart Pro. 📂
    Berfungsi sebagai pengelompokan barang (Makanan, Minuman, Elektronik, dll).
    """

    def __init__(self, nama):
        # Inisialisasi Nama Kategori
        self.nama = nama
        # List internal untuk menampung barang dalam kategori ini (Aggregation)
        self.__daftar_barang = []

    def get_nama(self):
        """Mengambil nama kategori."""
        return self.nama

    def tambah_barang_ke_kategori(self, barang):
        """Menambahkan objek barang ke dalam kategori ini."""
        if barang not in self.__daftar_barang:
            self.__daftar_barang.append(barang)

    def get_total_stok_kategori(self):
        """Menghitung total stok seluruh barang dalam kategori ini."""
        total = sum(b.stok for b in self.__daftar_barang)
        return total

    def tampilkan_info_singkat(self):
        """Mengembalikan string informasi kategori untuk tabel."""
        return f"Kategori: {self.nama:<15} | Item: {len(self.__daftar_barang):<3}"

    def __str__(self):
        """Representasi string saat objek diprint."""
        return self.nama

    def __repr__(self):
        return f"Kategori('{self.nama}')"