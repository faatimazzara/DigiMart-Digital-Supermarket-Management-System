from user import User
from design_output import TerminalDesign

class Kasir(User):
    """
    Subclass Kasir. 🛒
    Bertanggung jawab atas operasional penjualan dan pengecekan stok harian.
    Menerapkan Role-Based Access Control (RBAC).
    """

    def __init__(self, username, password, nama_lengkap="Petugas Kasir"):
        # Memanggil constructor induk (User) dengan role 'kasir'
        super().__init__(username, password, "kasir", nama_lengkap)

    def get_akses_menu(self):
        """Implementasi menu khusus untuk role Kasir (Polymorphism)."""
        return [
            "[1] Transaksi Penjualan Baru",
            "[2] Cek Stok Inventaris",
            "[3] Cari Produk Cepat",
            "[4] Riwayat Penjualan Saya"
        ]

    def dashboard(self, toko):
        """Menampilkan daftar barang dengan highlight untuk stok kritis."""
        TerminalDesign.print_header("MONITOR STOK KASIR")
        
        header = f"{'Produk':<25} | {'Kategori':<15} | {'Harga':<12} | {'Stok':<8}"
        print(f"{TerminalDesign.BOLD}{header}{TerminalDesign.ENDC}")
        print("-" * len(header))

        for b in toko.daftar_barang:
            # Logika Peringatan Stok (Sesuai kodinganmu)
            status_icon = f"{TerminalDesign.RED}⚠️ LOW{TerminalDesign.ENDC}" if b.stok <= 5 else f"{TerminalDesign.GREEN}OK{TerminalDesign.ENDC}"
            kategori = b.kategori.nama if b.kategori else "-"
            
            print(f"{b.nama[:25]:<25} | {kategori:<15} | Rp{b.harga_jual:>9,.0f} | {b.stok:>4} {status_icon}")

    def proses_transaksi_baru(self, toko):
        """Modul utama untuk menangani input belanja pelanggan."""
        from transaksi import Transaksi
        
        TerminalDesign.clear_screen()
        TerminalDesign.print_header("TRANSAKSI BARU")
        
        # Inisialisasi ID Transaksi unik
        id_tx = f"TX{toko.get_timestamp_short()}"
        tx = Transaksi(id_tx, self.nama_lengkap)

        # Proses input barang (Logic ada di file transaksi.py)
        tx.input_barang(toko)

        if not tx.keranjang:
            TerminalDesign.print_warning("Transaksi dibatalkan (Keranjang Kosong).")
            return

        # Finalisasi
        try:
            total = tx.hitung_total_akhir()
            TerminalDesign.print_info_box({"TOTAL BELANJA": f"Rp{total:,.0f}"})
            
            bayar = int(TerminalDesign.input_styled("Uang Tunai Pembeli"))
            kembali = tx.proses_pembayaran(bayar)
            
            # Simpan ke Toko & Database
            toko.tambah_transaksi(tx)
            toko.log_aktivitas("KASIR", f"Transaksi {id_tx} Berhasil (Total: Rp{total:,.0f})")
            
            # Cetak Struk
            TerminalDesign.clear_screen()
            print(tx.cetak_struk())
            input("\nTekan Enter untuk transaksi selanjutnya...")
            
        except Exception as e:
            TerminalDesign.print_error(f"Gagal memproses transaksi: {e}")

    def lihat_barang(self, toko):
        """Fitur untuk mencari spesifik barang (Cari Produk Cepat)."""
        TerminalDesign.print_header("CARI PRODUK CEPAT")
        kata_kunci = TerminalDesign.input_styled("Masukkan nama barang yang dicari")
        
        if not kata_kunci:
            return

        # Mencari barang yang namanya mengandung kata kunci (tidak harus sama persis)
        ditemukan = [b for b in toko.daftar_barang if kata_kunci.lower() in b.nama.lower()]

        if not ditemukan:
            TerminalDesign.print_warning(f"Barang dengan kata kunci '{kata_kunci}' tidak ditemukan.")
            return

        # Menampilkan header tabel jika barang ditemukan
        header = f"{'Produk':<25} | {'Kategori':<15} | {'Harga':<12} | {'Stok':<8}"
        print(f"\n{TerminalDesign.BOLD}{header}{TerminalDesign.ENDC}")
        print("-" * len(header))

        # Menampilkan hasil pencarian
        for b in ditemukan:
            status_icon = f"{TerminalDesign.RED}⚠️ LOW{TerminalDesign.ENDC}" if b.stok <= 5 else f"{TerminalDesign.GREEN}OK{TerminalDesign.ENDC}"
            kategori = b.kategori.nama if b.kategori else "-"
            print(f"{b.nama[:25]:<25} | {kategori:<15} | Rp{b.harga_jual:>9,.0f} | {b.stok:>4} {status_icon}")

    def laporan_harian_saya(self, toko):
        """Melihat ringkasan transaksi yang dilakukan oleh kasir yang sedang login."""
        TerminalDesign.print_header(f"LAPORAN HARIAN: {self.nama_lengkap}")
        count = 0
        for t in toko.daftar_transaksi:
            # Menggunakan .get() agar lebih aman dari error
            if t.get('kasir') == self.nama_lengkap:
                # PERBAIKAN: Key diubah menjadi 'id' dan 'total' sesuai database baru
                print(f" • {t.get('id')} | Total: Rp{t.get('total', 0):>10,}")
                count += 1
        
        if count == 0:
            print("(Belum ada transaksi hari ini)")

    def to_dict(self):
        return super().to_dict()