import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
from db import connect 
from manajemen_anggota import AnggotaApp 

# Asumsi impor yang dibutuhkan yang hilang (untuk run_query)
try:
    from mysql.connector import Error 
    def get_db_connection(): 
        return connect()
except: 
    class Error(Exception): pass 
    def get_db_connection(): return connect() 

# BARIS from manajemen_buku import BukuApp TELAH DIHAPUS

class BukuPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # ===================================================
        # START: CUSTOM STYLE (TEMA PERPUSTAKAAN COKLAT/EMAS)
        # ===================================================
        style = ttk.Style(parent)
        
        # Menggunakan tema 'clam' sebagai dasar untuk kustomisasi yang lebih baik
        style.theme_use('clam')
        
        # Warna Nuansa Perpustakaan
        BG_COLOR = "#4E342E"      # Coklat Tua (Latar Belakang Utama)
        FRAME_COLOR = "#5D4037"   # Coklat Sedang (Latar Belakang Input/Elemen)
        BUTTON_PRIMARY = "#FFC107" # Emas/Amber (Aksen Terang Tombol Utama)
        TEXT_COLOR = "#EDE7F6"    # Krem/Putih Pucat (Teks)
        
        # 1. Mengatur Latar Belakang Global
        style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure('TFrame', background=BG_COLOR, borderwidth=0)
        style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR)
        
        # 2. Styling Input (Entry)
        style.configure('TEntry', 
                        fieldbackground=FRAME_COLOR, 
                        foreground=TEXT_COLOR,
                        insertbackground=TEXT_COLOR) # Warna kursor
        
        # 3. Styling Tombol Primer (Tambah)
        style.configure('Primary.TButton', 
                        background=BUTTON_PRIMARY,  
                        foreground=BG_COLOR, # Teks Coklat Tua di tombol Emas
                        font=('Arial', 10, 'bold'),
                        borderwidth=0)
        style.map('Primary.TButton', 
                  background=[('active', '#FFD54F')], # Hover: Amber lebih muda
                  foreground=[('active', BG_COLOR)])
                  
        # Tombol Sekunder (Update, Hapus, Cari)
        style.configure('TButton',
                        background=FRAME_COLOR, # Coklat Sedang
                        foreground=TEXT_COLOR, # Teks Krem
                        borderwidth=0)
        style.map('TButton', 
                  background=[('active', '#6D4C41')]) # Hover: Coklat Sedang lebih gelap
        
        # 4. Styling Treeview (Tabel)
        style.configure('Treeview', 
                        background=FRAME_COLOR, 
                        foreground=TEXT_COLOR, 
                        fieldbackground=FRAME_COLOR, 
                        rowheight=25)
        style.configure('Treeview.Heading', 
                        background=BG_COLOR, 
                        foreground=BUTTON_PRIMARY, # Heading Treeview dengan aksen Emas
                        font=('Arial', 10, 'bold'))
        # Selected: Latar Emas, Teks Coklat Tua
        style.map('Treeview', 
                  background=[('selected', BUTTON_PRIMARY)], 
                  foreground=[('selected', BG_COLOR)]) 
        
        # Agar latar belakang frame BukuPage juga gelap
        self.configure(style='TFrame') 
        
        # ===================================================
        # END: CUSTOM STYLE
        # ===================================================

        # layout left form / right treeview
        left = ttk.Frame(self, padding=12); 
        left.grid(row=0, column=0, sticky='nsw', padx=(0,12), pady=6)
        
        labels = ['Kode Buku:', 'Judul:', 'Pengarang:', 'Penerbit:', 'Tahun Terbit:', 'Stok:']
        self.entries = {}
        for i, lbl in enumerate(labels):
            # Label akan otomatis berwarna krem
            ttk.Label(left, text=lbl).grid(row=i+1, column=0, sticky='e', padx=6, pady=4)
            ent = ttk.Entry(left, width=30); 
            ent.grid(row=i+1, column=1, sticky='w', padx=6, pady=4)
            self.entries[lbl] = ent
        
        # buttons
        # Tombol Tambah menggunakan style 'Primary.TButton' (Emas)
        ttk.Button(left, text='Tambah', command=self.add_buku, style='Primary.TButton').grid(row=8, column=0, pady=10)
        # Tombol lain menggunakan style default 'TButton' (Coklat Sedang)
        ttk.Button(left, text='Update', command=self.update_buku).grid(row=8, column=1, pady=10)
        ttk.Button(left, text='Hapus', command=self.delete_buku).grid(row=8, column=2, pady=10)
        
        # right: search + treeview
        right = ttk.Frame(self, padding=8); 
        right.grid(row=0, column=1, sticky='nsew')
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        search_frame = ttk.Frame(right);
        search_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 10))
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).grid(row=0, column=0, sticky='ew')
        ttk.Button(search_frame, text='Cari', command=self.search_buku).grid(row=0, column=1, padx=(6,0))
        
        cols = ('kode_buku','judul','pengarang','penerbit','tahun_terbit','stok')
        self.tree = ttk.Treeview(right, columns=cols, show='headings')
        for c in cols: 
            self.tree.heading(c, text=c.replace('_',' ').title())
            self.tree.column(c, width=120, anchor=tk.CENTER)
            
        self.tree.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        vsb = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=2, sticky='ns')
        self.tree.configure(yscrollcommand=vsb.set)
        
    # --- FUNGSI run_query dan lainnya (TIDAK BERUBAH) ---
    def run_query(self, sql, params=None, expect_rows=False):
        conn = get_db_connection(); 
        if not conn: return None
        try:
            cur = conn.cursor(); cur.execute(sql, params or ())
            if expect_rows or sql.strip().upper().startswith('SELECT'):
                rows = cur.fetchall(); cur.close(); conn.close(); return rows
            conn.commit(); affected = cur.rowcount; cur.close(); conn.close(); return affected
        except Error as e:
            messagebox.showerror('Database Error', f'Query gagal:\n{e}'); return None

    def validate(self):
        kode = self.entries['Kode Buku:'].get().strip(); judul = self.entries['Judul:'].get().strip()
        pengarang = self.entries['Pengarang:'].get().strip(); penerbit = self.entries['Penerbit:'].get().strip()
        tahun = self.entries['Tahun Terbit:'].get().strip(); stok = self.entries['Stok:'].get().strip()
        if not (kode and judul and pengarang and penerbit and tahun and stok):
            messagebox.showwarning('Validasi', 'Semua field harus diisi.'); return None
        if not tahun.isdigit(): messagebox.showwarning('Validasi', 'Tahun terbit harus angka.'); return None
        if not stok.isdigit() or int(stok) < 0: messagebox.showwarning('Validasi', 'Stok harus angka positif.'); return None
        return {'kode': kode, 'judul': judul, 'pengarang': pengarang, 'penerbit': penerbit, 'tahun': int(tahun), 'stok': int(stok)}

    def add_buku(self):
        data = self.validate(); 
        if not data: return
        rows = self.run_query('SELECT id FROM buku WHERE kode_buku=%s', (data['kode'],), expect_rows=True)
        if rows is None: return
        if rows: messagebox.showwarning('Validasi', 'Kode buku sudah ada.'); return
        sql = 'INSERT INTO buku (kode_buku, judul, pengarang, penerbit, tahun_terbit, stok) VALUES (%s,%s,%s,%s,%s,%s)'
        self.run_query(sql, (data['kode'], data['judul'], data['pengarang'], data['penerbit'], data['tahun'], data['stok']))
        messagebox.showinfo('Sukses', 'Buku berhasil ditambahkan.'); self.load_buku(); self.clear_form()

    def load_buku(self):
        rows = self.run_query('SELECT kode_buku, judul, pengarang, penerbit, tahun_terbit, stok FROM buku ORDER BY created_at DESC', expect_rows=True)
        if rows is None: return
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in rows: self.tree.insert('', 'end', values=r)

    def search_buku(self):
        q = self.search_var.get().strip(); 
        if not q: self.load_buku(); return
        like = f"%{q}%"
        rows = self.run_query('SELECT kode_buku, judul, pengarang, penerbit, tahun_terbit, stok FROM buku WHERE judul LIKE %s OR pengarang LIKE %s', (like, like), expect_rows=True)
        if rows is None: return
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in rows: self.tree.insert('', 'end', values=r)

    def on_select(self, event):
        sel = self.tree.selection(); 
        if not sel: return
        vals = self.tree.item(sel[0], 'values')
        keys = ['Kode Buku:', 'Judul:', 'Pengarang:', 'Penerbit:', 'Tahun Terbit:', 'Stok:']
        for k, v in zip(keys, vals):
            self.entries[k].delete(0, 'end'); self.entries[k].insert(0, v)

    def update_buku(self):
        data = self.validate(); 
        if not data: return
        sql = 'UPDATE buku SET judul=%s, pengarang=%s, penerbit=%s, tahun_terbit=%s, stok=%s WHERE kode_buku=%s'
        self.run_query(sql, (data['judul'], data['pengarang'], data['penerbit'], data['tahun'], data['stok'], data['kode']))
        messagebox.showinfo('Sukses', 'Data buku berhasil diupdate.'); self.load_buku(); self.clear_form()

    def delete_buku(self):
        kode = self.entries['Kode Buku:'].get().strip()
        if not kode: messagebox.showwarning('Validasi', 'Pilih buku yang akan dihapus.'); return
        if not messagebox.askyesno('Konfirmasi', f'Yakin hapus buku dengan kode {kode}?'): return
        self.run_query('DELETE FROM buku WHERE kode_buku=%s', (kode,)); messagebox.showinfo('Sukses', 'Buku berhasil dihapus.'); self.load_buku(); self.clear_form()

    def clear_form(self):
        for e in self.entries.values(): e.delete(0, 'end')