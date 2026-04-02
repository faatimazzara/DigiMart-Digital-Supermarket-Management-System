from datetime import datetime
from design_output import TerminalDesign

class LogSystem:
    """
    Sistem Penyimpanan Audit Log DigiMart Pro. 📜
    Menampung seluruh riwayat aktivitas dari Manager, Kasir, dan Staff Gudang.
    """

    def __init__(self):
        # List internal untuk menyimpan pesan log
        self.logs = []

    def tambah_log(self, log_message):
        """
        Menambahkan entri log baru.
        Menerima string pesan dari LogMixin (User).
        """
        if log_message:
            # Menyimpan log dalam list
            self.logs.append(log_message)

    def lihat_log(self):
        """
        Mengambil seluruh riwayat log.
        Dibalik (reverse) agar aktivitas terbaru muncul di paling atas.
        """
        if not self.logs:
            return ["(Belum ada aktivitas tercatat)"]
            
        # Mengembalikan copy list yang sudah dibalik urutannya
        return self.logs[::-1]

    def bersihkan_log(self):
        """Fitur opsional untuk mengosongkan riwayat log."""
        self.logs = []
        TerminalDesign.print_success("Riwayat aktivitas telah dibersihkan.")

    def get_jumlah_log(self):
        """Menghitung total aktivitas yang tercatat."""
        return len(self.logs)

    def tampilkan_log_ke_terminal(self, limit=20):
        """Format khusus untuk ditampilkan di menu Audit Log Manager."""
        TerminalDesign.print_header("AUDIT LOG SISTEM")
        riwayat = self.lihat_log()
        
        # Ambil maksimal sejumlah limit (misal 20 log terakhir)
        untuk_ditampilkan = riwayat[:limit]
        
        for entry in untuk_ditampilkan:
            # Memberikan warna biru informatif untuk setiap baris log
            print(f" {TerminalDesign.BLUE}•{TerminalDesign.ENDC} {entry}")
        
        if len(riwayat) > limit:
            print(f"\n... ({len(riwayat) - limit} log lainnya disembunyikan) ...")