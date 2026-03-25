
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import json


def downloadData(sharename):
    data = yf.download(sharename, start="2025-12-9", end="2026-03-10")
    data.to_csv(f"{sharename}.csv")
    return data


def readCSV(sharename):
    df = pd.read_csv(f"{sharename}.csv")
    return df


def readPrice(sharename):
    data = yf.download(sharename, period="1d", interval="1m")
    price = round(data["Close"].iloc[-1].item(), 2)
    return price


def onedaychart(sharename):
    data = yf.download(sharename, period="1d", interval="1m")
    return data


def plotgraph(data, sharename):
    plt.plot(data["Close"])
    plt.title(sharename + " Chart")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()


def purchase(shares, date, quantity):
    price = readPrice(shares)
    Total_Price = price*quantity
    
    data = {
        "Share": shares,
        "Date": date,
        "Quantity": quantity,
        "Total_Price":Total_Price,
        "Avg_Price": round(price, 2),
        "current_price": round(price, 2),
        "Profit_loss": round(0, 2)
    }
    try:
        with open("purchase.json", "r") as f:
            purchase = json.load(f)
    except:
        purchase = []
    found = False
    for stock in purchase:
        if stock["Share"] == shares:
            old_qty = stock["Quantity"]
            old_price = stock["Avg_Price"]
            new_qty = old_qty + quantity
            avg_price = ((old_price * old_qty) + (price * quantity))/new_qty
            profit_loss = (price-avg_price)*new_qty
            Total_Price = avg_price*new_qty
            stock["Quantity"] = new_qty
            stock["Avg_Price"] = avg_price
            stock["current_price"] = price
            stock["Profit_loss"] = profit_loss
            stock["Total_Price"] = Total_Price
            found = True
            break
    if not found:
        purchase.append(data)
    with open("purchase.json", "w") as f:
        json.dump(purchase, f, indent=4)
    print("stock purchase save")


def profit_loss_chart(share):
    with open("purchase.json", "r") as f:
        stocks = json.load(f)
    for stock in stocks:
        if stock["Share"] == share:
            buy_price = stock["Avg_Price"]
            current_price = stock["current_price"]
            profit_loss = current_price-buy_price
            break
    else:
        print("Stock not found!")
        return
    color = ["blue", "orange"]
    if profit_loss > 0:
        color.append("green")
    else:
        color.append("red")
    x = ["Buy Price", "Current Price", "Profit/loss"]
    y = [buy_price, current_price, profit_loss]

    plt.bar(x, y, color=color, label=share)
    plt.title(f"{share} Profit/Loss")
    plt.ylabel("Avg_Price")
    plt.xlabel("Current_Price")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()


def sell(sharename, sell_quantity):
    price = readPrice(sharename)
    with open("purchase.json", "r") as f:
        stocks = json.load(f)
    for stock in stocks:
        if stock["Share"] == sharename:
            if sell_quantity > stock["Quantity"]:
                print("Sell quantity not avalible")
                return
            buy_price = stock["Avg_Price"]
            profit = (price - buy_price) * sell_quantity
            stock["Quantity"] -= sell_quantity
            remaining_qty = stock["Quantity"]
            current_price = price
            buy_price = stock["Avg_Price"]
            profit_loss = (current_price-buy_price) * remaining_qty
            stock["current_price"] = round(current_price, 2)
            stock["Profit_loss"] = round(profit_loss, 2)
            sell_data = {
                "Share": sharename,
                "Sell_Quantity": sell_quantity,
                "Buy_Price": round(buy_price, 2),
                "Sell_Price": round(price, 2),
                "Profit/loss": round(profit, 2)
            }
            if stock["Quantity"] == 0:
                stocks.remove(stock)
            break
    else:
        print("Stock not found")
        return
    with open("purchase.json", "w") as f:
        json.dump(stocks, f, indent=4)
    try:
        with open("sell.json", "r") as f:
            sell_history = json.load(f)
    except:
        sell_history = []
    found = False
    for stock in sell_history:
        if stock["Share"] == sharename:
            stock["Sell_Quantity"] += sell_quantity
            stock["Profit"] += round(profit, 2)
            stock["Sell_Price"] = round(price, 2)
            found = True
            break
    if not found:
        sell_history.append(sell_data)
    with open("sell.json", "w") as f:
        json.dump(sell_history, f, indent=4)
    print("Stock sold successfully")


def profit_loss_details(sharename):
    with open("purchase.json", "r") as f:
        stocks = json.load(f)
        price = readPrice(sharename)
    for stock in stocks:
        if stock["Share"] == sharename:

            remaining_qty = stock["Quantity"]
            current_price = price
            buy_price = stock["Avg_Price"]
            profit_loss = (current_price-buy_price) * remaining_qty
            stock["current_price"] = round(current_price, 2)
            stock["Profit_loss"] = round(profit_loss, 2)

            print("Quantity :", stock["Quantity"])
            print("stock_name :", stock["Share"])
            print("Buy_Price :", stock["Avg_Price"])
            print("Current_Price :", stock["current_price"])
            print("Profit_loss :", stock["Profit_loss"])
            return
    print("Stock not found")


def buy_quantity(sharename):
    with open("purchase.json", "r") as f:
        stocks = json.load(f)
    for stock in stocks:
        if stock["Share"] == sharename:
            print("Avalible Quantity :", stock["Quantity"])
            return stock["Quantity"]

def view_chart(sharename,start,end):
    data = yf.download(sharename,start=start,end=end) 
    return data       
