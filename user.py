from abc import ABC, abstractmethod
from log_mixin import LogMixin

class User(ABC, LogMixin):
    """
    Abstract Base Class untuk pengguna sistem DigiMart Pro. 👤
    Mengelola kredensial login dengan enkapsulasi (Private Attributes).
    Mewarisi LogMixin agar setiap subclass (Manager, Kasir, Staff) bisa mencatat log.
    """

    def __init__(self, username, password, role, nama_lengkap="Karyawan"):
        # Inisialisasi dari LogMixin untuk fitur log aktivitas
        LogMixin.__init__(self)
        
        # Atribut Private (Encapsulation) untuk keamanan
        self.__username = username
        self.__password = password
        
        # Atribut Public
        self.role = role
        self.nama_lengkap = nama_lengkap
        self.is_login = False

    # ==========================================
    # ENKAPSULASI: GETTER & SETTER
    # ==========================================
    def get_username(self):
        """Getter aman untuk mengambil username."""
        try:
            return self.__username
        except Exception as e:
            print(f"Error ambil username: {e}")
            return None

    def check_password(self, password):
        """Verifikasi password tanpa mengekspos password asli."""
        try:
            if password is None:
                return False
            return self.__password == password
        except Exception as e:
            print(f"Error cek password: {e}")
            return False

    # ==========================================
    # MANAJEMEN SESI (LOGIN/LOGOUT)
    # ==========================================
    def login(self):
        """Mengubah status menjadi sedang aktif."""
        try:
            self.is_login = True
        except Exception as e:
            print(f"Error saat login: {e}")

    def logout(self):
        """Mengakhiri sesi pengguna."""
        try:
            self.is_login = False
            print(f"\n{self.nama_lengkap} telah keluar dari sistem.")
        except Exception as e:
            print(f"Error saat logout: {e}")

    def is_authenticated(self):
        """Mengecek apakah pengguna sudah login."""
        try:
            return self.is_login
        except Exception as e:
            print(f"Error cek autentikasi: {e}")
            return False

    # ==========================================
    # POLYMORPHISM: ABSTRACT METHOD
    # ==========================================
    @abstractmethod
    def get_akses_menu(self):
        """
        Method abstrak (Polymorphism).
        Setiap subclass wajib menentukan daftar menu yang bisa diakses.
        """
        pass

    # ==========================================
    # DATA PERSISTENCE (JSON READY)
    # ==========================================
    def to_dict(self):
        """Format data untuk disimpan ke user.json."""
        return {
            "username": self.__username,
            "password": self.__password,
            "role": self.role,
            "nama": self.nama_lengkap
        }

    def __str__(self):
        """Representasi string saat objek di-print."""
        return f"{self.nama_lengkap} ({self.role.upper()})"