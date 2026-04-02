# 🛒 DigiMart: Smart Supermarket Management System

DigiMart Pro adalah aplikasi manajemen supermarket berbasis Python yang berjalan di terminal (CLI). Sistem ini dirancang untuk membantu pengelolaan operasional toko secara terstruktur, mulai dari manajemen barang, transaksi penjualan, hingga pengelolaan user.  

Aplikasi ini dikembangkan menggunakan konsep **Object-Oriented Programming (OOP)** dengan penerapan prinsip seperti enkapsulasi, abstraksi, inheritance, polymorphism, modularitas, dan penggunaan mixins.

## 📌 Deskripsi Singkat
Aplikasi DigiMart Pro digunakan untuk:
- Mengelola data barang dan kategori produk
- Mengatur stok barang di gudang
- Melakukan transaksi penjualan
- Mencatat riwayat transaksi
- Mengelola akun pengguna berdasarkan role
- Menampilkan data secara terstruktur melalui terminal
Seluruh data disimpan dalam file **JSON** sehingga dapat digunakan kembali saat program dijalankan ulang.

## 👥 Role Pengguna
Sistem memiliki 3 jenis pengguna:
### 1. Manager
- Akses penuh ke seluruh sistem
- Mengelola user (tambah & hapus)
- Mengontrol data barang dan laporan

### 2. Kasir
- Melakukan transaksi penjualan
- Menghitung total belanja dan pembayaran
- Melihat stok barang

### 3. Staff Stok
- Mengelola data barang di gudang
- Update stok barang
- Mengubah harga modal
- Monitoring stok kritis

## ⚙️ Fitur Utama
- 🔐 Login sistem berbasis role
- 👤 Manajemen user (register & hapus user)
- 📦 Manajemen barang (tambah, update, detail)
- 📊 Pengelolaan stok barang
- 🛒 Transaksi penjualan
- 💰 Perhitungan total dan kembalian otomatis
- 🧾 Cetak struk transaksi
- 🔎 Pencarian barang cepat
- ⚠️ Monitoring stok kritis
- 📁 Penyimpanan data menggunakan JSON
- 🎨 Tampilan terminal interaktif (warna & animasi)

## 🧠 Konsep OOP yang Digunakan
### 🔹 Enkapsulasi
- Atribut private seperti `__nama`, `__stok`
- Akses data melalui method (getter & setter)

### 🔹 Abstraksi (Abstract Class)
- Class `Barang` sebagai abstract class
- Method `get_spesifikasi()` dan `hitung_total()` wajib diimplementasikan

### 🔹 Inheritance
- Class `User` diturunkan menjadi:
  - `Manager`
  - `Kasir`
  - `StaffStok`

### 🔹 Polymorphism
- Method seperti `hitung_total()` dan `get_akses_menu()` memiliki implementasi berbeda di setiap subclass

### 🔹 Modularitas
- Sistem dibagi ke beberapa file (auth, barang, transaksi, dll)

### 🔹 Mixins
- `TimestampMixin` → mencatat waktu pembuatan data

## 🗂️ Struktur Project
├── auth.py
├── database.py
├── barang.py
├── kasir.py
├── gudang.py
├── detail_transaksi.py
├── factory.py
├── design_output.py
├── transaksi.py
├── user.py
├── manager.py
├── kategori.py
├── timestamp_mixin.py
├── database/
│ ├── user.json
│ ├── barang.json
│ └── transaksi.json
├── main.py

## 💡 Teknologi yang Digunakan
### Python 3
### JSON (sebagai database sederhana)
### CLI (Command Line Interface)

## 👨‍💻 Tim Pengembang
### 1. Dian Fajar
### 2. Fatimah Azzahra
### 3. Ghenia Fadiya Zahra
### 4. R. Daffa