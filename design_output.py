import os
import time
import sys

class TerminalDesign:
    """
    Sistem UI/UX DigiMart Pro v2.0. 🏛️
    Pusat kendali estetika untuk seluruh 33 modul sistem.
    Menangani pewarnaan ANSI, kalkulasi spasi tabel, dan animasi loading.
    """
    
    # --- ANSI Escape Codes untuk Warna Terang ---
    HEADER    = '\033[95m'  # Ungu (Judul Utama)
    BLUE      = '\033[94m'  # Biru (Informasi/Header)
    CYAN      = '\033[96m'  # Cyan (Bingkai Tabel)
    GREEN     = '\033[92m'  # Hijau (Sukses/Angka Positif)
    YELLOW    = '\033[93m'  # Kuning (Peringatan/Input)
    RED       = '\033[91m'  # Merah (Error/Stok Kritis)
    BOLD      = '\033[1m'   # Teks Tebal
    UNDERLINE = '\033[4m'   # Garis Bawah
    ENDC      = '\033[0m'   # Reset Warna

    @staticmethod
    def clear_screen():
        """Membersihkan terminal agar interface tetap rapi."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_ascii_art():
        """Menampilkan logo DigiMart Pro dengan gaya elegan."""
        logo = f"""
{TerminalDesign.CYAN}{TerminalDesign.BOLD}
    ██████╗ ██╗ ██████╗ ██╗███╗   ███╗ █████╗ ██████╗ ████████╗
    ██╔══██╗██║██╔════╝ ██║████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
    ██║  ██║██║██║  ███╗██║██╔████╔██║███████║██████╔╝   ██║   
    ██║  ██║██║██║   ██║██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
    ██████╔╝██║╚██████╔╝██║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
    ╚═════╝ ╚═╝ ╚═════╝ ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
              Digital Supermarket Management System
{TerminalDesign.ENDC}"""
        print(logo)

    @staticmethod
    def print_header(title, width=82):
        """Membuat pembatas antar menu dengan garis biru presisi."""
        print(f"\n{TerminalDesign.BLUE}{'='*width}{TerminalDesign.ENDC}")
        print(f"{TerminalDesign.BOLD}{title.upper().center(width)}{TerminalDesign.ENDC}")
        print(f"{TerminalDesign.BLUE}{'='*width}{TerminalDesign.ENDC}")

    @staticmethod
    def print_sub_header(text, width=82):
        """Menampilkan sub-judul dengan dekorasi garis tipis."""
        print(f"{TerminalDesign.CYAN}{'-'*width}{TerminalDesign.ENDC}")
        print(f"{TerminalDesign.BOLD}{text.center(width)}{TerminalDesign.ENDC}")
        print(f"{TerminalDesign.CYAN}{'-'*width}{TerminalDesign.ENDC}")

    @staticmethod
    def print_info_box(info_dict, width=82):
        """
        Mencetak kotak informasi dengan Bingkai FULL CYAN. 💎
        Sangat presisi untuk menampilkan data dari 33 file sistem
        tanpa merusak garis pembatas kanan akibat kode warna.
        """
        # Garis Atas (Warna Cyan)
        print(f"{TerminalDesign.CYAN}┌" + "─" * (width - 2) + "┐" + f"{TerminalDesign.ENDC}")
        
        for key, value in info_dict.items():
            k = str(key).upper()
            v = str(value)
            
            # Label tetap 15 karakter untuk konsistensi vertikal
            label_text = f"{k:<15} : "
            
            # Hitung padding manual: total lebar - border - label - value
            padding_needed = width - 4 - len(label_text) - len(v)
            sisa_spasi = " " * max(0, padding_needed)
            
            # Rakit baris: Gabungan BOLD (Label) dan CYAN (Bingkai & Isi)
            line = (f"│ {TerminalDesign.BOLD}{label_text}{TerminalDesign.ENDC}"
                    f"{TerminalDesign.CYAN}{v}{sisa_spasi} │")
            
            print(f"{TerminalDesign.CYAN}{line}{TerminalDesign.ENDC}")
            
        # Garis Bawah (Warna Cyan)
        print(f"{TerminalDesign.CYAN}└" + "─" * (width - 2) + "┘" + f"{TerminalDesign.ENDC}")

    @staticmethod
    def loading_bar(duration=1.5, message="Sinkronisasi Database", width=35):
        """Animasi loading bar untuk simulasi pembacaan file JSON."""
        print(f"{TerminalDesign.CYAN}{TerminalDesign.BOLD}ℹ️  {message}{TerminalDesign.ENDC}")
        for i in range(width + 1):
            percent = int((i / width) * 100)
            bar = "█" * i + "░" * (width - i)
            
            # \r untuk menimpa baris yang sama agar animasi bergerak
            sys.stdout.write(f"\r{TerminalDesign.BLUE}[{bar}] {TerminalDesign.YELLOW}{percent}%")
            sys.stdout.flush()
            time.sleep(duration / width)
        print(f"\n{TerminalDesign.GREEN}[✔] Berhasil Disinkronkan!{TerminalDesign.ENDC}\n")

    @staticmethod
    def print_animated_text(text, delay=0.03):
        """Memberikan efek mengetik pada teks (Typewriter Effect)."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def input_styled(prompt):
        """Input field dengan indikator panah kuning agar user tidak bingung."""
        return input(f"{TerminalDesign.YELLOW}{TerminalDesign.BOLD} ❯❯ {prompt}: {TerminalDesign.ENDC}")

    @staticmethod
    def print_success(message):
        """Notifikasi sukses dengan warna hijau cerah."""
        print(f"{TerminalDesign.GREEN}✅ SUCCESS: {message}{TerminalDesign.ENDC}")
        time.sleep(0.8)

    @staticmethod
    def print_error(message):
        """Notifikasi error dengan warna merah dan delay agar terbaca."""
        print(f"\n{TerminalDesign.RED}❌ ERROR: {message}{TerminalDesign.ENDC}")
        time.sleep(1.5)

    @staticmethod
    def print_warning(message):
        """Notifikasi peringatan untuk stok kritis atau konfirmasi hapus."""
        print(f"{TerminalDesign.YELLOW}⚠️  WARNING: {message}{TerminalDesign.ENDC}")

    @staticmethod
    def menu_item(no, text):
        """Format standar untuk list menu agar sejajar secara vertikal."""
        print(f"  {TerminalDesign.CYAN}{TerminalDesign.BOLD}[{no}]{TerminalDesign.ENDC} {text}")

    @staticmethod
    def print_footer(width=82):
        """Menampilkan garis penutup di bagian bawah layar."""
        print(f"{TerminalDesign.BLUE}{'='*width}{TerminalDesign.ENDC}")
        date_now = time.strftime("%Y-%m-%d | %H:%M:%S")
        print(f"{TerminalDesign.BOLD}{'DigiMart Pro v2.0 - Team 4'.center(width)}{TerminalDesign.ENDC}")
        print(f"{date_now.center(width)}")
        print(f"{TerminalDesign.BLUE}{'='*width}{TerminalDesign.ENDC}\n")