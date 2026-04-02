from datetime import datetime
from detail_transaksi import DetailTransaksi
from log_mixin import LogMixin
from design_output import TerminalDesign

class Transaksi(LogMixin):
    """
    Sistem Transaksi DigiMart Pro. 🛒
    Mengelola keranjang belanja, validasi stok, dan pencetakan struk.
    Menerapkan Mixin untuk pencatatan aktivitas.
    """

    def __init__(self, id_transaksi, nama_kasir="System"):
        # Inisialisasi LogMixin
        super().__init__()
        self.id_transaksi = id_transaksi
        self.nama_kasir = nama_kasir
        self.daftar_barang = [] # List of DetailTransaksi objects
        self.tanggal = datetime.now()
        self.selesai = False
        
        # --- TAMBAHAN UNTUK FITUR STRUK ---
        self.bayar = 0
        self.kembali = 0

    def tambah_barang(self, barang, jumlah):
        """Menambahkan item ke dalam keranjang belanja."""
        if barang is None:
            raise ValueError("Barang tidak ditemukan!")
        if jumlah <= 0:
            raise ValueError("Jumlah pembelian tidak valid!")
        if jumlah > barang.stok:
            raise ValueError(f"Stok '{barang.nama}' tidak mencukupi!")

        # Menggunakan class DetailTransaksi (Composition)
        detail = DetailTransaksi(barang, jumlah)
        self.daftar_barang.append(detail)

    def hapus_barang(self, nama_pencarian):
        """Menghapus item dari keranjang berdasarkan nama."""
        self.daftar_barang = [
            item for item in self.daftar_barang 
            if item.barang.nama.lower() != nama_pencarian.lower()
        ]

    def hitung_total(self):
        """Menghitung total belanja seluruh item di keranjang."""
        return sum(item.subtotal() for item in self.daftar_barang)

    def proses_transaksi(self, uang_bayar):
        """Memvalidasi pembayaran dan memotong stok barang di gudang."""
        total = self.hitung_total()
        if not self.daftar_barang:
            raise ValueError("Keranjang belanja masih kosong!")
        
        if uang_bayar < total:
            raise ValueError(f"Uang tidak cukup! Kurang: Rp{total - uang_bayar:,.0f}")

        # Kurangi stok untuk setiap barang (Persistence Logic)
        for item in self.daftar_barang:
            item.barang.kurangi_stok(item.jumlah)

        self.selesai = True
        return uang_bayar - total # Mengembalikan uang kembalian

    def cetak_struk(self):
        """Menghasilkan struk belanja yang rapi dalam format list string."""
        lebar = 50
        struk = []
        struk.append("=" * lebar)
        struk.append("DIGIMART PRO - DIGITAL SUPERMARKET".center(lebar))
        struk.append(f"ID TRX : {self.id_transaksi}".center(lebar))
        struk.append(f"Kasir  : {self.nama_kasir}".center(lebar))
        struk.append(f"Waktu  : {self.tanggal.strftime('%Y-%m-%d %H:%M')}".center(lebar))
        struk.append("-" * lebar)

        for item in self.daftar_barang:
            # Contoh: Mie Instan x3  Rp9,000
            nama = item.barang.nama[:20]
            info_item = f"{nama:<20} x{int(item.jumlah):<3} Rp{item.subtotal():>12,.0f}"
            struk.append(info_item)

        struk.append("-" * lebar)
        struk.append(f"TOTAL       : Rp{self.hitung_total():>12,.0f}")
        
        # --- PERBAIKAN STRUK: MENAMPILKAN TUNAI & KEMBALIAN ---
        struk.append(f"TUNAI       : Rp{self.bayar:>12,.0f}")
        struk.append(f"KEMBALIAN   : Rp{self.kembali:>12,.0f}")
        # ------------------------------------------------------
        
        struk.append("=" * lebar)
        struk.append("Terima Kasih Atas Kunjungan Anda".center(lebar))
        return "\n".join(struk)

    def is_kosong(self):
        return len(self.daftar_barang) == 0

    def input_barang(self, toko):
        """Loop interaktif untuk kasir memasukkan barang belanjaan."""
        TerminalDesign.print_header("INPUT KERANJANG BELANJA")
        
        while True:
            TerminalDesign.print_info_box({
                "ID TRX": self.id_transaksi,
                "TOTAL": f"Rp{self.hitung_total():,.0f}",
                "ITEM": len(self.daftar_barang)
            }, width=50)

            nama = TerminalDesign.input_styled("Nama Barang (Kosongkan untuk Selesai)")
            
            if not nama:
                break

            barang = toko.cari_barang(nama)
            if barang is None:
                TerminalDesign.print_error("Barang tidak ditemukan!")
                continue

            try:
                # --- PERBAIKAN: Hitung stok virtual (Stok asli dikurangi yang ada di keranjang) ---
                stok_di_keranjang = sum(item.jumlah for item in self.daftar_barang if item.barang.nama == barang.nama)
                stok_tersedia = barang.stok - stok_di_keranjang

                print(f"Produk: {barang.nama} | Stok Tersedia: {int(stok_tersedia)}")
                if stok_tersedia <= 0:
                    TerminalDesign.print_error("Barang ini sudah habis dimasukkan ke keranjang semua!")
                    continue

                jumlah = int(TerminalDesign.input_styled(f"Jumlah Beli ({barang.nama})"))
                
                # Validasi agar tidak bisa input lebih dari stok yang tersisa
                if jumlah > stok_tersedia:
                    TerminalDesign.print_error(f"Stok tidak cukup! Hanya bisa menambah maksimal {stok_tersedia} lagi.")
                    continue
                # ----------------------------------------------------------------------------------
                
                self.tambah_barang(barang, jumlah)
                TerminalDesign.print_success(f"{barang.nama} ditambahkan ke keranjang.")

                lanjut = TerminalDesign.input_styled("Tambah lagi? (y/n)")
                if lanjut.lower() != 'y':
                    break
            except Exception as e:
                TerminalDesign.print_error(str(e))

        # Tampilkan Ringkasan Akhir
        if not self.is_kosong():
            TerminalDesign.clear_screen()
            TerminalDesign.print_header("RINGKASAN BELANJA")
            for item in self.daftar_barang:
                print(f" • {item.barang.nama:<20} x{item.jumlah:<3} = Rp{item.subtotal():,.0f}")
            print(f"\n{TerminalDesign.BOLD}TOTAL HARUS DIBAYAR: Rp{self.hitung_total():,.0f}{TerminalDesign.ENDC}")