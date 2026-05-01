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

# a, b = get_a_and_b(x, y)

# print("Intercept (a):", a)
# print("Slope (b):", b)

# y_pred = a + b * x

# plt.scatter(x, y, label="Actual Data")

sharename = input("Enter stock name :")
Start = input("Enter Start date :")
End = input("Enter the End :")

data = yf.download(sharename, start=Start, end=End)
print(data)

y = data["Close"].values.flatten()
n = len(y)
print(n)

x = [i + 1 for i in range(n)]
a, b = get_a_and_b(x, y)
print("Regression :",a, b)
py = [a + b * i for i in x]

r = np.corrcoef(x,y)[0,1]
print("Corrilation :",r)

plt.plot(x, py,label = "Regression")
plt.plot(x, y,label = "Actual Data")
plt.scatter(x, y)

plt.title("Sales Data with Regression Line")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.legend()

plt.show()