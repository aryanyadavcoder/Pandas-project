import tkinter as tk
from tkinter import messagebox
import main as sn   # तुम्हारा function file

root = tk.Tk()
root.title("Stock App")
root.geometry("400x400")

# -------- INPUT --------
tk.Label(root, text="Share Name").pack()
share_entry = tk.Entry(root)
share_entry.pack()
share_entry.insert(0, "RELIANCE.NS")

tk.Label(root, text="Quantity").pack()
qty_entry = tk.Entry(root)
qty_entry.pack()

result = tk.Label(root, text="")
result.pack(pady=10)

# -------- FUNCTIONS --------

def price():
    try:
        p = sn.readPrice(share_entry.get())
        result.config(text=f"Price: ₹{p}")
    except Exception as e:
        result.config(text=str(e))

def buy():
    try:
        sn.purchase(share_entry.get(), "2026-03-31", int(qty_entry.get()))
        result.config(text="Stock Buy हो गया ✅")
    except Exception as e:
        result.config(text=str(e))

def sell():
    try:
        sn.sell(share_entry.get(), int(qty_entry.get()))
        result.config(text="Stock Sell हो गया ✅")
    except Exception as e:
        result.config(text=str(e))

def chart():
    try:
        sn.profit_loss_chart(share_entry.get())
    except Exception as e:
        result.config(text=str(e))

# -------- BUTTONS --------
tk.Button(root, text="Price", command=price).pack(pady=5)
tk.Button(root, text="Buy", command=buy).pack(pady=5)
tk.Button(root, text="Sell", command=sell).pack(pady=5)
tk.Button(root, text="Profit Chart", command=chart).pack(pady=5)

root.mainloop()