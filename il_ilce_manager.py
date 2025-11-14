import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import ttkbootstrap as tb
from db_utils import (
    init_db_and_migrate, query_provinces, query_districts,
    add_province, rename_province, delete_province,
    add_district, rename_district, delete_district
)

class IlIlceManager:
    """
    Toplevel GUI to manage provinces and districts (add/rename/delete).
    Usage:
        IlIlceManager(root)
    """
    def __init__(self, parent):
        init_db_and_migrate()
        self.win = tb.Toplevel(parent)
        self.win.title("İl / İlçe Yönetimi")
        self.win.geometry("800x420")
        self.win.transient(parent)
        self.win.grab_set()

        left = ttk.Frame(self.win, padding=10); left.pack(side="left", fill="both", expand=True)
        right = ttk.Frame(self.win, padding=10); right.pack(side="right", fill="both", expand=True)

        tb.Label(left, text="İller", bootstyle="primary").pack(anchor="w")
        self.prov_search = tb.Entry(left, bootstyle="info"); self.prov_search.pack(fill="x", pady=(4,8))
        self.prov_search.bind("<KeyRelease>", lambda e: self.refresh_provinces())
        self.prov_list = tk.Listbox(left, height=18)
        self.prov_list.pack(fill="both", expand=True)
        self.prov_list.bind("<<ListboxSelect>>", lambda e: self.on_province_selected())

        p_btns = ttk.Frame(left); p_btns.pack(fill="x", pady=6)
        tb.Button(p_btns, text="Yeni İl", bootstyle="success", command=self.add_province).pack(side="left", padx=4)
        tb.Button(p_btns, text="İsim Değiştir", bootstyle="warning", command=self.rename_province).pack(side="left", padx=4)
        tb.Button(p_btns, text="Sil", bootstyle="danger", command=self.delete_province).pack(side="left", padx=4)

        tb.Label(right, text="İlçeler", bootstyle="primary").pack(anchor="w")
        self.dist_search = tb.Entry(right, bootstyle="info"); self.dist_search.pack(fill="x", pady=(4,8))
        self.dist_search.bind("<KeyRelease>", lambda e: self.refresh_districts())
        self.dist_list = tk.Listbox(right, height=18)
        self.dist_list.pack(fill="both", expand=True)

        d_btns = ttk.Frame(right); d_btns.pack(fill="x", pady=6)
        tb.Button(d_btns, text="Yeni İlçe", bootstyle="success", command=self.add_district).pack(side="left", padx=4)
        tb.Button(d_btns, text="İsim Değiştir", bootstyle="warning", command=self.rename_district).pack(side="left", padx=4)
        tb.Button(d_btns, text="Sil", bootstyle="danger", command=self.delete_district).pack(side="left", padx=4)

        # initial load
        self.refresh_provinces()

    def refresh_provinces(self):
        term = self.prov_search.get().strip()
        items = query_provinces(term)
        self.prov_list.delete(0, tk.END)
        for it in items:
            self.prov_list.insert(tk.END, it)
        # clear districts
        self.dist_list.delete(0, tk.END)

    def on_province_selected(self):
        self.refresh_districts()

    def refresh_districts(self):
        sel = self.get_selected_province()
        if not sel:
            self.dist_list.delete(0, tk.END); return
        term = self.dist_search.get().strip()
        items = query_districts(sel, term)
        self.dist_list.delete(0, tk.END)
        for it in items:
            self.dist_list.insert(tk.END, it)

    def get_selected_province(self):
        sel = self.prov_list.curselection()
        if not sel: return None
        return self.prov_list.get(sel[0])

    def get_selected_district(self):
        sel = self.dist_list.curselection()
        if not sel: return None
        return self.dist_list.get(sel[0])

    # Province operations
    def add_province(self):
        name = simpledialog.askstring("Yeni İl", "Yeni il adı:", parent=self.win)
        if not name: return
        try:
            add_province(name)
            self.refresh_provinces()
            messagebox.showinfo("Başarılı", f"İl '{name}' eklendi.", parent=self.win)
        except Exception as e:
            messagebox.showerror("Hata", str(e), parent=self.win)

    def rename_province(self):
        sel = self.get_selected_province()
        if not sel:
            messagebox.showwarning("Uyarı", "Lütfen bir il seçin.", parent=self.win); return
        new = simpledialog.askstring("İsim Değiştir", f"'{sel}' yeni adı:", parent=self.win)
        if not new: return
        try:
            rename_province(sel, new)
            self.refresh_provinces()
            messagebox.showinfo("Başarılı", f"'{sel}' -> '{new}'", parent=self.win)
        except Exception as e:
            messagebox.showerror("Hata", str(e), parent=self.win)

    def delete_province(self):
        sel = self.get_selected_province()
        if not sel:
            messagebox.showwarning("Uyarı", "Lütfen bir il seçin.", parent=self.win); return
        if not messagebox.askyesno("Sil", f"'{sel}' silinecek. Devam?", parent=self.win): return
        try:
            delete_province(sel)
            self.refresh_provinces()
            messagebox.showinfo("Başarılı", f"'{sel}' silindi.", parent=self.win)
        except Exception as e:
            messagebox.showerror("Hata", str(e), parent=self.win)

    # District operations
    def add_district(self):
        prov = self.get_selected_province()
        if not prov:
            messagebox.showwarning("Uyarı", "Lütfen önce bir il seçin.", parent=self.win); return
        name = simpledialog.askstring("Yeni İlçe", "Yeni ilçe adı:", parent=self.win)
        if not name: return
        try:
            add_district(prov, name)
            self.refresh_districts()
            messagebox.showinfo("Başarılı", f"İlçe '{name}' eklendi.", parent=self.win)
        except Exception as e:
            messagebox.showerror("Hata", str(e), parent=self.win)

    def rename_district(self):
        prov = self.get_selected_province()
        sel = self.get_selected_district()
        if not prov or not sel:
            messagebox.showwarning("Uyarı", "Lütfen il ve ilçe seçin.", parent=self.win); return
        new = simpledialog.askstring("İsim Değiştir", f"'{sel}' yeni adı:", parent=self.win)
        if not new: return
        try:
            rename_district(prov, sel, new)
            self.refresh_districts()
            messagebox.showinfo("Başarılı", f"'{sel}' -> '{new}'", parent=self.win)
        except Exception as e:
            messagebox.showerror("Hata", str(e), parent=self.win)

    def delete_district(self):
        prov = self.get_selected_province()
        sel = self.get_selected_district()
        if not prov or not sel:
            messagebox.showwarning("Uyarı", "Lütfen il ve ilçe seçin.", parent=self.win); return
        if not messagebox.askyesno("Sil", f"'{sel}' silinecek. Devam?", parent=self.win): return
        try:
            delete_district(prov, sel)
            self.refresh_districts()
            messagebox.showinfo("Başarılı", f"'{sel}' silindi.", parent=self.win)
        except Exception as e:
            messagebox.showerror("Hata", str(e), parent=self.win)