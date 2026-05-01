import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

def get_a_and_b(x, y):
    n = len(x)
    x = np.array(x)
    y = np.array(y)
    sigmax, sigmay = np.sum(x), np.sum(y)
    sigmaxy, sigmax2 = np.sum(x * y), np.sum(x * x)

    b = (n * sigmaxy - sigmax * sigmay) / (n * sigmax2 - sigmax**2)
    a = (sigmay - b * sigmax) / n
    return a, b


sharename = input("Enter stock name :")
Start = input("Enter Start date :")
End = input("Enter the End :")

data = yf.download(sharename, start=Start, end=End)
print(data)

x = data["Close"]
n = len(x)
print(n)

y = data["Volume"]

x = [i + 1 for i in range(n)]

a, b = get_a_and_b(x, y)
print(a, b)

py = [a + b * i for i in x]

plt.plot(x, py)
plt.plot(x, y)
plt.scatter(x, y)

plt.title("Sales Data with Regression Line")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.show()