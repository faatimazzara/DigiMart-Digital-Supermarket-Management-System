from barang import Barang

class KesehatanKecantikan(Barang):
    """
    Subclass KesehatanKecantikan. 💄
    Menangani produk kosmetik dan obat-obatan dengan atribut Merk dan Kadaluarsa.
    """

    def __init__(self, nama, harga_modal, harga_jual, stok, merk, tanggal_kadaluarsa, kategori_sub="Skincare", kategori="Kesehatan & Kecantikan"):
        # Memanggil constructor induk (Barang)
        super().__init__(nama, harga_modal, harga_jual, stok, kategori)
        # Atribut spesifik Kesehatan & Kecantikan
        self.merk = merk
        self.tanggal_kadaluarsa = tanggal_kadaluarsa
        self.kategori_sub = kategori_sub

    def get_spesifikasi(self):
        """Implementasi spesifikasi khusus produk kecantikan/kesehatan."""
        return f"Merk: {self.merk} | EXP: {self.tanggal_kadaluarsa}"

    def hitung_total(self, jumlah):
        """Menghitung total harga transaksi produk kesehatan/kecantikan."""
        return self.harga_jual * jumlah

    def tampilkan_detail(self):
        """Menyiapkan data untuk box informasi TerminalDesign."""
        data = super().tampilkan_detail()
        data.update({
            "Merk/Brand": self.merk,
            "Tgl Kadaluarsa": self.tanggal_kadaluarsa,
            "Sub Kategori": self.kategori_sub,
            "Spesifikasi": self.get_spesifikasi()
        })
        return data

    def to_dict(self):
        """Konversi ke dictionary untuk database JSON."""
        data = super().to_dict()
        data.update({
            "merk": self.merk,
            "tanggal_kadaluarsa": self.tanggal_kadaluarsa,
            "kategori_sub": self.kategori_sub
        })
        return data

    def __str__(self):
        return super().__str__() + f" [{self.merk}]"