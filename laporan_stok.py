from laporan import Laporan
from design_output import TerminalDesign

class LaporanStok(Laporan):
    """
    Subclass LaporanStok. 📊
    Menampilkan tabel persediaan barang secara detail untuk Manager dan Staff Gudang.
    """

    def __init__(self, data_barang):
        # Menyimpan referensi list barang dari Toko
        self.data_barang = data_barang

    def generate(self):
        """
        Implementasi metode generate (Polymorphism).
        Menghasilkan tabel stok dengan indikator warna untuk stok kritis.
        """
        TerminalDesign.print_header("LAPORAN STATUS INVENTARIS GUDANG")

        if not self.data_barang:
            print(f"{TerminalDesign.YELLOW}   [!] Belum ada data barang dalam sistem.{TerminalDesign.ENDC}")
            return

        # Header Tabel yang Presisi
        header = f"{'Nama Produk':<25} | {'Kategori':<15} | {'Stok':<8} | {'Status'}"
        print(f"{TerminalDesign.BOLD}{header}{TerminalDesign.ENDC}")
        print("=" * len(header))

        total_stok_toko = 0
        
        for b in self.data_barang:
            # Mengambil data menggunakan property/getter
            nama = b.nama[:25]
            kat_nama = b.kategori.nama if b.kategori else "Umum"
            stok = b.stok
            total_stok_toko += stok

            # Logika Visual: Merah jika stok <= 5
            if stok <= 5:
                status = f"{TerminalDesign.RED}REFILL NOW{TerminalDesign.ENDC}"
            else:
                status = f"{TerminalDesign.GREEN}SAFE{TerminalDesign.ENDC}"

            # Mencetak baris tabel
            print(f"{nama:<25} | {kat_nama:<15} | {stok:>8} | {status}")

        print("=" * len(header))
        
        # Ringkasan di bawah tabel
        ringkasan = {
            "Total Jenis Produk": f"{len(self.data_barang)} SKU",
            "Total Seluruh Stok": f"{total_stok_toko} Unit",
            "Update Terakhir": TerminalDesign.get_current_time()
        }
        TerminalDesign.print_info_box(ringkasan, width=45)