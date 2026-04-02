from barang import Barang

class BarangRumahTangga(Barang):
    """
    Subclass BarangRumahTangga. 🏠
    Menangani produk peralatan rumah tangga dengan atribut Merk.
    """

    def __init__(self, nama, harga_modal, harga_jual, stok, satuan="Pcs", merk="Universal", kategori_sub="RT", kategori="Rumah Tangga"):
        # Memanggil constructor induk (Barang)
        super().__init__(nama, harga_modal, harga_jual, stok, kategori)
        # Atribut spesifik Barang Rumah Tangga
        self.merk = merk
        self.satuan = satuan
        self.kategori_sub = kategori_sub

    def get_spesifikasi(self):
        """Implementasi spesifikasi untuk produk rumah tangga."""
        return f"Merk: {self.merk} | Satuan: {self.satuan}"

    def hitung_total(self, jumlah):
        """Menghitung total harga transaksi barang rumah tangga."""
        return self.harga_jual * jumlah

    def tampilkan_detail(self):
        """Menyiapkan data untuk box informasi TerminalDesign."""
        data = super().tampilkan_detail()
        data.update({
            "Merk/Brand": self.merk,
            "Satuan": self.satuan,
            "Sub Kategori": self.kategori_sub,
            "Spesifikasi": self.get_spesifikasi()
        })
        return data

    def to_dict(self):
        """Konversi ke dictionary untuk database JSON."""
        data = super().to_dict()
        data.update({
            "merk": self.merk,
            "satuan": self.satuan,
            "kategori_sub": self.kategori_sub
        })
        return data

    def __str__(self):
        return super().__str__() + f" [{self.merk} - {self.satuan}]"