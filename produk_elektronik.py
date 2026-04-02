from barang import Barang

class ProdukElektronik(Barang):
    """
    Subclass ProdukElektronik. 💻
    Menangani produk dengan atribut khusus Merk dan Masa Garansi.
    """

    def __init__(self, nama, harga_modal, harga_jual, stok, garansi, merk="Generic", kategori_sub="Elektronik", kategori="Elektronik"):
        # Memanggil constructor induk (Barang)
        super().__init__(nama, harga_modal, harga_jual, stok, kategori)
        # Atribut spesifik Elektronik
        self.garansi = garansi  # dalam bulan
        self.merk = merk
        self.kategori_sub = kategori_sub

    def get_spesifikasi(self):
        """Implementasi spesifikasi untuk produk elektronik."""
        return f"Merk: {self.merk} | Garansi: {self.garansi} Bulan"

    def hitung_total(self, jumlah):
        """Menghitung total harga transaksi elektronik."""
        return self.harga_jual * jumlah

    def tampilkan_detail(self):
        """Menyiapkan data untuk box informasi TerminalDesign."""
        data = super().tampilkan_detail()
        data.update({
            "Merk/Brand": self.merk,
            "Masa Garansi": f"{self.garansi} Bulan",
            "Sub Kategori": self.kategori_sub,
            "Spesifikasi": self.get_spesifikasi()
        })
        return data

    def to_dict(self):
        """Konversi ke dictionary untuk database JSON."""
        data = super().to_dict()
        data.update({
            "garansi": self.garansi,
            "merk": self.merk,
            "kategori_sub": self.kategori_sub
        })
        return data

    def __str__(self):
        return super().__str__() + f" [{self.merk} - {self.garansi}bln]"