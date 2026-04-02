# ==============================================================================
# PROYEK: DIGIMART PRO - SISTEM MANAJEMEN RITEL TERPADU (V2.0)
# KELOMPOK: TEAM 4
# MATA KULIAH: PEMROGRAMAN BERORIENTASI OBJEK (PBO)
# DESKRIPSI: ENTRY POINT UTAMA SISTEM DENGAN INTEGRASI 33 MODUL
# ==============================================================================

import os
import time
import sys
from datetime import datetime

# --- IMPORT CORE SYSTEMS ---
from auth import AuthSystem
from toko import Toko
from transaksi import Transaksi
from kategori import Kategori
from design_output import TerminalDesign

# --- IMPORT PRODUCT MODELS (POLYMORPHISM & INHERITANCE) ---
from makanan import Makanan
from minuman import Minuman
from rumah_tangga import BarangRumahTangga
from produk_segar import ProdukSegar
from produk_elektronik import ProdukElektronik
from kesehatan_kecantikan import KesehatanKecantikan

# ==============================================================================
# FUNGSI UI: SPLASH SCREEN & LAYAR PEMBUKA
# ==============================================================================

def jalankan_splash_screen():
    """Menampilkan animasi pembuka DigiMart Pro."""
    TerminalDesign.clear_screen()
    TerminalDesign.print_ascii_art()
    
    # Animasi teks berjalan untuk kesan profesional
    TerminalDesign.print_animated_text("Initializing Digital Supermarket Management System...", 0.02)
    TerminalDesign.loading_bar(1.8, "Memuat Modul Sistem & Aset Visual")
    
    print(f"\n{TerminalDesign.YELLOW}{TerminalDesign.BOLD}" + "─"*82)
    print("TEKAN [ENTER] UNTUK MASUK KE SISTEM".center(82))
    print("─"*82 + f"{TerminalDesign.ENDC}")
    input()

def tampilkan_tentang_aplikasi():
    """Menampilkan informasi metadata aplikasi dan tim pengembang."""
    TerminalDesign.clear_screen()
    TerminalDesign.print_header("TENTANG DIGIMART PRO V2.0")
    
    info_aplikasi = {
        "NAMA APLIKASI": "DigiMart Pro (Digital Supermarket Management)",
        "VERSI": "2.0.4 - Enterprise Edition",
        "BAHASA": "Python 3.x (Object-Oriented Programming)",
        "DATABASE": "JSON Persistence File System",
        "DEVELOPER": "Team 4 - Informatics Engineering",
        "STATUS": "Ujian Tengah Semester (UTS) Project"
    }
    TerminalDesign.print_info_box(info_aplikasi)
    
    print(f"\n{TerminalDesign.CYAN}Deskripsi Sistem:{TerminalDesign.ENDC}")
    TerminalDesign.print_animated_text(
        "DigiMart Pro adalah solusi manajemen ritel modern yang menerapkan\n"
        "prinsip Enkapsulasi, Pewarisan (Inheritance), dan Polimorfisme.\n"
        "Sistem ini dirancang untuk skalabilitas inventaris supermarket.", 0.01
    )
    input(f"\n{TerminalDesign.YELLOW}❯ Tekan Enter untuk kembali...{TerminalDesign.ENDC}")

# ==============================================================================
# FUNGSI NAVIGASI: LOGIN & AUTH
# ==============================================================================

def navigasi_login(auth_system):
    """Antarmuka login dengan penanganan error kredensial."""
    TerminalDesign.clear_screen()
    TerminalDesign.print_header("GERBANG LOGIN DIGIMART")
    
    print(f"{TerminalDesign.BLUE}Otorisasi diperlukan untuk mengakses database toko.{TerminalDesign.ENDC}\n")
    
    user_input = TerminalDesign.input_styled("Username")
    pass_input = TerminalDesign.input_styled("Password")

    if not user_input or not pass_input:
        TerminalDesign.print_error("Username dan Password tidak boleh kosong!")
        return None

    # Simulasi sinkronisasi sebelum login (estetika)
    TerminalDesign.loading_bar(0.8, "Memverifikasi Kredensial")
    
    user_auth = auth_system.login(user_input, pass_input)
    
    if user_auth:
        TerminalDesign.print_success(f"Login Berhasil! Selamat datang {user_auth.nama_lengkap}")
        time.sleep(1)
        return user_auth
    else:
        # Pesan error ditangani di auth.py, di sini hanya delay
        time.sleep(0.5)
        return None

# ==============================================================================
# FUNGSI OPERASIONAL: MANAJEMEN PRODUK
# ==============================================================================

def formulir_input_barang(toko):
    """Proses pembuatan objek barang baru melalui Factory Logic."""
    TerminalDesign.clear_screen()
    TerminalDesign.print_header("REGISTRASI PRODUK BARU")
    
    print(f"{TerminalDesign.BOLD}Pilih Kategori Produk yang akan didaftarkan:{TerminalDesign.ENDC}")
    TerminalDesign.menu_item("1", "MAKANAN (FOOD)")
    TerminalDesign.menu_item("2", "MINUMAN (BEVERAGES)")
    TerminalDesign.menu_item("3", "PERALATAN RUMAH TANGGA")
    TerminalDesign.menu_item("4", "PRODUK SEGAR (FRESH)")
    TerminalDesign.menu_item("5", "ELEKTRONIK & GADGET")
    TerminalDesign.menu_item("6", "KESEHATAN & KECANTIKAN")
    TerminalDesign.menu_item("0", "BATALKAN")

    opsi = input(f"\n{TerminalDesign.YELLOW}❯ Pilihan (0-6): {TerminalDesign.ENDC}")

    if opsi == "0" or opsi not in ["1","2","3","4","5","6"]:
        TerminalDesign.print_warning("Input dibatalkan oleh pengguna.")
        return None

    try:
        # Data Utama (Common Attributes)
        print(f"\n{TerminalDesign.CYAN}--- Data Umum ---{TerminalDesign.ENDC}")
        nama = TerminalDesign.input_styled("Nama Produk")
        if not nama: return None

        modal = int(TerminalDesign.input_styled("Harga Modal (Rp)"))
        jual = int(TerminalDesign.input_styled("Harga Jual (Rp)"))
        stok = int(TerminalDesign.input_styled("Stok Awal"))

        if modal < 0 or jual < 0 or stok < 0:
            TerminalDesign.print_error("Nilai numerik tidak boleh negatif!")
            return None

        kat_input = TerminalDesign.input_styled("Kategori (Opsional)")
        obj_kat = Kategori(kat_input) if kat_input else None

        # Data Spesifik (Sub-Class Specific Attributes)
        print(f"\n{TerminalDesign.CYAN}--- Atribut Spesifik Kategori ---{TerminalDesign.ENDC}")
        
        if opsi == "1": # Makanan
            exp = TerminalDesign.input_styled("Tgl Kadaluarsa (DD/MM/YYYY)")
            return Makanan(nama, modal, jual, stok, exp, obj_kat)

        elif opsi == "2": # Minuman
            vol = int(TerminalDesign.input_styled("Volume (ml)"))
            exp = TerminalDesign.input_styled("Tgl Kadaluarsa")
            return Minuman(nama, modal, jual, stok, vol, exp, obj_kat)

        elif opsi == "3": # Rumah Tangga
            merk = TerminalDesign.input_styled("Merk/Brand")
            return BarangRumahTangga(nama, modal, jual, stok, merk, obj_kat)

        elif opsi == "4": # Produk Segar
            berat = float(TerminalDesign.input_styled("Berat (kg)"))
            msk = TerminalDesign.input_styled("Tgl Masuk")
            exp = TerminalDesign.input_styled("Tgl Kadaluarsa")
            return ProdukSegar(nama, modal, jual, stok, berat, msk, exp, obj_kat)

        elif opsi == "5": # Elektronik
            gar = int(TerminalDesign.input_styled("Garansi (Bulan)"))
            merk = TerminalDesign.input_styled("Merk/Brand")
            return ProdukElektronik(nama, modal, jual, stok, gar, merk, obj_kat)

        elif opsi == "6": # Kesehatan
            exp = TerminalDesign.input_styled("Tgl Kadaluarsa")
            merk = TerminalDesign.input_styled("Merk/Brand")
            return KesehatanKecantikan(nama, modal, jual, stok, exp, merk, obj_kat)

    except ValueError:
        TerminalDesign.print_error("Input Gagal! Harga/Stok harus berupa angka.")
    except Exception as e:
        TerminalDesign.print_error(f"Sistem Gagal Memproses: {e}")
    
    return None

# ==============================================================================
# FUNGSI OPERASIONAL: TRANSAKSI KASIR
# ==============================================================================

def alur_transaksi_kasir(toko, user_kasir):
    """Menjalankan siklus belanja pelanggan dari input hingga struk."""
    TerminalDesign.clear_screen()
    TerminalDesign.print_header("KASIR: POINT OF SALES (POS)")
    
    # Inisialisasi ID unik menggunakan timestamp detik
    id_trx = f"INV-{datetime.now().strftime('%d%m%y-%H%M%S')}"
    transaksi_obj = Transaksi(id_trx, user_kasir.nama_lengkap)

    # Memanggil Input Loop di dalam class Transaksi (OOP Approach)
    transaksi_obj.input_barang(toko)

    if transaksi_obj.is_kosong():
        TerminalDesign.print_warning("Transaksi dibatalkan (Keranjang Kosong).")
        time.sleep(1.2)
        return

    # Sesi Pembayaran
    TerminalDesign.print_sub_header("FINALISASI PEMBAYARAN")
    total_tagihan = transaksi_obj.hitung_total()
    
    TerminalDesign.print_info_box({
        "NO INVOICE": id_trx,
        "JUMLAH ITEM": len(transaksi_obj.daftar_barang),
        "TOTAL TAGIHAN": f"Rp {total_tagihan:,.0f}"
    })

    try:
        bayar = int(TerminalDesign.input_styled("Nominal Bayar (Tunai)"))
        
        # --- PERBAIKAN: Gunakan proses_transaksi() agar stok dipotong otomatis ---
        # Fungsi ini akan memotong stok di keranjang dan menghasilkan nilai kembalian
        kembalian = transaksi_obj.proses_transaksi(bayar)
        
        transaksi_obj.bayar = bayar
        transaksi_obj.kembali = kembalian
        
        # Simpan riwayat transaksi
        toko.tambah_transaksi(transaksi_obj, user_kasir)
        
        # PENTING: Simpan perubahan stok barang yang sudah dipotong ke database JSON
        toko.save_barang() 
        # -------------------------------------------------------------------------
        
        TerminalDesign.print_success(f"Pembayaran Berhasil. Kembalian: Rp {kembalian:,.0f}")
        
        # Cetak Struk
        TerminalDesign.clear_screen()
        TerminalDesign.print_header("BUKTI PEMBAYARAN (STRUK)")
        print(transaksi_obj.cetak_struk())
        TerminalDesign.print_footer()
        input("\nTekan Enter untuk transaksi baru...")

    except ValueError as e:
        # Menangkap error dari proses_transaksi (misal: uang kurang) atau salah input
        TerminalDesign.print_error(str(e))
        input("\nTekan Enter untuk membatalkan transaksi...")

# ==============================================================================
# LOGIKA MENU: ROLE-BASED ACCESS CONTROL (RBAC)
# ==============================================================================

def jalankan_menu_manager(user, toko, auth):
    """Menu khusus Manager (Full Access)."""
    while user.is_login:
        TerminalDesign.clear_screen()
        TerminalDesign.print_header(f"PANEL MANAGER: {user.nama_lengkap.upper()}")
        
        # Dashboard Ringkas di atas menu
        toko_info = {
            "TOTAL PRODUK": f"{len(toko.daftar_barang)} SKU",
            "TOTAL OMZET": f"Rp {toko.total_pendapatan():,.0f}",
            "STOK KRITIS": f"{len(toko.barang_hampir_habis())} Item"
        }
        TerminalDesign.print_info_box(toko_info)

        # Daftar Menu
        TerminalDesign.menu_item("1", "Dashboard Detail")
        TerminalDesign.menu_item("2", "Daftarkan Barang Baru")
        TerminalDesign.menu_item("3", "Hapus Produk Sistem")
        TerminalDesign.menu_item("4", "Update Harga Jual")
        TerminalDesign.menu_item("5", "Lihat Laporan Transaksi")
        TerminalDesign.menu_item("6", "Analisis Laporan Keuangan")
        TerminalDesign.menu_item("7", "Manajemen User (Staff)")
        TerminalDesign.menu_item("8", "Lihat Audit Log Sistem")
        TerminalDesign.menu_item("0", "LOGOUT")

        pilih = input(f"\n{TerminalDesign.YELLOW}❯ Opsi Manager: {TerminalDesign.ENDC}")

        if pilih == "1":
            user.dashboard(toko)
            input("\nKembali...")
        elif pilih == "2":
            brg = formulir_input_barang(toko)
            if brg: 
                user.tambah_barang(toko, brg)
                TerminalDesign.print_success("Barang terdaftar!")
            input("\nKembali...")
        elif pilih == "3":
            nama = input("Nama barang yang akan dihapus: ")
            user.hapus_barang(toko, nama)
            input("\nKembali...")
        elif pilih == "4":
            nama = input("Cari barang: ")
            try:
                hrg = int(input("Harga jual baru: "))
                # Panggil dengan nama yang benar sesuai di manager.py
                user.ubah_harga_jual(toko, nama, hrg)
            except ValueError: 
                TerminalDesign.print_error("Input harus berupa angka bulat!")
            except Exception as e:
                TerminalDesign.print_error(f"Sistem Error: {e}")
            input("\nKembali...")  
        elif pilih == "5":
            user.lihat_riwayat_transaksi(toko)
            input("\nKembali...")
        elif pilih == "6":
            user.laporan_keuangan(toko)
            input("\nKembali...")
        elif pilih == "7":
            TerminalDesign.print_header("MANAJEMEN KARYAWAN (HRD)")
            print(f" {TerminalDesign.CYAN}1. Registrasi Karyawan Baru{TerminalDesign.ENDC}")
            print(f" {TerminalDesign.CYAN}2. Hapus Karyawan{TerminalDesign.ENDC}")
            
            opsi_hrd = input(f"\n{TerminalDesign.YELLOW}❯ Pilih aksi (1/2): {TerminalDesign.ENDC}")
            
            if opsi_hrd == "1":
                TerminalDesign.print_sub_header("TAMBAH KARYAWAN")
                u = TerminalDesign.input_styled("Username Baru")
                p = TerminalDesign.input_styled("Password Baru")
                r = TerminalDesign.input_styled("Role (manager/kasir/staff_stok)")
                user.tambah_karyawan_baru(auth, u, p, r)
            
            elif opsi_hrd == "2":
                TerminalDesign.print_sub_header("HAPUS KARYAWAN")
                u = TerminalDesign.input_styled("Username yang akan dihapus")
                user.hapus_karyawan(auth, u)
                
            else:
                TerminalDesign.print_error("Pilihan tidak valid!")
                
            input(f"\n{TerminalDesign.YELLOW}❯ Tekan Enter untuk kembali...{TerminalDesign.ENDC}")
        elif pilih == "8":
            user.lihat_log_aktivitas(toko)
            input("\nKembali...")
        elif pilih == "0":
            user.logout()

def jalankan_menu_kasir(user, toko):
    """Menu khusus Kasir (Sales Focused)."""
    while user.is_login:
        TerminalDesign.clear_screen()
        TerminalDesign.print_header(f"PANEL KASIR: {user.nama_lengkap.upper()}")
        
        TerminalDesign.menu_item("1", "Input Transaksi Baru")
        TerminalDesign.menu_item("2", "Dashboard / Cek Stok")
        TerminalDesign.menu_item("3", "Cari Produk Cepat")
        TerminalDesign.menu_item("4", "Riwayat Penjualan Saya")
        TerminalDesign.menu_item("0", "LOGOUT")

        pilih = input(f"\n{TerminalDesign.YELLOW}❯ Opsi Kasir: {TerminalDesign.ENDC}")

        if pilih == "1":
            alur_transaksi_kasir(toko, user)
        elif pilih == "2":
            user.dashboard(toko)
            input("\nKembali...")
        elif pilih == "3":
            user.lihat_barang(toko)
            input("\nKembali...")
        elif pilih == "4":
            user.laporan_harian_saya(toko)
            input("\nKembali...")
        elif pilih == "0":
            user.logout()

def jalankan_menu_gudang(user, toko):
    """Menu khusus Staff Stok (Inventory Focused)."""
    while user.is_login:
        TerminalDesign.clear_screen()
        TerminalDesign.print_header(f"PANEL GUDANG: {user.nama_lengkap.upper()}")
        
        TerminalDesign.menu_item("1", "Dashboard Stok")
        TerminalDesign.menu_item("2", "Input Barang Baru")
        TerminalDesign.menu_item("3", "Update Stok (Opname/Restock)")
        TerminalDesign.menu_item("4", "Update Harga Modal")
        TerminalDesign.menu_item("5", "Audit Log Stok")
        TerminalDesign.menu_item("0", "LOGOUT")

        pilih = input(f"\n{TerminalDesign.YELLOW}❯ Opsi Gudang: {TerminalDesign.ENDC}")

        if pilih == "1":
            user.dashboard(toko)
            input("\nKembali...")
        elif pilih == "2":
            brg = formulir_input_barang(toko)
            if brg: user.tambah_barang(toko, brg)
            input("\nSelesai...")
        elif pilih == "3":
            nama = input("Nama barang: ")
            try:
                qty = int(input("Jumlah (+/-): "))
                user.update_stok(toko, nama, qty)
            except: TerminalDesign.print_error("Gagal!")
            input("\nKembali...")
        elif pilih == "4":
            nama = input("❯ Nama barang: ")
            try:
                hrg = int(input("❯ Harga modal baru: "))
                # Pastikan ada 'toko' di sini:
                user.input_harga_modal(toko, nama, hrg) 
            except ValueError:
                TerminalDesign.print_error("Harga harus angka!")
            input("\nKembali...")
        elif pilih == "5":
            user.lihat_log(toko)
            input("\nKembali...")
        elif pilih == "0":
            user.logout()

# ==============================================================================
# MAIN SYSTEM: CORE LOOP
# ==============================================================================

def main():
    """Fungsi utama untuk menjalankan sistem DigiMart Pro."""
    
    # 1. Inisialisasi Objek Core
    auth_sys = AuthSystem()
    toko_obj = Toko("DigiMart Pro Utama")

    # 2. Splash Screen Pembuka
    jalankan_splash_screen()

    while True:
        TerminalDesign.clear_screen()
        TerminalDesign.print_header("SISTEM MANAJEMEN DIGIMART PRO V2.0")
        
        # Menu Sebelum Login
        TerminalDesign.menu_item("1", "LOGIN KE SISTEM")
        TerminalDesign.menu_item("2", "TENTANG APLIKASI")
        TerminalDesign.menu_item("0", "MATIKAN SISTEM")
        
        pilihan_awal = input(f"\n{TerminalDesign.YELLOW}❯ Pilih Menu: {TerminalDesign.ENDC}")

        if pilihan_awal == "1":
            # Proses Login
            user_login = navigasi_login(auth_sys)
            
            if user_login:
                # Navigasi berdasarkan ROLE (RBAC)
                if user_login.role == "manager":
                    jalankan_menu_manager(user_login, toko_obj, auth_sys)
                elif user_login.role == "kasir":
                    jalankan_menu_kasir(user_login, toko_obj)
                elif user_login.role == "staff_stok":
                    jalankan_menu_gudang(user_login, toko_obj)
            
        elif pilihan_awal == "2":
            tampilkan_tentang_aplikasi()
            
        elif pilihan_awal == "0":
            TerminalDesign.clear_screen()
            TerminalDesign.print_header("MEMATIKAN SISTEM")
            TerminalDesign.loading_bar(1.2, "Mengamankan Database JSON")
            TerminalDesign.print_animated_text("Sistem berhasil dimatikan secara aman. Sampai jumpa!", 0.03)
            TerminalDesign.print_footer()
            sys.exit()
            
        else:
            TerminalDesign.print_error("Pilihan menu tidak valid!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Penanganan jika user menekan Ctrl+C
        print(f"\n{TerminalDesign.RED}Aplikasi ditutup paksa. Data terakhir disimpan.{TerminalDesign.ENDC}")
        sys.exit()
        