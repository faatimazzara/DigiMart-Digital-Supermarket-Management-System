from abc import ABC, abstractmethod
from design_output import TerminalDesign

class Laporan(ABC):
    """
    Abstract Base Class untuk sistem pelaporan. 📊
    Memastikan semua jenis laporan memiliki metode generate().
    """
    @abstractmethod
    def generate(self):
        pass

# ==========================================
# LAPORAN STOK (File 27)
# ==========================================
class LaporanStok(Laporan):
    """Laporan untuk memantau sisa barang di gudang."""
    def __init__(self, data_barang):
        self.data_barang = data_barang

    def generate(self):
        TerminalDesign.print_header("LAPORAN STOK GUDANG")
        if not self.data_barang:
            print("   (Tidak ada data barang)")
            return

        # Header Tabel
        print(f"{'Produk':<25} | {'Kategori':<15} | {'Stok':<8} | {'Status'}")
        print("-" * 65)

        for b in self.data_barang:
            status = f"{TerminalDesign.RED}REFILL{TerminalDesign.ENDC}" if b.stok <= 5 else "AMAN"
            kat_nama = b.kategori.nama if b.kategori else "-"
            print(f"{b.nama[:25]:<25} | {kat_nama:<15} | {b.stok:>8} | {status}")

# ==========================================
# LAPORAN TRANSAKSI (File 28)
# ==========================================
class LaporanTransaksi(Laporan):
    """Laporan riwayat penjualan untuk Manager."""
    def __init__(self, data_transaksi):
        self.data_transaksi = data_transaksi

    def generate(self):
        TerminalDesign.print_header("LAPORAN RIWAYAT TRANSAKSI")
        if not self.data_transaksi:
            print("   (Belum ada transaksi tercatat)")
            return

        total_omzet = 0
        for t in self.data_transaksi:
            # Mengambil data dari dictionary (karena transaksi di toko.py disimpan sebagai dict)
            idx = t.get('id', 'N/A')
            tgl = t.get('tanggal', '-')[:16] # Ambil YYYY-MM-DD HH:MM
            total = t.get('total', 0)
            total_omzet += total
            
            print(f" 📑 {idx:<15} | 📅 {tgl} | 💰 Rp{total:>12,.0f}")

        print("-" * 65)
        print(f"{TerminalDesign.BOLD}TOTAL PENDAPATAN : Rp{total_omzet:>36,.0f}{TerminalDesign.ENDC}")

# ==========================================
# LAPORAN LABA (Tambahan Optional Biar Manager Senang)
# ==========================================
class LaporanLaba(Laporan):
    """Laporan khusus untuk melihat keuntungan bersih (Margin)."""
    def __init__(self, toko):
        self.toko = toko

    def generate(self):
        TerminalDesign.print_header("ANALISIS LABA RUGI")
        laba_total = 0
        
        # Logika: Laba dihitung dari (Harga Jual - Harga Modal) x Jumlah Terjual
        # Untuk demonstrasi sederhana, kita hitung potensi laba dari stok yang ada
        for b in self.toko.daftar_barang:
            modal = b.get_harga_modal("manager")
            if isinstance(modal, (int, float)):
                potensi_laba = (b.harga_jual - modal) * b.stok
                laba_total += potensi_laba
        
        TerminalDesign.print_info_box({
            "Total Aset (Modal)": f"Rp{sum(b.get_harga_modal('manager') * b.stok for b in self.toko.daftar_barang if isinstance(b.get_harga_modal('manager'), (int, float))):,.0f}",
            "Proyeksi Laba Bersih": f"Rp{laba_total:,.0f}"
        })