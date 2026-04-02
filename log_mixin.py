from datetime import datetime

class LogMixin:
    """
    Mixin untuk pencatatan aktivitas sistem dengan Emoji & Warna. 📝
    Membantu Audit Internal toko agar lebih mudah dibaca dan profesional.
    Menerapkan konsep Multiple Inheritance di PBO.
    """
    
    def __init__(self):
        # Inisialisasi list internal untuk menyimpan riwayat log (Audit Trail)
        self._logs = []

    # --- Tabel Warna ANSI ---
    C = {
        "GUDANG": "\033[96m",     # 📦 Cyan
        "KASIR": "\033[92m",      # 🛒 Hijau
        "MANAGER": "\033[95m",    # 💼 Magenta
        "ERROR": "\033[91m",      # ❌ Merah
        "SUCCESS": "\033[1;92m",  # ✅ Hijau Tebal
        "INFO": "\033[94m",       # ℹ️ Biru
        "SYSTEM": "\033[93m",     # ⚙️ Kuning (Sistem fallback)
        "RESET": "\033[0m"        # Reset Warna
    }

    def log_aktivitas(self, role: str, pesan: str):
        """
        Mencetak log langsung ke terminal dengan icon sesuai role
        dan mengembalikannya agar bisa disimpan oleh LogSystem Toko.
        """
        # Pemetaan Icon sesuai konteks aktivitas
        icon = {
            "GUDANG": "📦", 
            "KASIR": "🛒", 
            "MANAGER": "💼", 
            "ERROR": "❌", 
            "SUCCESS": "✅", 
            "INFO": "ℹ️",
            "SYSTEM": "⚙️"
        }
        
        waktu = datetime.now().strftime("%H:%M:%S")
        role_upper = str(role).upper() if role else "SYSTEM"
        
        # Mengambil warna dan emoji, jika tidak ada pakai default
        warna = self.C.get(role_upper, self.C["INFO"])
        emoji = icon.get(role_upper, "🔹")
        reset = self.C["RESET"]
        
        # Format string log untuk tampilan di layar (dengan ANSI)
        log_entry_layar = f"{warna}[{waktu}] {emoji} [{role_upper}] {pesan}{reset}"
        print(log_entry_layar) # Cetak langsung saat aksi terjadi
        
        # Format string bersih (tanpa ANSI) untuk disimpan ke memori/JSON
        log_entry_bersih = f"[{waktu}] [{role_upper}] {pesan}"
        self._logs.append(log_entry_bersih)
        
        return log_entry_bersih

    def log(self, pesan: str):
        """
        FUNGSI FIX: Alias method agar pemanggilan self.log(pesan) 
        dari Manager/Kasir/Gudang berfungsi tanpa Error.
        """
        # Mengambil atribut 'role' dari class User secara dinamis.
        # Jika belum ada role, gunakan 'SYSTEM' sebagai fallback aman.
        role_saat_ini = getattr(self, 'role', 'SYSTEM')
        
        # Teruskan ke fungsi utama log_aktivitas
        return self.log_aktivitas(role_saat_ini, pesan)

    def garis_log(self):
        """Mencetak garis pembatas log yang estetik."""
        print("\033[90m" + "─" * 60 + "\033[0m")

    def log_pembatas(self):
        """Menambahkan pembatas teks ke dalam riwayat log internal."""
        self._logs.append("=" * 40)

    def get_logs(self):
        """Mengambil seluruh riwayat aktivitas yang tersimpan."""
        return self._logs

# ==========================================
# MIXIN LAINNYA (TETAP DIPERTAHANKAN)
# ==========================================

class DiskonMixin:
    """Mixin untuk menangani perhitungan diskon transaksi."""
    def hitung_diskon(self, total, diskon):
        if diskon < 0 or diskon > 1:
            raise ValueError("Diskon harus antara 0 - 1 (Contoh: 0.1 untuk 10%)")
        return total - (total * diskon)

class TimestampMixin:
    """Mixin untuk memberikan stempel waktu pada objek (Barang/Transaksi)."""
    def get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")