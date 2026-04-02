from abc import ABC, abstractmethod
from kategori import Kategori
from timestamp_mixin import TimestampMixin

class Barang(ABC, TimestampMixin):
    """
    Abstract Base Class untuk semua produk di DigiMart Pro. 📦
    Menerapkan Enkapsulasi (Private Attributes) dan Abstraksi.
    """

    def __init__(self, nama, harga_modal, harga_jual, stok, kategori=None):
        # Inisialisasi Timestamp via Mixin
        super().__init__()
        
        # Atribut Private (Encapsulation)
        self.__nama = nama
        self.__harga_modal = harga_modal
        self.__stok = stok
        
        # Atribut Public/Protected
        self.harga_jual = harga_jual
        self.kategori = kategori if isinstance(kategori, Kategori) else Kategori(kategori) if kategori else None

    # --- GETTERS (Encapsulation) ---
    
    @property
    def nama(self):
        return self.__nama

    @property
    def stok(self):
        return self.__stok

    def get_harga_modal(self, role=None):
        """Hanya Manager dan Staff Stok yang bisa melihat harga modal."""
        if str(role).lower() in ["manager", "staff_stok"]:
            return self.__harga_modal
        return "Akses Ditolak"

    # --- SETTERS & LOGIC ---

    def set_harga_jual(self, harga):
        if harga < 0:
            raise ValueError("Harga jual tidak boleh negatif!")
        self.harga_jual = harga

    def tambah_stok(self, jumlah):
        if jumlah <= 0:
            raise ValueError("Jumlah penambahan stok harus lebih dari 0")
        self.__stok += jumlah

    def kurangi_stok(self, jumlah):
        if jumlah <= 0:
            raise ValueError("Jumlah pengurangan harus lebih dari 0")
        if jumlah > self.__stok:
            raise ValueError(f"Stok tidak cukup! (Sisa: {self.__stok})")
        self.__stok -= jumlah

    def hitung_keuntungan(self, jumlah):
        """Menghitung margin keuntungan per item."""
        return (self.harga_jual - self.__harga_modal) * jumlah

    def tampilkan_detail(self):
        """Mengembalikan informasi detail untuk ditampilkan di TerminalDesign."""
        kat_nama = self.kategori.nama if self.kategori else "-"
        return {
            "Nama Produk": self.__nama,
            "Kategori": kat_nama,
            "Harga Jual": f"Rp{self.harga_jual:,.0f}",
            "Stok Tersedia": f"{self.__stok} unit",
            "Tgl Input": self.get_created_at()
        }

    @abstractmethod
    def get_spesifikasi(self):
        """Method abstrak yang wajib diimplementasikan oleh subclass."""
        pass

    @abstractmethod
    def hitung_total(self, jumlah):
        """Method abstrak untuk perhitungan total transaksi."""
        pass

    def to_dict(self):
        """Konversi objek ke dictionary untuk disimpan ke JSON."""
        return {
            "type": self.__class__.__name__,
            "nama": self.__nama,
            "harga_modal": self.__harga_modal,
            "harga_jual": self.harga_jual,
            "stok": self.__stok,
            "kategori": self.kategori.nama if self.kategori else None
        }

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.__nama} - Rp{self.harga_jual}"