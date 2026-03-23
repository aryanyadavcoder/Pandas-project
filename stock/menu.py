import yfinance as yf
import main as sn
import json
from datetime import date


with open("stock/stock.json","r") as f:
    shares = json.load(f)


while True:
    print("<---menu--->")
    print("0-Exit,1-Buy,2-Sell,3-View current price,4-chart")
    option = int(input("Enter option\n"))
    if option == 0:
        print("Exit")
        exit()
        
        
    elif option == 1:
        print("<---Menu--->")
        for key,value in shares.items():
            print(key,value)
        n = int(input("Enter stock number :"))
        sharename = shares[str(n)]
        buy_date =str(date.today())
        prices = sn.readPrice(sharename)
        print("latest close price :", prices)
        
        
        
        quantity = int(input("Enter quantity :"))
        sn.purchase(sharename, buy_date, quantity)


    elif option == 2:
        print("Sell")
        continue


    elif option == 3:
        print("<---Menu--->")
        for key,value in shares.items():
            print(key,value)
        n = int(input("Enter number\n"))
        sharename = shares[str(n)]

        prices = sn.readPrice(sharename)
        print("latest close price :", prices)
        data = sn.onedaychart(sharename)

        sn.plotgraph(data, sharename)

        continue
    
    
    elif option == 4:
        print("Chart")
        print("<---Menu--->")
        for key,value in shares.items():
            print(key,value)
        n = int(input("Enter number\n"))
        stock = shares[str(n)]

        start = input("Enter start date :")
        end = input("Enter end date :")
        data = yf.download(stock, start, end)
        sn.plotgraph(data, stock)
        continue
    else:
        print("Invalid option")
