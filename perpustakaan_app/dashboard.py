import tkinter as tk
from tkinter import messagebox
from db import connect
# Pastikan Anda sudah memperbaiki manajemen_buku.py agar mengimpor BukuPage, bukan BukuApp
from manajemen_buku import BukuPage
from manajemen_anggota import AnggotaApp

class Dashboard:
    def __init__(self, user):
        self.root = tk.Tk()
        self.root.title("Dashboard - Sistem Manajemen Perpustakaan")
        self.root.geometry("500x400")
        self.user = user

        # --- Skema Warna Nuansa Perpustakaan (Coklat Tua) ---
        BG_COLOR = "#4E342E"      # Coklat Tua (Latar Belakang Utama)
        BUTTON_COLOR = "#FFC107"  # Emas/Amber (Aksen Terang Tombol Utama)
        LOGOUT_COLOR = "#DC3545"  # Merah (Tombol Logout/Peringatan)
        TEXT_COLOR = "#EDE7F6"    # Krem/Putih Pucat (Teks)
        
        self.root.configure(bg=BG_COLOR)
        
        # Frame Header
        header_frame = tk.Frame(self.root, bg=BG_COLOR)
        header_frame.pack(pady=15)

        # Label Selamat Datang (Teks Krem/Putih Pucat)
        tk.Label(header_frame, text=f"Selamat Datang, {user['username']}", 
                 font=("Arial", 14, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack()
        
        # Frame untuk Tombol
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=10)

        # Fungsi pembantu untuk membuat tombol yang konsisten
        def create_button(text, command, color):
            # Teks tombol utama berwarna coklat tua (BG_COLOR) agar kontras dengan latar tombol emas
            fg_color = BG_COLOR if color == BUTTON_COLOR else TEXT_COLOR
            
            return tk.Button(button_frame, text=text, width=25, command=command,
                             bg=color, fg=fg_color, 
                             activebackground=color, 
                             # Active foreground disesuaikan untuk kontras saat hover
                             activeforeground=fg_color, 
                             font=("Arial", 10, "bold"), 
                             relief=tk.FLAT, bd=0)
            
        # Tombol Manajemen Buku (Emas/Amber)
        create_button("📚 Manajemen Buku", self.open_buku, BUTTON_COLOR).pack(pady=5)
        # Tombol Manajemen Anggota (Emas/Amber)
        create_button("👥 Manajemen Anggota", self.open_anggota, BUTTON_COLOR).pack(pady=5)
        # Tombol Logout (Merah)
        create_button("🚪 Logout", self.logout, LOGOUT_COLOR).pack(pady=15)

        # Label Statistik (Teks Krem/Putih Pucat)
        self.stats_label = tk.Label(self.root, font=("Arial", 10), bg=BG_COLOR, fg=TEXT_COLOR)
        self.stats_label.pack(pady=10)
        self.show_stats()
        
        self.root.mainloop()

    def show_stats(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM buku")
        total_buku = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM anggota")
        total_anggota = cur.fetchone()[0]
        conn.close()

        self.stats_label.config(text=f"Jumlah Buku: {total_buku} | Jumlah Anggota: {total_anggota}")

    def open_buku(self):
        buku_window = tk.Toplevel(self.root) 
        buku_window.title("Manajemen Buku")
        # Set background Toplevel agar konsisten dengan tema dark/coklat
        buku_window.configure(bg="#1E1E1E") 
        # Catatan: BukuPage menggunakan ttk.Frame, style-nya harus diatur di manajemen_buku.py
        buku_app = BukuPage(buku_window, self) 
        buku_app.pack(expand=True, fill='both') 
        # Coba muat data buku
        try:
            buku_app.load_buku() 
        except Exception as e:
            messagebox.showwarning("Error", f"Gagal memuat data buku saat membuka jendela: {e}")
            
        buku_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_buku(buku_window))

    def on_close_buku(self, window):
        window.destroy()
        self.show_stats() 

    def open_anggota(self):
        self.root.destroy()
        AnggotaApp(self.user)

    def logout(self):
        self.root.destroy()
        try:
            import login
            login.LoginApp(tk.Tk())
        except ImportError:
            messagebox.showerror("Error", "Modul login tidak ditemukan. Tidak dapat Logout.")