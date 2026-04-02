from database import Database
from makanan import Makanan
from minuman import Minuman
from produk_segar import ProdukSegar
from produk_elektronik import ProdukElektronik
from rumah_tangga import BarangRumahTangga
from kesehatan_kecantikan import KesehatanKecantikan
from design_output import TerminalDesign

class StokManager:
    """
    Manajer Inventaris DigiMart Pro. 📦
    Mengelola daftar barang, pencarian, dan sinkronisasi dengan database JSON.
    """

    def __init__(self):
        self.db = Database("database/barang.json")
        self.__daftar_barang = self.load_barang()

    def load_barang(self):
        """Memuat data JSON dan mengonversinya kembali menjadi objek Class yang sesuai."""
        data = self.db.load()
        list_barang = []
        
        for b in data:
            try:
                # Factory Logic: Instansiasi objek berdasarkan 'type' di JSON
                t = b["type"]
                if t == "Makanan":
                    obj = Makanan(b["nama"], b["harga_modal"], b["harga_jual"], b["stok"], b["tanggal_kadaluarsa"], b["kategori"])
                elif t == "Minuman":
                    obj = Minuman(b["nama"], b["harga_modal"], b["harga_jual"], b["stok"], b["volume"], b["tanggal_kadaluarsa"], b["kategori"])
                elif t == "ProdukSegar":
                    obj = ProdukSegar(b["nama"], b["harga_modal"], b["harga_jual"], b["stok"], b.get("berat", 1), b["tanggal_kedatangan"], b["tanggal_kadaluarsa"], b["kategori"])
                elif t == "ProdukElektronik":
                    obj = ProdukElektronik(b["nama"], b["harga_modal"], b["harga_jual"], b["stok"], b["garansi"], b["merk"], b.get("kategori_sub"), b["kategori"])
                elif t == "BarangRumahTangga":
                    obj = BarangRumahTangga(b["nama"], b["harga_modal"], b["harga_jual"], b["stok"], b.get("satuan"), b["merk"], b.get("kategori_sub"), b["kategori"])
                elif t == "KesehatanKecantikan":
                    obj = KesehatanKecantikan(b["nama"], b["harga_modal"], b["harga_jual"], b["stok"], b["merk"], b["tanggal_kadaluarsa"], b.get("kategori_sub"), b["kategori"])
                else:
                    continue
                
                list_barang.append(obj)
            except Exception as e:
                print(f"Gagal memuat item {b.get('nama')}: {e}")
        
        return list_barang

    def ambil_semua_barang(self):
        """Getter untuk list barang (Encapsulation)."""
        return self.__daftar_barang

    def cari_barang(self, keyword):
        """Mencari barang berdasarkan nama (case-insensitive)."""
        keyword = str(keyword).lower()
        for b in self.__daftar_barang:
            if keyword in b.nama.lower():
                return b
        return None

    def tambah_barang_baru(self, barang_obj):
        """Menambahkan objek barang baru ke list dan simpan ke database."""
        # Cek jika barang sudah ada (berdasarkan nama)
        exist = self.cari_barang(barang_obj.nama)
        if exist:
            TerminalDesign.print_warning(f"Barang '{barang_obj.nama}' sudah ada. Gunakan Update Stok!")
            return False
            
        self.__daftar_barang.append(barang_obj)
        return self.save_perubahan()

    def hapus_barang(self, nama_barang):
        """Menghapus barang dari daftar."""
        barang = self.cari_barang(nama_barang)
        if barang:
            self.__daftar_barang.remove(barang)
            TerminalDesign.print_success(f"Barang '{nama_barang}' telah dihapus.")
            return self.save_perubahan()
        return False

    def save_perubahan(self):
        """Menyimpan list objek barang kembali ke format JSON dictionary."""
        try:
            data_to_save = [b.to_dict() for b in self.__daftar_barang]
            return self.db.save(data_to_save)
        except Exception as e:
            TerminalDesign.print_error(f"Gagal menyimpan database barang: {e}")
            return False

    def get_total_item_unik(self):
        """Menghitung jumlah jenis barang yang tersedia."""
        return len(self.__daftar_barang)