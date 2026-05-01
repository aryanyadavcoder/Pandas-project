import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

def get_a_and_b(x,y):
    n = len(x)
    x = np.array(x)
    y = np.array(y)
    sx,sy = np.sum(x),np.sum(y)
    sxy,sx2 = np.sum(x*y),np.sum(x*x)
    b = (n*sxy- sx * sy) / (n*sx2-sx**2)
    a = (sy - b* sx)/n
    return a,b 

share = input("Enter first stock name : ")
share1 = input("Enter second stock name : ")
Start = input("Enter start date (YYYY-MM-DD): ")
End = input("Enter end date (YYYY-MM-DD): ")

data1 = yf.download(share,start=Start,end=End)
data2 = yf.download(share1,start=Start,end=End)

# Safety check
if data1.empty or data2.empty:
    print("❌ Invalid stock name or date")
    exit()

# Safe merge
close1 = data1["Close"]
close2 = data2["Close"]

data = pd.concat([close1, close2], axis=1)
data.columns = ["stock1", "stock2"]
data = data.dropna()

if data.empty:
    print("❌ No overlapping data")
    exit()

# Arrays
y1 = data["stock1"].values
y2 = data["stock2"].values
x = np.arange(1, len(y1)+1)

# Regression
a1,b1 = get_a_and_b(x,y1)
a2,b2 = get_a_and_b(x,y2)

correlation = np.corrcoef(y1, y2)[0,1]
print("Stock 1 regression :",a1,b1)
print("Stock 2 regression :",a2,b2)
print("Stock vs Stock correlation :",correlation)

# Plot
plt.scatter(x, y1, s=10, label="Stock 1 Data")
plt.scatter(x, y2, s=10, label="Stock 2 Data")

plt.plot(x, a1 + b1*np.array(x), color='red', label="Stock 1 Regression")
plt.plot(x, a2 + b2*np.array(x), color='green', label="Stock 2 Regression")

plt.xlabel("Time")
plt.ylabel("Price")
plt.title("Stock Comparison")

plt.legend()
plt.show()