from database import Database
from factory import create_barang
from logsystem import LogSystem
from design_output import TerminalDesign

class Toko:
    """
    Kelas Utama Toko (DigiMart Pro). 🏢
    Pusat kendali yang menghubungkan Database, Barang, Transaksi, dan Log.
    Menerapkan Aggregation terhadap Database dan LogSystem.
    """

    def __init__(self, nama):
        self.nama_toko = nama
        
        # Inisialisasi Database (Composition)
        self.db_barang = Database("database/barang.json")
        self.db_transaksi = Database("database/transaksi.json")
        self.log_system = LogSystem()
        
        # Load Data Awal
        self.daftar_barang = self.load_barang()
        self.daftar_transaksi = self.db_transaksi.load()
        self.daftar_kategori = ["Makanan", "Minuman", "Produk Segar", "Elektronik", "Rumah Tangga"]

    # ======================
    # LOAD & SAVE LOGIC
    # ======================
    def load_barang(self):
        """Memuat objek barang menggunakan Factory Pattern agar data mentah jadi objek."""
        try:
            data = self.db_barang.load()
            return [create_barang(b) for b in data if b]
        except Exception as e:
            TerminalDesign.print_error(f"Gagal memuat barang: {e}")
            return []

    def save_barang(self):
        """Menyimpan seluruh objek barang kembali ke file JSON."""
        data = [b.to_dict() for b in self.daftar_barang]
        self.db_barang.save(data)

    # ======================
    # MANAJEMEN BARANG
    # ======================
    def tambah_barang(self, barang, user=None):
        """Menambah barang ke list dan mencatat log pelakunya."""
        self.daftar_barang.append(barang)
        self.save_barang()

        if user and hasattr(user, "log"):
            try:
                # Menggunakan method .nama (property) dari objek barang
                log = user.log(f"Tambah barang: {barang.nama}")
                self.log_system.tambah_log(log)
            except:
                pass

    def hapus_barang(self, nama):
        """Menghapus barang berdasarkan nama (Case-Insensitive)."""
        original_count = len(self.daftar_barang)
        self.daftar_barang = [
            b for b in self.daftar_barang
            if b.nama.lower() != nama.lower()
        ]
        
        if len(self.daftar_barang) < original_count:
            self.save_barang()
            return True
        return False

    def cari_barang(self, nama):
        """Mencari objek barang di dalam list berdasarkan nama."""
        for b in self.daftar_barang:
            if b.nama.lower() == nama.lower():
                return b
        return None

    def laporan_stok(self):
        """Mengambil ringkasan info semua barang."""
        return [b.tampilkan_detail() for b in self.daftar_barang]

    def barang_hampir_habis(self):
        """Mengambil list barang dengan stok rendah (<= 5)."""
        return [b for b in self.daftar_barang if b.stok <= 5]

    # ======================
    # MANAJEMEN TRANSAKSI
    # ======================
    def tambah_transaksi(self, transaksi, user=None):
        """Menyimpan data transaksi dan melakukan auto-save stok barang."""
        data_tx = {
            "id": transaksi.id_transaksi,
            "tanggal": str(transaksi.tanggal),
            "total": transaksi.hitung_total(),
            "kasir": user.nama_lengkap if user else "System"
        }

        self.daftar_transaksi.append(data_tx)
        self.db_transaksi.save(self.daftar_transaksi)
        
        # 🔥 PENTING: Simpan perubahan stok barang setelah dibeli
        self.save_barang()

        if user and hasattr(user, "log"):
            try:
                log = user.log(f"Transaksi ID {transaksi.id_transaksi} | Total: Rp{data_tx['total']:,}")
                self.log_system.tambah_log(log)
            except:
                pass

    def total_pendapatan(self):
        """Menghitung akumulasi pendapatan dari seluruh transaksi di JSON."""
        return sum(t.get("total", 0) for t in self.daftar_transaksi)

    # ======================
    # MANAJEMEN KATEGORI & LOG
    # ======================
    def tambah_kategori(self, nama):
        """Menambah kategori baru jika belum ada."""
        if nama not in self.daftar_kategori:
            self.daftar_kategori.append(nama)
            TerminalDesign.print_success(f"Kategori '{nama}' berhasil ditambahkan!")
        else:
            TerminalDesign.print_warning(f"Kategori '{nama}' sudah ada!")

    def lihat_kategori(self):
        """Getter untuk list kategori."""
        return self.daftar_kategori

    def lihat_log(self):
        """Mengambil data aktivitas dari LogSystem."""
        return self.log_system.lihat_log()