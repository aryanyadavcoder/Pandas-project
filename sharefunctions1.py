import yfinance as yf
import json
import pandas as pd
import matplotlib.pyplot as plt


def saveToJson(filename, data):
    filename = filename + ".json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    return True


def readFromJson(filename):
    filename = filename + ".json"
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def downloadShareData(sharename, startdate, enddate):
    data = yf.download(sharename, start=startdate, end=enddate)
    data.to_csv(sharename + ".csv")
    return data


def getSharePrice(sharename):
    data = yf.download("RELIANCE.NS", period="1d")
    print(data["Close"])
    
def plotgraph(data, sharename):
    plt.plot(data["Open"], linestyle="--")
    plt.plot(data["Close"], linestyle="--")

    plt.title(sharename)
    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.legend(["Open", "Close"])
    plt.show()
    




