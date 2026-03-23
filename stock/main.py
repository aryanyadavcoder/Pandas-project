
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
    plt.title(sharename +" Chart")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()
    
    
def purchase(shares, date, quantity):

    price = readPrice(shares)

    data = {
        "Share": shares,
        "Date": date,
        "Quantity": quantity,
        "Price": price
    }

    try:
        with open("purchase.json", "r") as f:
            purchase = json.load(f)
    except:
        purchase = []

    found = False

    for item in purchase:
        if item["Share"] == shares:

            old_qty = item["Quantity"]
            old_price = item["Price"]

            new_qty = old_qty + quantity

            avg_price = ((old_price * old_qty) + (price * quantity)) / new_qty

            item["Quantity"] = new_qty
            item["Price"] = avg_price

            found = True
            break

    if not found:
        purchase.append(data)

    with open("purchase.json", "w") as f:
        json.dump(purchase, f, indent=4)

    print("stock purchase save")

