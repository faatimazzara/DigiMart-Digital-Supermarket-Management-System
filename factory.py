from makanan import Makanan
from minuman import Minuman
from rumah_tangga import BarangRumahTangga
from produk_segar import ProdukSegar
from produk_elektronik import ProdukElektronik
from kesehatan_kecantikan import KesehatanKecantikan
from kategori import Kategori

def create_barang(data):
    """
    Fungsi Factory untuk menginstansiasi objek subclass Barang. 🏭
    Mengambil dictionary dari JSON dan mengembalikan objek Class yang sesuai.
    """
    try:
        if not data:
            return None

        tipe = data.get("type")
        # Membuat objek Kategori jika datanya tersedia
        kategori_obj = Kategori(data["kategori"]) if data.get("kategori") else None

        if tipe == "Makanan":
            return Makanan(
                data["nama"], 
                data["harga_modal"], 
                data["harga_jual"], 
                data["stok"], 
                data["tanggal_kadaluarsa"], 
                kategori_obj
            )

        elif tipe == "Minuman":
            return Minuman(
                data["nama"], 
                data["harga_modal"], 
                data["harga_jual"], 
                data["stok"], 
                data["volume"], 
                data["tanggal_kadaluarsa"], 
                kategori_obj
            )

        elif tipe == "BarangRumahTangga":
            return BarangRumahTangga(
                data["nama"], 
                data["harga_modal"], 
                data["harga_jual"], 
                data["stok"], 
                data.get("merk", "Tanpa Merk"), 
                kategori_obj
            )

        elif tipe == "ProdukSegar":
            # Menyesuaikan dengan parameter ProdukSegar (berat ditambahkan default 1 jika tidak ada)
            return ProdukSegar(
                data["nama"], 
                data["harga_modal"], 
                data["harga_jual"], 
                data["stok"], 
                data.get("berat", 1.0),
                data["tanggal_kedatangan"], 
                data["tanggal_kadaluarsa"], 
                kategori_obj
            )

        elif tipe == "ProdukElektronik":
            return ProdukElektronik(
                data["nama"], 
                data["harga_modal"], 
                data["harga_jual"], 
                data["stok"], 
                data["garansi"], 
                data["merk"], 
                kategori_obj
            )

        elif tipe == "KesehatanKecantikan":
            return KesehatanKecantikan(
                data["nama"], 
                data["harga_modal"], 
                data["harga_jual"], 
                data["stok"], 
                data["merk"],
                data["tanggal_kadaluarsa"], 
                kategori_obj
            )

        return None
        
    except KeyError as e:
        print(f"⚠️ Gagal membuat barang: Field {e} hilang dalam data.")
        return None
    except Exception as e:
        print(f"⚠️ Error pada Factory: {e}")
        return None