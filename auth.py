from database import Database
from manager import Manager
from kasir import Kasir
from gudang import StaffStok
from design_output import TerminalDesign

class AuthSystem:
    """
    Sistem Otentikasi & Otorisasi DigiMart Pro. 🔐
    Mengelola proses login, registrasi, dan pemuatan user dari database JSON.
    """

    def __init__(self):
        # Path ke file database user
        self.db = Database("database/user.json")
        self.__current_user = None

        # FIX: Inisialisasi User Default jika database kosong
        try:
            data = self.db.load()
        except Exception:
            data = []

        if not data:
            default_users = [
                {"username": "admin", "password": "111", "role": "manager", "nama": "Admin Utama"},
                {"username": "kasir", "password": "222", "role": "kasir", "nama": "Siti Kasir"},
                {"username": "staff", "password": "333", "role": "staff_stok", "nama": "Budi Gudang"}
            ]
            try:
                self.db.save(default_users)
            except Exception as e:
                TerminalDesign.print_error(f"Gagal membuat user default: {e}")

    def load_users(self):
        """Membaca data JSON dan menginstansiasi objek User sesuai Role-nya."""
        try:
            data = self.db.load()
        except Exception:
            data = []

        users = []
        for u in data:
            try:
                # Factory Logic: Membuat objek berdasarkan role (Polymorphism)
                if u["role"] == "manager":
                    users.append(Manager(u["username"], u["password"], u.get("nama", "Manager")))
                elif u["role"] == "kasir":
                    users.append(Kasir(u["username"], u["password"], u.get("nama", "Kasir")))
                elif u["role"] == "staff_stok":
                    users.append(StaffStok(u["username"], u["password"], u.get("nama", "Staff Gudang")))
            except Exception as e:
                print(f"Error instansiasi user {u.get('username')}: {e}")

        return users

    def login(self, username, password):
        """Memverifikasi username dan password."""
        if not username or not password:
            TerminalDesign.print_warning("Username dan password wajib diisi!")
            return None

        # Simulasi proses pengecekan database
        TerminalDesign.loading_bar(0.6, "Memverifikasi Kredensial...")
        
        all_users = self.load_users()

        for user in all_users:
            try:
                if user.get_username() == username:
                    if user.check_password(password):
                        user.login() # Mengubah is_login menjadi True
                        self.__current_user = user
                        TerminalDesign.print_success(f"Selamat Datang, {user.nama_lengkap}!")
                        return user
                    else:
                        TerminalDesign.print_error("Password yang Anda masukkan salah!")
                        return None
            except Exception as e:
                TerminalDesign.print_error(f"Kegagalan sistem login: {e}")

        TerminalDesign.print_error("User tidak ditemukan di database kami.")
        return None

    def register(self, username, password, role, nama="Karyawan Baru"):
        """Menambahkan user baru ke database (Hanya bisa dipanggil oleh Manager)."""
        if not username or not password or not role:
            TerminalDesign.print_error("Gagal Registrasi: Field tidak lengkap!")
            return

        try:
            data = self.db.load()
        except Exception:
            data = []

        # Validasi Duplikasi Username
        if any(u["username"] == username for u in data):
            TerminalDesign.print_warning(f"Username '{username}' sudah terdaftar!")
            return

        # Tambahkan data baru
        data.append({
            "username": username,
            "password": password,
            "role": role,
            "nama": nama
        })

        try:
            self.db.save(data)
            TerminalDesign.print_success(f"Akun {username} sebagai {role} berhasil dibuat.")
        except Exception as e:
            TerminalDesign.print_error(f"Gagal menyimpan ke JSON: {e}")

    def logout(self):
        """Mengosongkan sesi user aktif."""
        if self.__current_user:
            self.__current_user.logout()
            self.__current_user = None
            TerminalDesign.print_success("Sesi berakhir. Anda telah logout.")

    def hapus_user(self, username):
        """Menghapus user dari database JSON tanpa batasan role."""
        try:
            # 1. Muat data terbaru dari database
            data = self.db.load()
        except Exception:
            data = []

        # 2. Cari user yang akan dihapus
        user_target = next((u for u in data if u["username"] == username), None)

        if not user_target:
            raise ValueError(f"Username '{username}' tidak ditemukan di sistem!")

        # --- PERBAIKAN: Proteksi dihapus agar Manager bisa hapus siapa saja ---
        # Kita hanya berikan peringatan kecil di log jika yang dihapus adalah manager
        if user_target.get("role") == "manager":
            TerminalDesign.print_warning(f"Perhatian: Akun Manager '{username}' akan dihapus.")

        # 4. Buat list baru tanpa user tersebut
        data_baru = [u for u in data if u["username"] != username]

        # 5. Simpan kembali ke file JSON
        try:
            self.db.save(data_baru)
            return True
        except Exception as e:
            raise Exception(f"Gagal menyimpan ke database: {e}")