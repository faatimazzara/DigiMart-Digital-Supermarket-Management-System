from laporan import Laporan
from design_output import TerminalDesign

class LaporanKeuangan(Laporan):
    """
    Subclass LaporanKeuangan. 💹
    Menganalisis kesehatan finansial toko berdasarkan Modal vs Harga Jual.
    Hanya bisa diakses oleh Manager karena mengandung data sensitif (Harga Modal).
    """

    def __init__(self, toko):
        # Mengambil referensi seluruh objek Toko
        self.toko = toko

    def generate(self):
        """
        Menghasilkan analisis laba rugi (Profit & Loss).
        Menghitung selisih harga untuk setiap item dalam stok.
        """
        TerminalDesign.print_header("ANALISIS MARGIN & LABA TERPROYEKSI")
        
        if not self.toko.daftar_barang:
            print("   (Data barang kosong, tidak bisa menghitung keuangan)")
            return

        print(f"{'Nama Produk':<25} | {'Modal':>12} | {'Jual':>12} | {'Laba/Unit':>12}")
        print("-" * 70)

        total_modal_aset = 0
        total_proyeksi_laba = 0

        for b in self.toko.daftar_barang:
            # Mengambil harga modal dengan hak akses 'manager'
            modal = b.get_harga_modal("manager")
            
            # Validasi jika modal adalah angka (bukan "Akses Ditolak")
            if isinstance(modal, (int, float)):
                jual = b.harga_jual
                laba_per_unit = jual - modal
                stok = b.stok
                
                total_modal_aset += (modal * stok)
                total_proyeksi_laba += (laba_per_unit * stok)

                print(f"{b.nama[:25]:<25} | {modal:>12,.0f} | {jual:>12,.0f} | {laba_per_unit:>12,.0f}")

        print("-" * 70)

        # Ringkasan Eksekutif dalam Box
        ringkasan = {
            "Total Aset (Modal)": f"Rp{total_modal_aset:,.0f}",
            "Total Omzet Berjalan": f"Rp{self.toko.total_pendapatan():,.0f}",
            "Proyeksi Laba Bersih": f"Rp{total_proyeksi_laba:,.0f}",
            "Margin Keuntungan": f"{(total_proyeksi_laba / total_modal_aset * 100) if total_modal_aset > 0 else 0:.1f}%"
        }
        
