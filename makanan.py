from barang import Barang

class Makanan(Barang):
    """
    Subclass Makanan yang mewarisi sifat dari Barang. 🍞
    Menambahkan atribut khusus 'tanggal_kadaluarsa'.
    """

    def __init__(self, nama, harga_modal, harga_jual, stok, tanggal_kadaluarsa, kategori="Makanan"):
        # Memanggil constructor induk (Barang)
        super().__init__(nama, harga_modal, harga_jual, stok, kategori)
        # Atribut spesifik subclass
        self.tanggal_kadaluarsa = tanggal_kadaluarsa

    def get_spesifikasi(self):
        """Implementasi spesifikasi khusus untuk produk makanan."""
        return f"Kadaluarsa: {self.tanggal_kadaluarsa}"

    def hitung_total(self, jumlah):
        """Menghitung total harga untuk transaksi makanan."""
        return self.harga_jual * jumlah

    def tampilkan_detail(self):
        """
        Mengambil detail dari induk dan menambahkan 
        informasi kadaluarsa untuk TerminalDesign.
        """
        data = super().tampilkan_detail()
        data.update({
            "Spesifikasi": self.get_spesifikasi(),
            "Status": "Layak Jual" # Bisa ditambah logika pengecekan tanggal di sini
        })
        return data

    def to_dict(self):
        """Override to_dict untuk menyertakan data kadaluarsa ke JSON."""
        data = super().to_dict()
        data.update({
            "tanggal_kadaluarsa": self.tanggal_kadaluarsa,
        })
        return data

    def __str__(self):
        return super().__str__() + f" [EXP: {self.tanggal_kadaluarsa}]"