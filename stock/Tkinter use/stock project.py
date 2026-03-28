import tkinter as tk
from datetime import date
import main as sn


root = tk.Tk()
root.title("Stock App")
root.geometry("400x300")
# share input
tk.Label(root, text="Shere name").pack(pady=5)
share_entry = tk.Entry(root)
share_entry.pack(pady=5)
# Quantity input
tk.Label(root, text="Buy Quantity").pack(pady=5)
buy_entry = tk.Entry(root)
buy_entry.pack(pady=5)
# Sell Quantity input
tk.Label(root, text="Sell Quantity").pack(pady=5)
sell_entry = tk.Entry(root)
sell_entry.pack(pady=5)


def buy_stock():
    try:
        sharename = share_entry.get().upper()+".NS"
        quantity = int(buy_entry.get())
        buy_date = str(date.today())
        sn.purchase(sharename, buy_date, quantity)
        buy_label.config(text=f"Bought {quantity} shares of {sharename}")
    except Exception as e:
        buy_label.config(text=f"Error: {e}")


tk.Button(root, text="Buy", command=buy_stock).pack(pady=5)
buy_label = tk.Label(root, text="")
buy_label.pack()


def sell_stock():
    try:
        sharename = share_entry.get().upper()+".NS"
        sell_quantity = int(sell_entry.get())
        sn.sell(sharename, sell_quantity)
        sell_label.config(text=f"sold {sell_quantity} shares of {sharename}")
    except Exception as e:
        sell_label.config(text=f"Error: {e}")


tk.Button(root, text="Sell", command=sell_stock).pack(pady=5)
sell_label = tk.Label(root, text="")
sell_label.pack()


def show_current_price():
    try:
        sharename = share_entry.get().upper()+".NS"
        price = sn.readPrice(sharename)
        price_label.config(text=f"current Price : {round(price,2)}")
    except Exception as e:
        price_label.config(text=f"error:{e}")
tk.Button(root, text="Show current price ",
          command=show_current_price).pack(pady=5)
price_label = tk.Label(root, text="")
price_label.pack()


def show_profit_loss():
    try
root.mainloop()
