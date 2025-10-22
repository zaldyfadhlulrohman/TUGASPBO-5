📚 Aplikasi Sistem Manajemen Perpustakaan

Aplikasi ini dibuat menggunakan Python (Tkinter) dan MySQL untuk memenuhi tugas materi 5 tentang GUI dan database.
Aplikasi berfungsi untuk mengelola data buku, anggota, serta login pengguna dengan sistem validasi dan koneksi database langsung.

🧠 Deskripsi Singkat

Aplikasi ini memanfaatkan database perpustakaan_db yang memiliki tiga tabel utama yaitu users, buku, dan anggota.
Seluruh fitur login, dashboard, manajemen buku, dan manajemen anggota terhubung langsung dengan database ini menggunakan library mysql.connector.

⚙️ Fitur Utama
1. Sistem Login

Sistem login dibuat menggunakan tabel users sebagai dasar autentikasi.
Pengguna memasukkan username dan password, kemudian program mencocokkannya dengan data yang tersimpan di database menggunakan query pencarian.
Jika data cocok, maka login berhasil dan pengguna diarahkan ke halaman dashboard.
Sebelum proses login dijalankan, program memeriksa apakah kolom username atau password kosong.
Jika kosong, muncul peringatan agar pengguna mengisi data terlebih dahulu.
Informasi pengguna yang berhasil login disimpan ke dalam variabel session bernama current_user, yang digunakan untuk menampilkan nama pengguna di dashboard.
Selain itu, sistem login juga dilengkapi penanganan error menggunakan blok try dan except agar program tidak berhenti saat koneksi database gagal.

Kesimpulan:
Sistem login berfungsi untuk memverifikasi data pengguna dari tabel users, memastikan hanya akun yang terdaftar yang dapat mengakses aplikasi.

2. Dashboard

Setelah login berhasil, pengguna diarahkan ke halaman dashboard.
Dashboard menampilkan teks sambutan dengan nama pengguna aktif yang diambil dari variabel current_user.
Selain itu, halaman ini juga menampilkan jumlah buku dan jumlah anggota yang datanya diambil dari database menggunakan perintah COUNT.
Informasi tersebut diperbarui secara otomatis setiap kali pengguna membuka dashboard.
Terdapat juga tombol navigasi untuk menuju ke halaman Manajemen Buku, Manajemen Anggota, dan Logout.

Kesimpulan:
Dashboard berfungsi sebagai pusat kontrol dan informasi utama.
Data yang tampil berasal langsung dari tabel buku dan anggota, sehingga pengguna bisa memantau data perpustakaan secara real-time.

3. Manajemen Buku

Bagian ini digunakan untuk mengelola data koleksi buku pada tabel buku.
Fitur yang disediakan meliputi tambah, ubah, hapus, dan cari data (CRUD).
Admin dapat menambahkan data buku dengan field seperti kode buku, judul, pengarang, penerbit, tahun terbit, dan stok.
Sebelum disimpan, sistem memeriksa apakah kode buku sudah digunakan sebelumnya, apakah tahun terbit berupa angka, dan apakah stok bernilai positif.
Jika ada kesalahan input, muncul peringatan menggunakan messagebox.
Semua data buku ditampilkan di tampilan tabel menggunakan komponen Treeview, sehingga mudah dibaca dan dikelola.
Fitur pencarian juga tersedia untuk memudahkan pengguna menemukan data berdasarkan judul atau pengarang.

Kesimpulan:
Manajemen Buku membantu admin mengatur seluruh data koleksi buku di database buku dengan validasi lengkap dan tampilan yang mudah digunakan.

4. Manajemen Anggota

Bagian ini digunakan untuk mengelola data anggota perpustakaan.
Data yang dikelola meliputi kode anggota, nama, alamat, telepon, dan email.
Program menyediakan fitur CRUD yang sama seperti pada manajemen buku.
Sebelum data disimpan, sistem memeriksa apakah kode anggota sudah ada sebelumnya, nomor telepon hanya berupa angka, dan format email benar.
Validasi dilakukan dengan fungsi logika dan pola regex agar data sesuai dengan tipe yang diharapkan.
Setelah tersimpan, data anggota langsung ditampilkan pada tabel Treeview.

Kesimpulan:
Manajemen Anggota digunakan untuk mencatat dan memperbarui data anggota di tabel anggota, memastikan semua data valid dan terhindar dari duplikasi.

💾 Koneksi Database

Aplikasi menggunakan MySQL Connector untuk menghubungkan Python dengan MySQL.
Database bernama perpustakaan_db memiliki tiga tabel utama:

users → menyimpan data login pengguna

buku → menyimpan data koleksi buku

anggota → menyimpan data anggota perpustakaan

Semua query menggunakan parameterisasi agar aman dari serangan SQL Injection.

🚀 Cara Menjalankan Aplikasi

Import database dari file database_setup.sql ke dalam MySQL (melalui phpMyAdmin atau terminal).

Install library MySQL Connector dengan perintah:
pip install mysql-connector-python
Jalankan program utama dengan:

python perpustakaan_app.py


Gunakan akun login default:

Username: zaldy
Password: zaldy123
🗃️ Struktur Proyek

PerpustakaanApp
│
├── perpustakaan_app.py (Program utama GUI)
├── database_setup.sql (Struktur database MySQL)
└── README.md (Dokumentasi aplikasi)

🧩 Kesimpulan Akhir

Seluruh bagian aplikasi (login, dashboard, buku, anggota) bekerja sesuai dengan struktur database perpustakaan_db.
Setiap proses CRUD terhubung langsung ke tabel masing-masing dan memiliki validasi untuk menjaga kebenaran data.
Aplikasi ini menggabungkan antarmuka visual yang sederhana dengan logika database yang kuat, sehingga cocok untuk sistem perpustakaan berskala kecil hingga menengah.

👨‍💻 Pengembang

Nama: Zaldy
Peran: Pengembang Aplikasi Perpustakaan

📜 Lisensi

Aplikasi ini dibuat untuk keperluan akademik dan pembelajaran.
Diperbolehkan untuk digunakan ulang selama menyertakan kredit pengembang.
