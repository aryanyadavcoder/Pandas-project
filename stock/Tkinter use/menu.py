import yfinance as yf
import main as sn
import json
from datetime import date


with open("stock/stock.json", "r") as f:
    shares = json.load(f)


while True:
    print("<---menu--->")
    print("0-Exit,1-Buy,2-sell,3-View current price and chart,4-Profit_loss_chart,5-show all buy & sell details,6-view chart")
    option = int(input("Enter option\n"))
    if option == 0:
        print("Exit")
        exit()

    elif option == 1:
        print("<---Menu--->")
        for key, value in shares.items():
            print(key, value)
        n = int(input("Enter stock number :"))
        sharename = shares[str(n)]
        buy_date = str(date.today())
        prices = sn.readPrice(sharename)
        print("latest close price :", prices)

        quantity = int(input("Enter quantity :"))
        sn.purchase(sharename, buy_date, quantity)
        break

    elif option == 2:
        print("<---menu--->")
        for key, value in shares.items():
            print(key,value)
        n = int(input("Enter stock number :"))
        sharename = shares[str(n)]
        sell_date = str(date.today())
        sn.buy_quantity(sharename)
        sell_quantity = int(input("Enter sell quantity :"))           
        sn.sell(sharename, sell_quantity) 
        break
        

    elif option == 3:
        print("<---Menu--->")
        for key, value in shares.items():
            print(key, value)
        n = int(input("Enter number\n"))
        sharename = shares[str(n)]
        prices = sn.readPrice(sharename)
        print("latest close price :", prices)
        data = sn.onedaychart(sharename)
        sn.plotgraph(data, sharename)
        break

    elif option == 4:
        print("Chart")
        print("<---Menu--->")
        for key, value in shares.items():
            print(key, value)
        n = int(input("Enter number\n"))
        stock = shares[str(n)]
        sn.profit_loss_chart(stock)
        break
    
    elif option == 5:
        print("<---Menu--->")
        for key, value in shares.items():
            print(key, value)
        n = int(input("Enter number\n"))
        sharename = shares[str(n)]
        sn.profit_loss_details(sharename)
        break
    
    elif option == 6:
        print("<---Menu--->")
        for key, value in shares.items():
            print(key, value)
        n = int(input("Enter number\n"))
        sharename = shares[str(n)]
        start = input("Enter start date :")
        end = input("Enter end date :")
        data = sn.view_chart(sharename,start,end)
        sn.plotgraph(data,sharename)
        
    # elif option == 7:
    else:
        print("Invalid option")
