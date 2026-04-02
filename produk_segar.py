from barang import Barang

class ProdukSegar(Barang):
    """
    Subclass ProdukSegar (Buah, Sayur, Daging). 🍎
    Memerlukan pencatatan tanggal kedatangan untuk memantau kesegaran.
    """

    def __init__(self, nama, harga_modal, harga_jual, stok, berat, tanggal_kedatangan, tanggal_kadaluarsa, kategori="Produk Segar"):
        # Memanggil constructor induk (Barang)
        super().__init__(nama, harga_modal, harga_jual, stok, kategori)
        # Atribut spesifik produk segar
        self.berat = berat  # dalam kg
        self.tanggal_kedatangan = tanggal_kedatangan
        self.tanggal_kadaluarsa = tanggal_kadaluarsa

    def get_spesifikasi(self):
        """Implementasi spesifikasi untuk memantau masa simpan."""
        return f"Berat: {self.berat}kg | Datang: {self.tanggal_kedatangan}"

    def hitung_total(self, jumlah):
        """
        Menghitung total harga. 
        Pada produk segar, jumlah bisa berupa berat (float).
        """
        return self.harga_jual * jumlah

    def tampilkan_detail(self):
        """Menyiapkan data untuk box informasi di terminal."""
        data = super().tampilkan_detail()
        data.update({
            "Berat Satuan": f"{self.berat} kg",
            "Tgl Datang": self.tanggal_kedatangan,
            "Tgl Kadaluarsa": self.tanggal_kadaluarsa,
            "Spesifikasi": self.get_spesifikasi()
        })
        return data

    def to_dict(self):
        """Konversi ke dictionary untuk database JSON."""
        data = super().to_dict()
        data.update({
            "berat": self.berat,
            "tanggal_kedatangan": self.tanggal_kedatangan,
            "tanggal_kadaluarsa": self.tanggal_kadaluarsa
        })
        return data

    def __str__(self):
        return super().__str__() + f" [{self.berat}kg - Segar]"