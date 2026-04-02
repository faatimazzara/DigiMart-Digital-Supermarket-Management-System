import os
import json
from design_output import TerminalDesign

class Database:
    """
    Sistem Manajemen File JSON DigiMart Pro. 💾
    Menangani persistensi data (Read, Write, Add) untuk Barang, User, dan Transaksi.
    """

    def __init__(self, path):
        # Path file (Contoh: 'database/barang.json')
        self.path = path

        # 🔥 Pastikan folder 'database' ada (Logika kodinganmu)
        folder = os.path.dirname(self.path)
        if folder and not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as e:
                print(f"Error create folder: {e}")

        # 🔥 Buat file JSON kosong jika belum ada
        if not os.path.exists(self.path):
            try:
                with open(self.path, "w") as f:
                    json.dump([], f)
            except Exception as e:
                print(f"Error create file: {e}")

    # ========================
    # READ DATA (Muat Data)
    # ========================
    def read(self):
        """Membaca isi file JSON dan mengembalikannya dalam bentuk list."""
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except Exception:
            # Jika file korup atau tidak terbaca, kembalikan list kosong
            return []

    # ========================
    # WRITE DATA (Simpan Data)
    # ========================
    def write(self, data):
        """Menulis data ke file JSON dengan format indentasi 4 agar rapi."""
        try:
            with open(self.path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            TerminalDesign.print_error(f"Gagal menulis ke {self.path}: {e}")

    # ========================
    # ADD DATA (Tambah Data)
    # ========================
    def add(self, item):
        """Menambah satu item baru ke dalam file JSON secara langsung."""
        data = self.read()
        data.append(item)
        self.write(data)

    # --- Alias Method (Agar sinkron dengan AuthSystem & StokManager) ---
    
    def load(self):
        """Alias untuk fungsi read."""
        return self.read()

    def save(self, data):
        """Alias untuk fungsi write."""
        self.write(data)

    def is_empty(self):
        """Mengecek apakah database memiliki isi atau kosong."""
        return len(self.read())