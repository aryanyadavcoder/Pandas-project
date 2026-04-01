import threading
import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime


def readPrice(sharename):
    # automatic .NS formatting for professional touch
    ticker = sharename.upper()
    if ".NS" not in ticker and "." not in ticker: ticker += ".NS"
    
    try:
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if data.empty: return 0.0
        return round(data["Close"].iloc[-1].item(), 2)
    except: return 0.0

def onedaychart_data(sharename):
    return yf.download(sharename, period="1d", interval="1m", progress=False)

def purchase_stock_logic(shares, quantity):
    # Professional Feedback
    print(f"Purchasing {quantity} of {shares}...")
    price = readPrice(shares)
    
    if price == 0:
        raise ValueError("Invalid Ticker or Price not available.")
        
    total_price = price * quantity
    date_now = str(datetime.now().date())
    
    # Try to load existing
    try:
        with open("purchase.json", "r") as f: data = json.load(f)
    except: data = []

    # Update or Add new
    found = False
    for stock in data:
        if stock["Share"] == shares:
            new_qty = stock["Quantity"] + quantity
            # Average Price calculation
            stock["Avg_Price"] = round(((stock["Avg_Price"] * stock["Quantity"]) + (price * quantity)) / new_qty, 2)
            stock["Quantity"] = new_qty
            stock["Total_Price"] = round(stock["Avg_Price"] * new_qty, 2)
            found = True
            break
    
    if not found:
        data.append({
            "Share": shares, "Date": date_now, "Quantity": quantity,
            "Total_Price": total_price, "Avg_Price": price,
            "current_price": price, "Profit_loss": 0.0
        })

    with open("purchase.json", "w") as f:
        json.dump(data, f, indent=4)
    return price

# 2. MAIN GUI CLASS (Software Structure)

class StockTerminalGUI:  
    def __init__(self, root):
        self.root = root
        self.root.title("TERMINAL - PROFESSIONAL STOCK MANAGER")
        self.root.geometry("1100x750")
        
        # Professional Color Palette (FIXED 'brand2' error)
        self.colors = {
            "bg": "#121212", # Dark
            "panel": "#1e1e1e", # Card
            "ink": "#ffffff", # Text
            "muted": "#888888",
            "brand": "#00ffcc",  # Neon Cyan
            "brand2": "#f59e0b", # Orange (Fixed KeyError)
            "danger": "#ff4444" # Red
        }

        self.root.configure(bg=self.colors["bg"])
        self._setup_styles()
        self._build_ui()
        self.refresh_portfolio_data() # Initial load on start

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.colors["panel"], foreground="white", padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", self.colors["brand"])], foreground=[("selected", "black")])
        
        style.configure("Treeview", background=self.colors["panel"], foreground="white", fieldbackground=self.colors["panel"], borderwidth=0)
        style.configure("Treeview.Heading", background="#333", foreground="white", font=("Arial", 10, "bold"))

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["panel"], height=60)
        header.pack(fill="x")
        tk.Label(header, text="STOCK TRADER PRO", font=("Impact", 20), bg=self.colors["panel"], fg=self.colors["brand"]).pack(side="left", padx=20)

        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_trade = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.tab_portfolio = tk.Frame(self.notebook, bg=self.colors["bg"])
        
        self.notebook.add(self.tab_trade, text=" LIVE TRADING ")
        self.notebook.add(self.tab_portfolio, text=" MY PORTFOLIO ")

        self._build_trade_section()
        self._build_portfolio_section()

    def _build_trade_section(self):
        # Professional Layout: Left Inputs, Right Chart
        controls = tk.Frame(self.tab_trade, bg=self.colors["panel"], width=300, padx=20, pady=20, highlightthickness=1, highlightbackground="#333")
        controls.pack(side="left", fill="y", padx=5, pady=5)

        tk.Label(controls, text="STOCK SYMBOL (e.g. TCS)", bg=self.colors["panel"], fg=self.colors["muted"]).pack(anchor="w")
        self.ticker_var = tk.StringVar(value="RELIANCE.NS")
        tk.Entry(controls, textvariable=self.ticker_var, bg="#333", fg="white", font=("Arial", 12), bd=0, insertbackground="white").pack(fill="x", pady=5, ipady=5)

        tk.Label(controls, text="QUANTITY", bg=self.colors["panel"], fg=self.colors["muted"]).pack(anchor="w", pady=(10,0))
        self.qty_var = tk.StringVar(value="1")
        tk.Entry(controls, textvariable=self.qty_var, bg="#333", fg="white", font=("Arial", 12), bd=0, insertbackground="white").pack(fill="x", pady=5, ipady=5)

        self.price_display = tk.Label(controls, text="₹ 0.00", bg=self.colors["panel"], fg=self.colors["brand"], font=("Arial", 18, "bold"))
        self.price_display.pack(pady=20)

        # Buttons with Professional Styles
        tk.Button(controls, text="BUY STOCK", bg=self.colors["brand"], fg="black", font=("Arial", 10, "bold"), bd=0, command=self.handle_buy_click).pack(fill="x", pady=5, ipady=8)
        tk.Button(controls, text="SELL STOCK", bg=self.colors["danger"], fg="white", font=("Arial", 10, "bold"), bd=0, command=lambda: messagebox.showinfo("Info","Sell feature is not yet mapped")).pack(fill="x", pady=5, ipady=8)
        tk.Button(controls, text="GET PRICE", bg="#444", fg="white", bd=0, command=self.update_live_price).pack(fill="x", pady=5, ipady=5)
        tk.Button(controls, text="VIEW CHART", bg="#007bff", fg="white", bd=0, command=self.plot_live_chart).pack(fill="x", pady=5, ipady=5)

        # Chart Area (Right)
        self.chart_frame = tk.Frame(self.tab_trade, bg=self.colors["bg"])
        self.chart_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor=self.colors["bg"])
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.colors["panel"])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _build_portfolio_section(self):
        cols = ("Share", "Qty", "Avg Price", "Current", "Value", "PnL")
        self.tree = ttk.Treeview(self.tab_portfolio, columns=cols, show="headings")
        for col in cols: self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Action Buttons
        btn_frame = tk.Frame(self.tab_portfolio, bg=self.colors["bg"])
        btn_frame.pack(fill="x", padx=10)

        # brand2 color fixed
        tk.Button(btn_frame, text="REFRESH PORTFOLIO", bg=self.colors["brand2"], command=self.refresh_portfolio_data, bd=0, padx=10).pack(side="left", pady=10, ipady=5)
        tk.Button(btn_frame, text="EXPORT CSV", bg="#444", fg="white", bd=0, padx=10, command=self.export_csv).pack(side="left", padx=10, pady=10, ipady=5)

    # 3. INTERFACE LOGIC (Multi-Threading)

    def update_live_price(self):
        sym = self.ticker_var.get().upper()
        if not sym: return
        price = readPrice(sym)
        self.price_display.config(text=f"₹ {price}")
        return price

    def plot_live_chart(self):
        sym = self.ticker_var.get().upper()
        def thread_task():
            data = onedaychart_data(sym)
            if data.empty: return
            self.ax.clear()
            # Professional Color and Tick Styling
            self.ax.plot(data['Close'], color=self.colors["brand"], linewidth=2)
            self.ax.tick_params(colors='white', labelsize=8)
            self.ax.set_title(f"{sym} Intraday", color='white')
            self.canvas.draw()
        
        # Multithreading added for Professional Touch
        threading.Thread(target=thread_task, daemon=True).start()

    def handle_buy_click(self):
        sym = self.ticker_var.get().upper()
        try:
            q = int(self.qty_var.get())
            if q <= 0: raise ValueError
            
            # Calling your simple core function
            buy_price = purchase_stock_logic(sym, q)
            messagebox.showinfo("Success", f"Order Placed!\n{q} shares of {sym} at ₹{buy_price}")
            self.refresh_portfolio_data()
        except Exception as e:
            messagebox.showerror("Error", f"Transaction Failed: {e}")

    def refresh_portfolio_data(self):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            with open("purchase.json", "r") as f:
                stocks = json.load(f)
            
            for s in stocks:
                curr = readPrice(s["Share"])
                total_val = round(curr * s["Quantity"], 2)
                pnl = round((curr - s["Avg_Price"]) * s["Quantity"], 2)
                
                # Check color for pnl
                if pnl >= 0:
                    item_id = self.tree.insert("", "end", values=(
                        s["Share"], s["Quantity"], s["Avg_Price"], curr, total_val, pnl
                    ))
                    self.tree.tag_configure("gain", foreground="green")
                    self.tree.item(item_id, tags=("gain",))
                else:
                    item_id = self.tree.insert("", "end", values=(
                        s["Share"], s["Quantity"], s["Avg_Price"], curr, total_val, pnl
                    ))
                    self.tree.tag_configure("loss", foreground="red")
                    self.tree.item(item_id, tags=("loss",))
        except:
            pass

    def export_csv(self):
        # Professional Feature
        try:
            df = pd.read_json("purchase.json")
            df.to_csv("my_portfolio.csv", index=False)
            messagebox.showinfo("Success", "Portfolio exported to my_portfolio.csv")
        except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = StockTerminalGUI(root)
    root.mainloop()