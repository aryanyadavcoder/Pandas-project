import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import main as sn  # aapka main.py jisme purchase(), sell(), readPrice() hai
import yfinance as yf
import threading
import time

# ---------- Root Window ----------
root = tk.Tk()
root.title("Stock App")
root.geometry("550x800")

# ---------- Helper Functions ----------
def format_ticker(name):
    name = name.strip().upper()
    if not name.endswith(".NS"):
        name += ".NS"
    return name

def save_transaction(action, sharename, qty):
    try:
        with open("transactions.json", "r") as f:
            transactions = json.load(f)
    except:
        transactions = []
    transactions.append({
        "Action": action,
        "Share": sharename,
        "Quantity": qty,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open("transactions.json", "w") as f:
        json.dump(transactions, f, indent=4)

# ---------- UI ----------
tk.Label(root, text="Share Name").pack(pady=5)
share_entry = tk.Entry(root)
share_entry.pack(pady=5)

tk.Label(root, text="Buy Quantity").pack(pady=5)
buy_entry = tk.Entry(root)
buy_entry.pack(pady=5)

tk.Label(root, text="Sell Quantity").pack(pady=5)
sell_entry = tk.Entry(root)
sell_entry.pack(pady=5)

tk.Label(root, text="Target Price for Alert").pack(pady=5)
alert_entry = tk.Entry(root)
alert_entry.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

# ---------- Portfolio Window Globals ----------
portfolio_win = None
portfolio_canvas = None
portfolio_fig = None
portfolio_ax = None
portfolio_canvas_pie = None
portfolio_fig_pie = None
portfolio_ax_pie = None

# ---------- Alerts / Watchlist ----------
alerts = []
watchlist = []

watchlist_win = None
watchlist_table = None

# ---------- Buy/Sell Functions ----------
def buy_stock():
    try:
        sharename = format_ticker(share_entry.get())
        quantity = int(buy_entry.get())
        if quantity <= 0: raise ValueError("Quantity must be positive")
        sn.purchase(sharename, str(date.today()), quantity)
        save_transaction("BUY", sharename, quantity)
        result_label.config(text=f"Bought {quantity} of {sharename}", fg="green")
        update_portfolio_graph()
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

def sell_stock():
    try:
        sharename = format_ticker(share_entry.get())
        quantity = int(sell_entry.get())
        if quantity <= 0: raise ValueError("Quantity must be positive")
        sn.sell(sharename, quantity)
        save_transaction("SELL", sharename, quantity)
        result_label.config(text=f"Sold {quantity} of {sharename}", fg="green")
        update_portfolio_graph()
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

# ---------- Show Info Functions ----------
def show_current_price():
    try:
        sharename = format_ticker(share_entry.get())
        price = sn.readPrice(sharename)
        result_label.config(text=f"Current Price: ₹{round(price,2)}", fg="blue")
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

def show_profit_loss():
    try:
        sharename = format_ticker(share_entry.get())
        with open("purchase.json", "r") as f:
            stocks = json.load(f)
        for stock in stocks:
            if stock["Share"] == sharename:
                qty = stock["Quantity"]
                buy_price = stock["Avg_Price"]
                current_price = sn.readPrice(sharename)
                profit = round((current_price - buy_price) * qty, 2)
                color = "green" if profit >=0 else "red"
                result_label.config(text=f"P/L: ₹{profit} | Qty: {qty}", fg=color)
                return
        result_label.config(text="Stock not found", fg="orange")
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

def show_total_profit():
    try:
        with open("purchase.json","r") as f:
            stocks = json.load(f)
        total_profit = 0
        for stock in stocks:
            qty = stock["Quantity"]
            buy_price = stock["Avg_Price"]
            current_price = sn.readPrice(stock["Share"])
            total_profit += (current_price - buy_price) * qty
        total_profit = round(total_profit,2)
        color = "green" if total_profit >=0 else "red"
        result_label.config(text=f"Total P/L: ₹{total_profit}", fg=color)
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

# ---------- Portfolio & Graph ----------
def show_portfolio():
    global portfolio_win, portfolio_canvas, portfolio_fig, portfolio_ax
    global portfolio_canvas_pie, portfolio_fig_pie, portfolio_ax_pie
    try:
        with open("purchase.json","r") as f:
            stocks = json.load(f)
        if portfolio_win is None or not portfolio_win.winfo_exists():
            portfolio_win = tk.Toplevel(root)
            portfolio_win.title("Portfolio")
            portfolio_win.geometry("700x500")
            
            # Search
            tk.Label(portfolio_win, text="Search Share:").pack(pady=3)
            search_entry = tk.Entry(portfolio_win)
            search_entry.pack(pady=3)
            
            # Table
            table = ttk.Treeview(portfolio_win, columns=("Share","Qty","Avg","Current","Value","P/L"), show="headings")
            for col, text in zip(("Share","Qty","Avg","Current","Value","P/L"),
                                 ("Share","Quantity","Avg Price","Current Price","Total Value","Profit/Loss")):
                table.heading(col,text=text)
            table.pack(fill="x")
            portfolio_win.table = table  # save reference
            
            # Bar Graph
            portfolio_fig, portfolio_ax = plt.subplots(figsize=(6,3))
            portfolio_canvas = FigureCanvasTkAgg(portfolio_fig, master=portfolio_win)
            portfolio_canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Pie Chart
            portfolio_fig_pie, portfolio_ax_pie = plt.subplots(figsize=(6,3))
            portfolio_canvas_pie = FigureCanvasTkAgg(portfolio_fig_pie, master=portfolio_win)
            portfolio_canvas_pie.get_tk_widget().pack(fill="both", expand=True)
        
            # Filter function
            def filter_table():
                term = search_entry.get().upper()
                for row in table.get_children():
                    table.delete(row)
                for stock in stocks:
                    if term in stock["Share"]:
                        sharename = stock["Share"]
                        qty = stock["Quantity"]
                        avg = stock["Avg_Price"]
                        current = sn.readPrice(sharename)
                        value = round(current*qty,2)
                        pl = round((current-avg)*qty,2)
                        table.insert("", "end", values=(sharename, qty, avg, current, value, pl))
            search_entry.bind("<KeyRelease>", lambda e: filter_table())

        update_portfolio_graph()
        auto_refresh()  # auto-refresh start
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_portfolio_graph():
    global portfolio_win, portfolio_canvas, portfolio_fig, portfolio_ax
    global portfolio_canvas_pie, portfolio_fig_pie, portfolio_ax_pie
    if portfolio_win is None or not portfolio_win.winfo_exists():
        return
    try:
        with open("purchase.json","r") as f:
            stocks = json.load(f)
        table = portfolio_win.table
        # --- Update Table ---
        for i in table.get_children():
            table.delete(i)
        for stock in stocks:
            sharename = stock["Share"]
            qty = stock["Quantity"]
            avg = stock["Avg_Price"]
            current = sn.readPrice(sharename)
            value = round(current*qty,2)
            pl = round((current-avg)*qty,2)
            table.insert("", "end", values=(sharename, qty, avg, current, value, pl))
        
        # --- Bar Graph ---
        portfolio_ax.clear()
        shares = [s["Share"] for s in stocks]
        profits = [round((sn.readPrice(s["Share"])-s["Avg_Price"])*s["Quantity"],2) for s in stocks]
        colors = ["green" if p>=0 else "red" for p in profits]
        portfolio_ax.bar(shares, profits, color=colors)
        portfolio_ax.set_ylabel("Profit/Loss ₹")
        portfolio_ax.set_title("Portfolio Profit/Loss")
        portfolio_ax.axhline(0,color='black',linewidth=0.8)
        portfolio_fig.tight_layout()
        portfolio_canvas.draw()
        
        # --- Pie Chart ---
        portfolio_ax_pie.clear()
        values = [round(sn.readPrice(s["Share"])*s["Quantity"],2) for s in stocks]
        labels = [s["Share"] for s in stocks]
        if values:
            portfolio_ax_pie.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            portfolio_ax_pie.set_title("Portfolio Distribution")
        portfolio_fig_pie.tight_layout()
        portfolio_canvas_pie.draw()
    except Exception as e:
        print("Graph Update Error:", e)

def auto_refresh():
    update_portfolio_graph()
    check_price_alerts()
    update_watchlist_table()
    if portfolio_win is not None and portfolio_win.winfo_exists():
        portfolio_win.after(5000, auto_refresh)  # 5 sec refresh

# ---------- Transactions ----------
def show_transaction_history():
    try:
        import os
        if os.path.exists("transactions.json"):
            with open("transactions.json","r") as f:
                trans = json.load(f)
        else:
            trans = []
        win = tk.Toplevel(root)
        win.title("Transactions")
        table = ttk.Treeview(win, columns=("Action","Share","Qty","Date"), show="headings")
        for col in ("Action","Share","Qty","Date"):
            table.heading(col,text=col)
        for t in trans:
            table.insert("", "end", values=(t["Action"],t["Share"],t["Quantity"],t["Date"]))
        table.pack(fill="both", expand=True)
        if len(trans)==0:
            messagebox.showinfo("Info","No transactions yet!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- Export ----------
def export_portfolio():
    try:
        with open("purchase.json","r") as f:
            stocks = json.load(f)
        df = pd.DataFrame(stocks)
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
        filetypes=[("CSV files","*.csv")])
        if filename:
            df.to_csv(filename,index=False)
            result_label.config(text="Portfolio exported!", fg="blue")
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

# ---------- Price History ----------
def show_price_history():
    sharename = format_ticker(share_entry.get())
    try:
        data = yf.download(sharename, period="3mo")
        data["Daily Return"] = data["Close"].pct_change() * 100

        history_win = tk.Toplevel(root)
        history_win.title(f"{sharename} - Price History")
        history_win.geometry("800x500")

        chart_var = tk.StringVar()
        chart_var.set("Close Price")
        chart_options = ["Close Price", "Volume", "Daily Return", "Histogram"]
        tk.Label(history_win, text="Select Chart Type:").pack(pady=5)
        dropdown = tk.OptionMenu(history_win, chart_var, *chart_options)
        dropdown.pack(pady=5)

        canvas_frame = tk.Frame(history_win)
        canvas_frame.pack(fill="both", expand=True)
        fig, ax = plt.subplots(figsize=(8,4))
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        def draw_chart(*args):
            ax.clear()
            chart_type = chart_var.get()
            if chart_type == "Close Price":
                ax.plot(data.index, data["Close"], color="blue")
                ax.set_ylabel("Close Price ₹")
            elif chart_type == "Volume":
                ax.bar(data.index, data["Volume"], color="orange")
                ax.set_ylabel("Volume")
            elif chart_type == "Daily Return":
                ax.plot(data.index, data["Daily Return"], color="green")
                ax.set_ylabel("Daily Return %")
            elif chart_type == "Histogram":
                ax.hist(data["Daily Return"].dropna(), bins=20, color="purple", edgecolor="black")
                ax.set_xlabel("Daily Return %")
                ax.set_ylabel("Frequency")
            ax.set_title(f"{sharename} - {chart_type}")
            fig.autofmt_xdate()
            fig.tight_layout()
            canvas.draw()

        chart_var.trace("w", draw_chart)
        draw_chart()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- Price Alert ----------
def add_price_alert():
    try:
        sharename = format_ticker(share_entry.get())
        target = float(alert_entry.get())
        alerts.append({"Share": sharename, "Target": target})
        result_label.config(text=f"Price Alert set for {sharename} at ₹{target}", fg="purple")
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

def check_price_alerts():
    remove_list = []
    for alert in alerts:
        try:
            current_price = sn.readPrice(alert["Share"])
            if current_price >= alert["Target"]:
                messagebox.showinfo("Price Alert", f"{alert['Share']} reached ₹{alert['Target']} (Current: ₹{current_price})")
                remove_list.append(alert)
        except:
            pass
    for r in remove_list:
        alerts.remove(r)

# ---------- Watchlist ----------
def add_to_watchlist():
    sharename = format_ticker(share_entry.get())
    if sharename not in watchlist:
        watchlist.append(sharename)
        messagebox.showinfo("Watchlist", f"{sharename} added to watchlist")
    update_watchlist_table()

def show_watchlist():
    global watchlist_win, watchlist_table
    if watchlist_win is None or not watchlist_win.winfo_exists():
        watchlist_win = tk.Toplevel(root)
        watchlist_win.title("Watchlist")
        watchlist_win.geometry("500x400")
        watchlist_table = ttk.Treeview(watchlist_win, columns=("Share","Current Price","Target","Alert"), show="headings")
        for col in ("Share","Current Price","Target","Alert"):
            watchlist_table.heading(col,text=col)
        watchlist_table.pack(fill="both", expand=True)
    update_watchlist_table()
    auto_refresh_watchlist()

def update_watchlist_table():
    if watchlist_table is None:
        return
    for i in watchlist_table.get_children():
        watchlist_table.delete(i)
    for s in watchlist:
        cur = sn.readPrice(s)
        target = None
        alert_flag=""
        for a in alerts:
            if a["Share"]==s:
                target=a["Target"]
                if cur>=target:
                    alert_flag="Reached!"
        watchlist_table.insert("", "end", values=(s,cur,target,alert_flag))

def auto_refresh_watchlist():
    update_watchlist_table()
    if watchlist_win and watchlist_win.winfo_exists():
        watchlist_win.after(5000, auto_refresh_watchlist)

# ---------- Threaded Alert Checker ----------
def start_alert_checker():
    def check_alerts_loop():
        while True:
            check_price_alerts()
            time.sleep(5)
    threading.Thread(target=check_alerts_loop, daemon=True).start()

start_alert_checker()

# ---------- Buttons ----------
tk.Button(root, text="Buy", command=buy_stock).pack(pady=5)
tk.Button(root, text="Sell", command=sell_stock).pack(pady=5)
tk.Button(root, text="Current Price", command=show_current_price).pack(pady=5)
tk.Button(root, text="Profit/Loss", command=show_profit_loss).pack(pady=5)
tk.Button(root, text="Total Profit", command=show_total_profit).pack(pady=5)
tk.Button(root, text="Show Portfolio", command=show_portfolio).pack(pady=5)
tk.Button(root, text="Transaction History", command=show_transaction_history).pack(pady=5)
tk.Button(root, text="Export Portfolio", command=export_portfolio).pack(pady=5)
tk.Button(root, text="Show Price History", command=show_price_history).pack(pady=5)
tk.Button(root, text="Set Price Alert", command=add_price_alert).pack(pady=5)
tk.Button(root, text="Add to Watchlist", command=add_to_watchlist).pack(pady=5)
tk.Button(root, text="Show Watchlist", command=show_watchlist).pack(pady=5)

root.mainloop()