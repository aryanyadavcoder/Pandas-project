
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

    price = data["Close"].iloc[-1].item()

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
    data = {
        "Share": shares,
        "Date": date,
        "Quantity": quantity,
        "Avg_Price": price,
        "current_price": price,
        "Profit_loss": 0

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

            avg_price = ((old_price *old_qty) +(price* quantity))/new_qty

            profit_loss = (price-avg_price)*new_qty

            stock["Quantity"] = new_qty
            stock["Avg_Price"] = round(avg_price, 2)
            stock["current_price"] = round(price, 2)
            stock["Profit_loss"] = round(profit_loss, 2)
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

    color = ["blue","orange"]
    if profit_loss>0:
        color.append("green")
    else:
        color.append("red")
            
    x = ["Buy Price", "Current Price","Profit/loss"]
    y = [buy_price, current_price,profit_loss]
    
    
    plt.bar(x,y,color=color,label = share)
    plt.title(f"{share} Profit/Loss")
    plt.ylabel("Avg_Price")
    plt.xlabel("Current_Price")
    plt.legend()
    plt.show()