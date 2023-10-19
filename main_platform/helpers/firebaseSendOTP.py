import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("credkey.json")
firebase_admin.initialize_app(cred)

phone_number = input("Masukkan nomor telepon: ")

# Membuat konfigurasi Recaptcha (jika digunakan)
# Tambahkan konfigurasi Recaptcha di sini

auth_instance = auth.initialize_app(cred)

# Memulai proses otentikasi nomor telepon
verification = auth.create_phone_verification(phone_number, app=auth_instance)

# SMS dikirim. Mintalah pengguna untuk memasukkan kode dari pesan, lalu otentikasi
# pengguna dengan hasil konfirmasi.
confirmation_result = auth.confirm_phone_verification(verification['session_info'], input("Masukkan kode verifikasi: "))

# Berhasil otentikasi
print("Otentikasi berhasil: ", confirmation_result.user.uid)

# Tangani kesalahan jika SMS tidak dapat dikirimkan atau ada masalah lain
# Dalam kasus kesalahan, Anda dapat menambahkan logika untuk menangani kesalahan tersebut.
