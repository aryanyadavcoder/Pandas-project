import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import main as sn
import yfinance as yf
import threading
import time

# ---------- ROOT ----------
root = tk.Tk()
root.title("🔥 Stock Pro Dashboard")
root.geometry("1200x700")
root.configure(bg="#0f172a")

# ---------- SIDEBAR ----------
sidebar = tk.Frame(root, bg="#020617", width=200)
sidebar.pack(side="left", fill="y")

def side_btn(text, cmd):
    return tk.Button(sidebar, text=text, command=cmd,
                     bg="#020617", fg="white",
                     font=("Arial", 11), bd=0, anchor="w", padx=20)

# ---------- MAIN ----------
main = tk.Frame(root, bg="#0f172a")
main.pack(fill="both", expand=True)

# ---------- INPUT PANEL ----------
panel = tk.Frame(main, bg="#1e293b", padx=20, pady=20)
panel.pack(pady=20)

def lbl(text, r):
    tk.Label(panel, text=text, bg="#1e293b", fg="white").grid(row=r, column=0, pady=5)

def ent(r):
    e = tk.Entry(panel)
    e.grid(row=r, column=1, pady=5)
    return e

lbl("Share Name",0); share_entry = ent(0)
lbl("Buy Qty",1); buy_entry = ent(1)
lbl("Sell Qty",2); sell_entry = ent(2)
lbl("Alert Price",3); alert_entry = ent(3)

result_label = tk.Label(main, text="", bg="#0f172a", fg="white")
result_label.pack()

# ---------- HELPERS ----------
def format_ticker(name):
    name = name.strip().upper()
    if not name.endswith(".NS"):
        name += ".NS"
    return name

def save_transaction(action, sharename, qty):
    try:
        with open("transactions.json", "r") as f:
            data = json.load(f)
    except:
        data = []
    data.append({
        "Action": action,
        "Share": sharename,
        "Quantity": qty,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open("transactions.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------- CORE ----------
def buy_stock():
    try:
        s = format_ticker(share_entry.get())
        q = int(buy_entry.get())
        sn.purchase(s, str(date.today()), q)
        save_transaction("BUY", s, q)
        result_label.config(text=f"Bought {q} {s}", fg="green")
    except Exception as e:
        result_label.config(text=e, fg="red")

def sell_stock():
    try:
        s = format_ticker(share_entry.get())
        q = int(sell_entry.get())
        sn.sell(s, q)
        save_transaction("SELL", s, q)
        result_label.config(text=f"Sold {q} {s}", fg="orange")
    except Exception as e:
        result_label.config(text=e, fg="red")

def show_current_price():
    try:
        s = format_ticker(share_entry.get())
        price = sn.readPrice(s)
        result_label.config(text=f"₹ {round(price,2)}", fg="cyan")
    except Exception as e:
        result_label.config(text=e, fg="red")

# ---------- PORTFOLIO ----------
def show_portfolio():
    try:
        with open("purchase.json","r") as f:
            stocks = json.load(f)

        win = tk.Toplevel(root)
        win.title("Portfolio")

        table = ttk.Treeview(win, columns=("Share","Qty","Avg","Current","Value","P/L"), show="headings")
        for col in ("Share","Qty","Avg","Current","Value","P/L"):
            table.heading(col, text=col)
        table.pack(fill="x")

        shares = []
        profits = []
        values = []

        for s in stocks:
            current = sn.readPrice(s["Share"])
            pl = (current - s["Avg_Price"]) * s["Quantity"]
            val = current * s["Quantity"]

            shares.append(s["Share"])
            profits.append(pl)
            values.append(val)

            table.insert("", "end", values=(s["Share"], s["Quantity"], s["Avg_Price"], current, val, pl))

        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack()

        ax.bar(shares, profits)
        canvas.draw()

        fig2, ax2 = plt.subplots()
        canvas2 = FigureCanvasTkAgg(fig2, master=win)
        canvas2.get_tk_widget().pack()

        ax2.pie(values, labels=shares, autopct="%1.1f%%")
        canvas2.draw()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- PRICE HISTORY ----------
def show_price_history():
    s = format_ticker(share_entry.get())
    data = yf.download(s, period="3mo")

    win = tk.Toplevel(root)
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    ax.plot(data["Close"])
    canvas.draw()

# ---------- ALERT ----------
alerts = []

def add_price_alert():
    s = format_ticker(share_entry.get())
    t = float(alert_entry.get())
    alerts.append((s,t))
    result_label.config(text="Alert Set", fg="yellow")

def check_alerts():
    while True:
        for s,t in alerts:
            try:
                if sn.readPrice(s) >= t:
                    messagebox.showinfo("Alert", f"{s} reached {t}")
            except: pass
        time.sleep(5)

threading.Thread(target=check_alerts, daemon=True).start()

# ---------- WATCHLIST ----------
watchlist = []

def add_watchlist():
    s = format_ticker(share_entry.get())
    if s not in watchlist:
        watchlist.append(s)
        messagebox.showinfo("Watchlist", "Added")

def show_watchlist():
    win = tk.Toplevel(root)
    table = ttk.Treeview(win, columns=("Share","Price"), show="headings")
    table.heading("Share", text="Share")
    table.heading("Price", text="Price")

    for s in watchlist:
        table.insert("", "end", values=(s, sn.readPrice(s)))

    table.pack()

# ---------- TRANSACTIONS ----------
def show_transaction_history():
    try:
        with open("transactions.json","r") as f:
            data = json.load(f)
    except:
        data = []

    win = tk.Toplevel(root)
    table = ttk.Treeview(win, columns=("Action","Share","Qty","Date"), show="headings")

    for col in ("Action","Share","Qty","Date"):
        table.heading(col, text=col)

    for d in data:
        table.insert("", "end", values=(d["Action"],d["Share"],d["Quantity"],d["Date"]))

    table.pack(fill="both", expand=True)

# ---------- EXPORT ----------
def export_portfolio():
    with open("purchase.json","r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    file = filedialog.asksaveasfilename(defaultextension=".csv")
    if file:
        df.to_csv(file,index=False)
        result_label.config(text="Exported!", fg="green")

# ---------- BUTTON GRID ----------
btn_frame = tk.Frame(main, bg="#0f172a")
btn_frame.pack(pady=20)

def btn(text, cmd, r, c, color):
    tk.Button(btn_frame, text=text, command=cmd,
              bg=color, fg="white", width=15).grid(row=r, column=c, padx=10, pady=10)

btn("BUY", buy_stock, 0,0,"green")
btn("SELL", sell_stock,0,1,"red")
btn("PRICE", show_current_price,0,2,"blue")

btn("PORTFOLIO", show_portfolio,1,0,"#6366f1")
btn("HISTORY", show_price_history,1,1,"#f59e0b")
btn("ALERT", add_price_alert,1,2,"#a855f7")

btn("WATCH ADD", add_watchlist,2,0,"#06b6d4")
btn("WATCHLIST", show_watchlist,2,1,"#22c55e")
btn("TRANSACTIONS", show_transaction_history,2,2,"#ef4444")

btn("EXPORT", export_portfolio,3,1,"#10b981")

root.mainloop()