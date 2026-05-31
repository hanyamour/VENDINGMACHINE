import tkinter as tk
from tkinter import messagebox
import random

class SimpleVendingMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine Modern")
        self.root.geometry("900x520")

        #DATABASE BARANG
        self.stock = {
            "Coca Cola": {"price": 10000, "count": 5, "icon": "🥤"},
            "Pepsi": {"price": 10000, "count": 3, "icon": "🔵"},
            "Popcorn": {"price": 15000, "count": 8, "icon": "🍿"},
            "Air Mineral": {"price": 5000, "count": 10, "icon": "💧"}
        }

        self.cart = []
        self.released_items = []

        #FRAME UTAMA
        self.left_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.create_widgets()
        self.update_stock_display()
        self.update_cart_display()

    def create_widgets(self):
        #KIRI
        tk.Label(
            self.left_frame,
            text="=== ETALASE VENDING MACHINE ===",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        grid_frame = tk.Frame(self.left_frame)
        grid_frame.pack(pady=10)

        row, col = 0, 0
        for item_name, info in self.stock.items():
            btn_text = f"{info['icon']}\n{item_name}\nRp {info['price']:,}"

            btn = tk.Button(
                grid_frame,
                text=btn_text,
                width=12,
                height=4,
                command=lambda name=item_name: self.add_to_cart(name)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col > 1:
                col = 0
                row += 1

        #DISPENSER
        tk.Label(
            self.left_frame,
            text="Dispenser / Tempat Ambil Barang:"
        ).pack(pady=(20, 2))

        self.lbl_dispenser = tk.Label(
            self.left_frame,
            text="[Kosong]",
            font=("Arial", 12, "bold"),
            bd=2,
            relief=tk.SUNKEN,
            width=40,
            height=2,
            bg="lightgrey"
        )
        self.lbl_dispenser.pack()

        #LIST BARANG KELUAR
        tk.Label(
            self.left_frame,
            text="Barang yang Sudah Keluar:",
            font=("Arial", 10, "bold")
        ).pack(pady=(15, 2))

        self.released_listbox = tk.Listbox(self.left_frame, width=40, height=6)
        self.released_listbox.pack()

        #KANAN
        tk.Label(
            self.right_frame,
            text="INFO STOK BARANG:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.lbl_stock_info = tk.Label(
            self.right_frame,
            text="",
            justify=tk.LEFT,
            font=("Courier", 10)
        )
        self.lbl_stock_info.pack(anchor="w", pady=5)

        #INFO JUMLAH BARANG DAN TOTAL
        self.lbl_cart_info = tk.Label(
            self.right_frame,
            text="Jumlah Barang: 0\nTotal Harga: Rp 0",
            font=("Arial", 10, "bold"),
            fg="blue",
            justify=tk.LEFT
        )
        self.lbl_cart_info.pack(anchor="w", pady=10)

        #KERANJANG
        tk.Label(
            self.right_frame,
            text="KERANJANG BELANJA:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(10, 2))

        self.cart_listbox = tk.Listbox(self.right_frame, width=35, height=8)
        self.cart_listbox.pack()

        #TOMBOL HAPUS
        tk.Button(
            self.right_frame,
            text="Hapus Item Terpilih",
            command=self.remove_selected_item,
            bg="orange"
        ).pack(fill=tk.X, pady=5)

        #TOMBOL BAYAR
        tk.Button(
            self.right_frame,
            text="BAYAR SEKARANG",
            command=self.show_qr_payment,
            bg="lightblue",
            font=("Arial", 11, "bold")
        ).pack(fill=tk.X, pady=10)

    #LOGIKA

    def update_stock_display(self):
        text_display = ""

        for name, info in self.stock.items():
            text_display += f"{info['icon']} {name.ljust(10)}: Sisa {info['count']} pcs\n"

        self.lbl_stock_info.config(text=text_display)

    def update_cart_display(self):
        self.cart_listbox.delete(0, tk.END)

        for idx, item in enumerate(self.cart, start=1):
            self.cart_listbox.insert(
                tk.END,
                f"{idx}. {item} (Rp {self.stock[item]['price']:,})"
            )

        total_cost = sum(self.stock[item]["price"] for item in self.cart)

        self.lbl_cart_info.config(
            text=f"Jumlah Barang: {len(self.cart)}\n"
                 f"Total Harga: Rp {total_cost:,}"
        )

    def add_to_cart(self, item_name):
        if self.stock[item_name]["count"] > 0:
            self.stock[item_name]["count"] -= 1
            self.cart.append(item_name)

            self.update_stock_display()
            self.update_cart_display()

        else:
            messagebox.showwarning(
                "Habis",
                f"Stok {item_name} habis!"
            )
        self.released_listbox.delete(0, tk.END)

    def remove_selected_item(self):
        selected_index = self.cart_listbox.curselection()

        if not selected_index:
            messagebox.showwarning(
                "Peringatan",
                "Pilih item yang ingin dihapus!"
            )
            return

        idx = selected_index[0]

        removed_item = self.cart.pop(idx)
        self.stock[removed_item]["count"] += 1

        self.update_stock_display()
        self.update_cart_display()

        messagebox.showinfo(
            "Berhasil",
            f"{removed_item} berhasil dihapus dari keranjang."
        )

    def show_qr_payment(self):
        if not self.cart:
            messagebox.showwarning(
                "Kosong",
                "Keranjang masih kosong!"
            )
            return

        total_cost = sum(self.stock[item]["price"] for item in self.cart)

        qr_window = tk.Toplevel(self.root)
        qr_window.title("QR Payment")
        qr_window.geometry("400x400")

        tk.Label(
            qr_window,
            text="SCAN QR UNTUK PEMBAYARAN",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        #QR
        qr_text = ""
        for i in range(15):
            qr_text += "".join(random.choice(["█", " "]) for _ in range(30)) + "\n"

        qr_label = tk.Label(
            qr_window,
            text=qr_text,
            font=("Courier", 7),
            bg="white",
            relief=tk.SOLID
        )
        qr_label.pack(pady=10)

        tk.Label(
            qr_window,
            text=f"Total Bayar: Rp {total_cost:,}",
            font=("Arial", 11, "bold"),
            fg="green"
        ).pack(pady=10)

        tk.Button(
            qr_window,
            text="Konfirmasi Pembayaran",
            bg="lightgreen",
            command=lambda: self.finish_payment(qr_window)
        ).pack(pady=10)

    def finish_payment(self, qr_window):
        qr_window.destroy()

        messagebox.showinfo(
            "Pembayaran Berhasil",
            "Pembayaran berhasil diproses!"
        )

        self.released_items = []
        self.animate_fifo_release()

    def animate_fifo_release(self):
        if self.cart:
            current_item = self.cart.pop(0)

            icon = self.stock[current_item]["icon"]

            self.lbl_dispenser.config(
                text=f"⏳ Gluduk... Mengeluarkan {icon} {current_item}",
                bg="yellow"
            )

            self.released_items.append(f"{icon} {current_item}")

            self.released_listbox.insert(
                tk.END,
                f"{icon} {current_item}"
            )

            self.update_cart_display()

            self.root.after(1500, self.animate_fifo_release)

        else:
            self.lbl_dispenser.config(
                text="✅ Selesai! Silakan Ambil Barang.",
                bg="lightgreen"
            )

            messagebox.showinfo(
                "Sukses",
                "Semua barang berhasil dikeluarkan!"
            )

#MAIN PROGRAM
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleVendingMachine(root)
    root.mainloop()
