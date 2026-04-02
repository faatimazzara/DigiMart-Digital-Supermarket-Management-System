from barang import Barang

class Minuman(Barang):
    """
    Subclass Minuman yang mewarisi sifat dari Barang. 🥤
    Menambahkan atribut khusus 'volume' dan 'tanggal_kadaluarsa'.
    """

    def __init__(self, nama, harga_modal, harga_jual, stok, volume, tanggal_kadaluarsa, kategori="Minuman"):
        # Memanggil constructor induk (Barang)
        super().__init__(nama, harga_modal, harga_jual, stok, kategori)
        # Atribut spesifik subclass
        self.volume = volume
        self.tanggal_kadaluarsa = tanggal_kadaluarsa

    def get_spesifikasi(self):
        """Implementasi spesifikasi khusus untuk produk minuman."""
        return f"Vol: {self.volume} ml | EXP: {self.tanggal_kadaluarsa}"

    def hitung_total(self, jumlah):
        """Menghitung total harga untuk transaksi minuman."""
        return self.harga_jual * jumlah

    def tampilkan_detail(self):
        """
        Mengambil detail dari induk dan menambahkan 
        informasi volume & kadaluarsa untuk TerminalDesign.
        """
        data = super().tampilkan_detail()
        data.update({
            "Spesifikasi": self.get_spesifikasi(),
            "Kapasitas": f"{self.volume} ml"
        })
        return data

    def to_dict(self):
        """Override to_dict untuk menyimpan data volume ke JSON."""
        data = super().to_dict()
        data.update({
            "volume": self.volume,
            "tanggal_kadaluarsa": self.tanggal_kadaluarsa
        })
        return data

    def __str__(self):
        return super().__str__() + f" ({self.volume}ml)"