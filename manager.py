from user import User
from design_output import TerminalDesign

class Manager(User):
    """
    Subclass Manager. 💼
    Memiliki hak akses penuh (Super User) untuk manajemen barang, user, dan keuangan.
    Mewarisi sifat User dan LogMixin, serta menerapkan Role-Based Access Control (RBAC).
    """

    def __init__(self, username, password, nama_lengkap="Manager Toko"):
        # Memanggil constructor induk (User) dengan menetapkan role 'manager' secara otomatis
        super().__init__(username, password, "manager", nama_lengkap)

    def get_akses_menu(self):
        """Implementasi method abstrak untuk menampilkan menu khusus Manager (Polymorphism)."""
        return [
            "[1] Dashboard Ringkasan Toko",
            "[2] Tambah Produk Baru",
            "[3] Hapus Produk Sistem",
            "[4] Update Harga Jual",
            "[5] Lihat Riwayat Transaksi",
            "[6] Laporan Keuangan (Laba)",
            "[7] Registrasi User Baru",
            "[8] Lihat Daftar Barang",
            "[9] Audit Log Sistem"
        ]

    # ==============================================================================
    # 1. FITUR DASHBOARD & MONITORING
    # ==============================================================================
    def dashboard(self, toko):
        """Menampilkan ringkasan performa toko dalam box informasi UI."""
        TerminalDesign.print_header("DASHBOARD MANAGER")
        
        info = {
            "Total Produk": f"{len(toko.daftar_barang)} Item",
            "Total Transaksi": f"{len(toko.daftar_transaksi)} Nota",
            "Total Pendapatan": f"Rp{toko.total_pendapatan():,}"
        }
        TerminalDesign.print_info_box(info)

    def lihat_barang(self, toko):
        """Mendelegasikan tampilan stok ke class LaporanStok."""
        from laporan_stok import LaporanStok # Import di dalam untuk menghindari circular import
        lap = LaporanStok(toko.daftar_barang)
        lap.generate()

    # ==============================================================================
    # 2. MANAJEMEN INVENTARIS (AKSI SUPERVISI)
    # ==============================================================================
    def tambah_barang(self, toko, barang):
        """Aksi Manager untuk meregistrasi SKU (barang) baru ke database."""
        try:
            # Panggil fungsi di toko.py dan lempar objek 'self' (Manager) untuk dicatat lognya
            toko.tambah_barang(barang, self) 
            TerminalDesign.print_success(f"Produk '{barang.nama}' berhasil didaftarkan!")
        except Exception as e:
            TerminalDesign.print_error(f"Gagal menambah barang: {e}")

    def hapus_barang(self, toko, nama_barang):
        """Aksi Manager untuk menghapus (write-off) barang dari sistem."""
        berhasil = toko.hapus_barang(nama_barang)
        if berhasil:
            # Mencatat log aktivitas penghapusan
            log_msg = f"Menghapus produk dari sistem: {nama_barang}"
            toko.log_system.tambah_log(self.log(log_msg))
            
            TerminalDesign.print_success(f"Produk '{nama_barang}' telah dihapus.")
        else:
            TerminalDesign.print_error(f"Produk '{nama_barang}' tidak ditemukan di database!")

    def ubah_harga_jual(self, toko, nama_barang, harga_baru):
        """Mengubah harga jual dengan validasi proteksi margin."""
        barang = toko.cari_barang(nama_barang)
        
        if not barang:
            TerminalDesign.print_error(f"Produk '{nama_barang}' tidak ditemukan!")
            return

        try:
            # Terapkan perubahan
            barang.harga_jual = harga_baru
            toko.save_barang() # Simpan ke database JSON
            
            # Catat ke sistem log audit
            log_msg = f"Ubah harga '{barang.nama}' menjadi Rp{harga_baru:,}"
            toko.log_system.tambah_log(self.log(log_msg))
            
            TerminalDesign.print_success(f"Harga {barang.nama} berhasil diperbarui!")
            
        except Exception as e:
            TerminalDesign.print_error(f"Gagal memproses ubah harga: {e}")

    # ==============================================================================
    # 3. MANAJEMEN KEUANGAN & AUDIT
    # ==============================================================================
    def lihat_riwayat_transaksi(self, toko):
        """Menampilkan daftar riwayat penjualan dari database JSON."""
        TerminalDesign.print_header("RIWAYAT TRANSAKSI PENJUALAN")
        
        if not toko.daftar_transaksi:
            print("   (Belum ada data transaksi yang tercatat hari ini)")
            return

        for t in toko.daftar_transaksi:
            try:
                # Key dictionary disesuaikan dengan fungsi tambah_transaksi di toko.py
                print(f" 📑 ID: {t['id']:<18} | 📅 {t['tanggal'][:16]} | 💰 Total: Rp{t['total']:>10,}")
            except KeyError:
                continue

    def laporan_keuangan(self, toko):
        """Mendelegasikan kalkulasi laba/rugi ke class LaporanKeuangan."""
        from laporan_keuangan import LaporanKeuangan
        lap = LaporanKeuangan(toko)
        lap.generate()

    def lihat_log_aktivitas(self, toko):
        """Mengakses kotak hitam (Black Box) aktivitas sistem."""
        TerminalDesign.print_header("AUDIT LOG SISTEM (BLACK BOX)")
        
        logs = toko.lihat_log()
        
        if not logs or logs == ["(Belum ada aktivitas tercatat)"]:
            print("   (Tidak ada log aktivitas)")
            return
            
        # Menampilkan 20 log terakhir agar terminal tidak terlalu penuh
        for l in logs[-20:]: 
            print(f" {l}")

    # ==============================================================================
    # 4. MANAJEMEN USER (HRD)
    # ==============================================================================
    def tambah_karyawan_baru(self, auth_system, username, password, role):
        """Mendaftarkan akun karyawan baru (Kasir/Gudang) ke sistem Auth."""
        try:
            # Memanggil fungsi register yang ada di auth.py
            auth_system.register(username, password, role)
        except Exception as e:
            TerminalDesign.print_error(f"Gagal mendaftarkan user: {e}")

    def hapus_karyawan(self, auth_system, username):
        """Aksi Manager untuk menghapus akun karyawan."""
        try:
            auth_system.hapus_user(username)
            TerminalDesign.print_success(f"Akun karyawan '{username}' berhasil dihapus secara permanen!")
        except Exception as e:
            TerminalDesign.print_error(f"Gagal menghapus karyawan: {e}")
    # ==============================================================================
    # OVERRIDES
    # ==============================================================================
    def hapus_karyawan(self, auth_system, username):
        """Aksi Manager untuk menghapus akun karyawan melalui AuthSystem."""
        try:
            # Memanggil fungsi hapus_user yang sudah kita buat di auth.py tadi
            auth_system.hapus_user(username)
            TerminalDesign.print_success(f"Akun karyawan '{username}' berhasil dihapus secara permanen!")
        except Exception as e:
            # Menampilkan pesan error jika user tidak ditemukan atau alasan lainnya
            TerminalDesign.print_error(f"Gagal menghapus karyawan: {e}")

    def to_dict(self):
        """Memanggil format to_dict dari kelas induk User."""
        return super().to_dict()

    def __str__(self):
        """Representasi nama dan jabatan saat objek di-print."""
        return f"💼 Manager: {self.nama_lengkap}"