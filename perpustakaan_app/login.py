import tkinter as tk
from tkinter import messagebox
from db import connect
from dashboard import Dashboard 

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sistem Manajemen Perpustakaan")
        self.root.geometry("400x250")
        
        # --- Skema Warna Nuansa Perpustakaan (Coklat Tua) ---
        BG_COLOR = "#4E342E"      # Coklat Tua (Latar Belakang)
        FRAME_COLOR = "#5D4037"   # Coklat Sedang (Frame/Input Background)
        BUTTON_COLOR = "#FFC107"  # Emas/Amber (Aksen Terang Tombol)
        TEXT_COLOR = "#EDE7F6"    # Krem/Putih Pucat (Teks)
        
        self.root.configure(bg=BG_COLOR)

        # Frame utama untuk penataan
        main_frame = tk.Frame(root, bg=BG_COLOR) 
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Label Judul/Selamat Datang
        tk.Label(main_frame, text="Sistem Manajemen Perpustakaan", bg=BG_COLOR, fg=BUTTON_COLOR, font=("Georgia", 14, "bold")).pack(pady=(0, 15))


        # Label Username (Teks Krem)
        tk.Label(main_frame, text="Username", bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 10)).pack(pady=(0, 2))
        
        # Input field Username (Background Coklat Sedang, Teks Krem)
        self.username_entry = tk.Entry(main_frame, width=30, 
                                       bg=FRAME_COLOR, fg=TEXT_COLOR, 
                                       insertbackground=TEXT_COLOR, relief=tk.FLAT) 
        self.username_entry.pack()

        # Label Password (Teks Krem)
        tk.Label(main_frame, text="Password", bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 10)).pack(pady=(10, 2))
        
        # Input field Password (Background Coklat Sedang, Teks Krem)
        self.password_entry = tk.Entry(main_frame, show="*", width=30, 
                                       bg=FRAME_COLOR, fg=TEXT_COLOR, 
                                       insertbackground=TEXT_COLOR, relief=tk.FLAT) 
        self.password_entry.pack()

        # Tombol Login (Emas/Amber sebagai aksen terang)
        tk.Button(main_frame, text="Login", command=self.login, 
                  bg=BUTTON_COLOR, fg=BG_COLOR, # Warna tombol Emas, Teks Coklat Tua
                  activebackground="#FFD54F", activeforeground=BG_COLOR, # Efek hover
                  font=("Arial", 10, "bold"), width=15, relief=tk.FLAT, bd=0).pack(pady=20)

    def login(self):
        # Logika login (TIDAK BERUBAH)
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "Username dan password tidak boleh kosong!")
            return
        
        try:
            conn = connect()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cur.fetchone()

            if user:
                messagebox.showinfo("Sukses", f"Selamat datang, {user['username']}!")
                self.root.destroy()
                Dashboard(user) 
            else:
                messagebox.showerror("Gagal", "Username atau password salah!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal koneksi database: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()