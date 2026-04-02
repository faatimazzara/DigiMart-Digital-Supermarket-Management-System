class DetailTransaksi:
    """
    Model data untuk rincian item dalam transaksi. 🧾
    Menghubungkan objek Barang dengan jumlah yang dibeli pelanggan.
    """

    def __init__(self, barang, jumlah):
        # Menyimpan referensi objek Barang (Aggregation)
        self.barang = barang
        self.jumlah = jumlah

    def subtotal(self):
        """
        Menghitung total harga per baris item.
        Memanfaatkan Polymorphism dari method hitung_total milik subclass Barang.
        """
        try:
            return self.barang.hitung_total(self.jumlah)
        except AttributeError:
            # Fallback jika method tidak ditemukan
            return self.barang.harga_jual * self.jumlah

    def info(self):
        """
        Mengembalikan string informasi item untuk dicetak di struk.
        Contoh: "Mie Instan x3 = 9,000"
        """
        nama = self.barang.get_nama()
        return f"{nama:<20} x{self.jumlah:<3} = Rp{self.subtotal():,.0f}"

    def to_dict(self):
        """Konversi detail ke dictionary untuk disimpan dalam riwayat transaksi."""
        return {
            "nama": self.barang.get_nama(),
            "jumlah": self.jumlah,
            "harga_satuan": self.barang.harga_jual,
            "subtotal": self.subtotal()
        }

    def __repr__(self):
        return f"Detail({self.barang.get_nama()}, qty={self.jumlah})"