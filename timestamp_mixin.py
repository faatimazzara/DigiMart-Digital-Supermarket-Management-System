from datetime import datetime

class TimestampMixin:
    """
    Mixin untuk memberikan stempel waktu otomatis pada objek. ⏳
    Digunakan oleh kelas Barang dan Transaksi untuk pencatatan 
    waktu pembuatan atau pembaruan data secara real-time.
    """

    def __init__(self):
        # Menyimpan waktu saat objek pertama kali dibuat
        self.__created_at = datetime.now()

    def get_timestamp(self):
        """
        Mengambil string waktu saat ini dengan format standar Indonesia.
        Format: YYYY-MM-DD HH:MM:SS
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_created_at(self):
        """
        Mengambil waktu pembuatan objek dalam format yang mudah dibaca.
        """
        return self.__created_at.strftime("%d/%m/%Y %H:%M:%S")

    def format_date_custom(self, date_obj):
        """
        Helper untuk memformat objek datetime tertentu menjadi 
        format laporan yang rapi (Contoh: 02 April 2026).
        """
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%d %B %Y")
        return str(date_obj)

    def log_time_info(self):
        """
        Mencetak informasi waktu ke terminal dengan warna biru informasi.
        """
        from design_output import TerminalDesign
        print(f"{TerminalDesign.BLUE}[🕒 TIME] Akses pada: {self.get_timestamp()}{TerminalDesign.ENDC}")