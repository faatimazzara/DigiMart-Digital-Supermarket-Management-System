from laporan import Laporan
from design_output import TerminalDesign

class LaporanTransaksi(Laporan):
    """
    Subclass LaporanTransaksi. 💰
    Menampilkan riwayat penjualan lengkap beserta total omzet harian.
    Implementasi dari Abstract Base Class Laporan.
    """

    def __init__(self, data_transaksi):
        # Mengambil data dari list transaksi yang ada di Toko
        self.data_transaksi = data_transaksi

    def generate(self):
        """
        Menghasilkan laporan keuangan ringkas di terminal.
        Menampilkan ID, Waktu, dan Nominal setiap transaksi.
        """
        TerminalDesign.print_header("LAPORAN RIWAYAT TRANSAKSI PENJUALAN")

        if not self.data_transaksi:
            print(f"{TerminalDesign.YELLOW}   [!] Belum ada transaksi yang tercatat hari ini.{TerminalDesign.ENDC}")
            return

        # Header Tabel
        header = f"{'ID Transaksi':<18} | {'Waktu':<19} | {'Total Bayar':>15}"
        print(f"{TerminalDesign.BOLD}{header}{TerminalDesign.ENDC}")
        print("-" * len(header))

        total_omzet = 0

        for t in self.data_transaksi:
            # Karena data transaksi di toko.py disimpan sebagai dictionary:
            id_tx = t.get('id', 'N/A')
            waktu = t.get('tanggal', '-')[:19] # Memotong string ISO date agar rapi
            total = t.get('total', 0)
            
            total_omzet += total

            # Mencetak baris transaksi dengan format mata uang yang rapi
            print(f" {id_tx:<17} | {waktu:<19} | Rp{total:>13,.0f}")

        print("-" * len(header))
        
        # Ringkasan Pendapatan (Highlight Hijau)
        print(f"{TerminalDesign.GREEN}{TerminalDesign.BOLD}"
              f"{'TOTAL PENDAPATAN (OMZET)':<40} : Rp{total_omzet:>13,.0f}"
              f"{TerminalDesign.ENDC}")
        
        # Menampilkan info box tambahan
        summary = {
            "Jumlah Transaksi": f"{len(self.data_transaksi)} Nota",
            "Rata-rata/Nota": f"Rp{total_omzet/len(self.data_transaksi) if self.data_transaksi else 0:,.0f}",
            "Status Laporan": "FINAL & TERVERIFIKASI"
        }
        TerminalDesign.print_info_box(summary, width=50)