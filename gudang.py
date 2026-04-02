from user import User
from design_output import TerminalDesign

class StaffStok(User):
    """
    Subclass StaffStok (Petugas Gudang). 📦
    """

    def __init__(self, username, password, nama_lengkap="Petugas Gudang"):
        super().__init__(username, password, "staff_stok", nama_lengkap)

    def get_akses_menu(self):
        return [
            "[1] Lihat Stok Inventaris",
            "[2] Registrasi Barang Baru",
            "[3] Update Stok (Restock/Opname)",
            "[4] Update Harga Modal",
            "[5] Laporan Stok Kritis"
        ]

    # --- FITUR UTAMA YANG BERMASALAH ---
    def input_harga_modal(self, toko, nama_barang, harga_baru):
        """Update harga modal dengan pencarian case-insensitive dan auto-save."""
        # 1. Cari barang (bisa ketik 'apel' atau 'Apel' tetap ketemu)
        barang = next((b for b in toko.daftar_barang if b.nama.lower() == nama_barang.lower()), None)
        
        if not barang:
            TerminalDesign.print_error(f"Barang '{nama_barang}' tidak ditemukan di gudang!")
            return

        try:
            # 2. Update harga modal (Gunakan Name Mangling untuk atribut private)
            # Pastikan di file barang.py nama class-nya adalah 'Barang'
            barang._Barang__harga_modal = int(harga_baru)
            
            # 3. WAJIB: Simpan ke database JSON agar permanen
            toko.save_barang()
            
            # 4. Catat aktivitas ke Log
            pesan_log = f"Update harga modal {barang.nama} menjadi Rp{harga_baru:,}"
            toko.log_system.tambah_log(self.log(pesan_log))

            TerminalDesign.print_success(f"Berhasil! Harga modal {barang.nama} sekarang Rp{harga_baru:,}")
            
        except Exception as e:
            TerminalDesign.print_error(f"Gagal update harga: {e}")

    # --- FITUR LAINNYA ---
    def dashboard(self, toko):
        TerminalDesign.print_header("DASHBOARD GUDANG")
        for b in toko.daftar_barang:
            kategori = b.kategori.nama if b.kategori else "-"
            status = f"{TerminalDesign.RED}⚠️ KRITIS{TerminalDesign.ENDC}" if b.stok <= 5 else f"{TerminalDesign.GREEN}AMAN{TerminalDesign.ENDC}"
            print(f" • {b.nama[:15]:<15} | Stok: {int(b.stok):>4} | {status}")

    def update_stok(self, toko, nama_barang, jumlah):
        barang = next((b for b in toko.daftar_barang if b.nama.lower() == nama_barang.lower()), None)
        if barang:
            barang.tambah_stok(jumlah) if jumlah > 0 else barang.kurangi_stok(abs(jumlah))
            toko.save_barang()
            TerminalDesign.print_success(f"Stok {barang.nama} berhasil diupdate!")
        else:
            TerminalDesign.print_error("Barang tidak ditemukan!")

    def to_dict(self):
        return super().to_dict()