import tkinter as tk
from tkinter import ttk, messagebox
from db import connect
import re

class AnggotaApp:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title("Manajemen Anggota")
        self.root.geometry("850x550")

        # --- SKEMA WARNA NUANSA PERPUSTAKAAN (COKLAT TUA) ---
        BG_COLOR = "#4E342E"      # Coklat Tua (Latar Belakang Utama)
        FRAME_COLOR = "#5D4037"   # Coklat Sedang (Latar Belakang Input/Elemen)
        BUTTON_PRIMARY = "#FFC107" # Emas/Amber (Aksen Terang Tombol Utama)
        BUTTON_DANGER = "#DC3545"  # Merah (Tombol Hapus)
        TEXT_COLOR = "#EDE7F6"    # Krem/Putih Pucat (Teks)
        
        self.root.configure(bg=BG_COLOR)
        
        # --- Style untuk Treeview (Tabel) ---
        style = ttk.Style()
        # Menggunakan tema 'default' atau 'clam' sebagai dasar lebih baik untuk kustomisasi warna
        style.theme_use("default") 
        
        # Mengatur style untuk tampilan Treeview
        style.configure("Treeview", 
                        background=FRAME_COLOR, 
                        foreground=TEXT_COLOR, 
                        rowheight=25, 
                        fieldbackground=FRAME_COLOR, # Latar belakang gelap
                        font=("Arial", 9))
        
        # Warna Treeview saat dipilih (Aksen Emas)
        style.map('Treeview', 
                  background=[('selected', BUTTON_PRIMARY)],
                  foreground=[('selected', BG_COLOR)]) # Teks Coklat Tua saat terpilih
        
        # Mengatur style untuk Heading (judul kolom)
        style.configure("Treeview.Heading", 
                        font=("Arial", 10, "bold"), 
                        background=BG_COLOR, # Gunakan latar belakang gelap
                        foreground=BUTTON_PRIMARY, # Teks Emas sebagai aksen
                        relief=tk.FLAT)
        
        # --- Judul ---
        tk.Label(self.root, text="👥 Manajemen Anggota", font=("Arial", 14, "bold"), 
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        # --- Frame Form Input ---
        form_frame = tk.Frame(self.root, bg=BG_COLOR)
        form_frame.pack(pady=10)

        labels = ["Kode Anggota", "Nama", "Alamat", "Telepon", "Email"]
        self.entries = {}

        for i, label in enumerate(labels):
            # Label dengan teks cerah (Krem)
            tk.Label(form_frame, text=label, bg=BG_COLOR, fg=TEXT_COLOR).grid(row=i, column=0, padx=10, pady=5, sticky="e")

            if label == "Alamat":
                # Text input dengan background coklat sedang dan teks krem
                entry = tk.Text(form_frame, width=30, height=3, bg=FRAME_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)
            else:
                # Entry input dengan background coklat sedang dan teks krem
                entry = tk.Entry(form_frame, width=30, bg=FRAME_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)

            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry

        # --- Tombol Aksi ---
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=10)

        # Fungsi pembantu untuk tombol
        def create_button(parent, text, command, color):
            # Warna teks tombol utama (Emas) adalah Coklat Tua (BG_COLOR)
            fg_color = BG_COLOR if color == BUTTON_PRIMARY else TEXT_COLOR
            
            return tk.Button(parent, text=text, command=command, 
                             bg=color, fg=fg_color, 
                             activebackground=color, activeforeground=fg_color,
                             font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10, bd=0)
        
        # Tombol Tambah dan Edit (Emas/Amber)
        create_button(button_frame, "Tambah", self.tambah_anggota, BUTTON_PRIMARY).grid(row=0, column=0, padx=5)
        create_button(button_frame, "Edit", self.edit_anggota, BUTTON_PRIMARY).grid(row=0, column=1, padx=5)
        
        # Tombol Hapus (Merah)
        create_button(button_frame, "Hapus", self.hapus_anggota, BUTTON_DANGER).grid(row=0, column=2, padx=5)
        
        # Tombol Kembali (Emas/Amber)
        create_button(button_frame, "Kembali", self.kembali, BUTTON_PRIMARY).grid(row=0, column=3, padx=5)

        # --- Tabel Treeview ---
        columns = ("id", "kode", "nama", "alamat", "telepon", "email")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", width=0, stretch=tk.NO) 
        
        display_cols = ["kode", "nama", "alamat", "telepon", "email"]
        for col in display_cols:
             self.tree.heading(col, text=col.capitalize())
             self.tree.column(col, width=150)
             
        self.tree.pack(pady=10, fill="x", padx=20)

        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.load_data()
        self.root.mainloop()

    # --- Load Data ---
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT id, kode_anggota, nama, alamat, telepon, email FROM anggota") 
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    # --- Validasi Data (tetap sama) ---
    def validasi(self, kode, email, telepon):
        if not self.entries["Nama"].get().strip(): 
             messagebox.showerror("Error", "Nama tidak boleh kosong!")
             return False
        if not kode or not email or not telepon:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Format email tidak valid!")
            return False
        if not telepon.isdigit():
            messagebox.showerror("Error", "Telepon harus berupa angka!")
            return False
        return True

    # --- Tambah Anggota ---
    def tambah_anggota(self):
        kode = self.entries["Kode Anggota"].get().strip()
        nama = self.entries["Nama"].get().strip()
        alamat = self.entries["Alamat"].get("1.0", "end").strip()
        telepon = self.entries["Telepon"].get().strip()
        email = self.entries["Email"].get().strip()

        if not self.validasi(kode, email, telepon):
            return

        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("SELECT kode_anggota FROM anggota WHERE kode_anggota=%s", (kode,))
            if cur.fetchone():
                messagebox.showerror("Error", "Kode anggota sudah digunakan!")
                conn.close()
                return

            cur.execute("""
                INSERT INTO anggota (kode_anggota, nama, alamat, telepon, email)
                VALUES (%s, %s, %s, %s, %s)
            """, (kode, nama, alamat, telepon, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Anggota berhasil ditambahkan!")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah anggota: {e}")

    # --- Edit Anggota ---
    def edit_anggota(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih data yang ingin diedit!")
            return

        original_kode = self.tree.item(selected)['values'][1] 
        
        kode = self.entries["Kode Anggota"].get().strip()
        nama = self.entries["Nama"].get().strip()
        alamat = self.entries["Alamat"].get("1.0", "end").strip()
        telepon = self.entries["Telepon"].get().strip()
        email = self.entries["Email"].get().strip()

        if not self.validasi(kode, email, telepon):
            return
            
        if kode != original_kode:
            try:
                conn_check = connect()
                cur_check = conn_check.cursor()
                cur_check.execute("SELECT kode_anggota FROM anggota WHERE kode_anggota=%s", (kode,))
                if cur_check.fetchone():
                    messagebox.showerror("Error", "Kode anggota baru sudah digunakan oleh anggota lain!")
                    conn_check.close()
                    return
                conn_check.close()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal cek kode anggota: {e}")
                return

        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("""
                UPDATE anggota 
                SET kode_anggota=%s, nama=%s, alamat=%s, telepon=%s, email=%s 
                WHERE kode_anggota=%s
            """, (kode, nama, alamat, telepon, email, original_kode))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui anggota: {e}")

    # --- Hapus Anggota ---
    def hapus_anggota(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih data yang ingin dihapus!")
            return
        
        kode = self.tree.item(selected)['values'][1] 
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus anggota dengan kode {kode}?")
        if confirm:
            try:
                conn = connect()
                cur = conn.cursor()
                cur.execute("DELETE FROM anggota WHERE kode_anggota=%s", (kode,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
                self.load_data()
                self.clear_entries()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus anggota: {e}")


    # --- Saat Klik di Treeview ---
    def on_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        data = self.tree.item(selected)['values'] 
        
        # Bersihkan dan isi ulang form
        self.clear_entries()
        self.entries["Kode Anggota"].insert(0, data[1])
        self.entries["Nama"].insert(0, data[2])
        self.entries["Alamat"].insert("1.0", data[3])
        self.entries["Telepon"].insert(0, data[4])
        self.entries["Email"].insert(0, data[5])
        
    # --- Fungsi Bersihkan Input ---
    def clear_entries(self):
        for label in self.entries:
            if label == "Alamat":
                self.entries[label].delete("1.0", "end")
            else:
                self.entries[label].delete(0, "end")


    # --- Kembali ke Dashboard ---
    def kembali(self):
        self.root.destroy()
        from dashboard import Dashboard
        Dashboard(self.user)