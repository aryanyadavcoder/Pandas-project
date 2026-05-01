""" Equation 1:  sigmay=n x a + b X sigmax
Equation 2: sigmaxy = a x sigmax + b x sigmax2
 Solution for a and b
 Eq 1 x sigmax: sigmax x sigmay = n x a x sigmax + b x sigmax x sigmax
 
 Eq 2 x n: n x sigmaxy = n x a x sigmax + n x b x sigmax2
Eq 3 = Eq 1-Eq 2=  sigmax x sigmay = n x a x sigmax + b x sigmax x sigmax  -  (n x a x sigmax + n x b x sigmax2)
Eq 3:  sigmax x sigmay-n x sigmaxy = n x a x sigmax - n x a x sigmax + b x sigmax x sigmax - n x b x sigmax2
Eq 4: sigmax x sigmay-n x sigmaxy=b x sigmax x sigmax - n x b x sigmax2

Eq 5: b =(sigmax x sigmay-n x sigmaxy)/(  sigmax x sigmax - n   x sigmax2)


Equation 1:  sigmay=n x a + b X sigmax
Substitute value of b from Eq 5
sigmay= n x a + ((sigmax x sigmay-n x sigmaxy)/(  sigmax x sigmax - n   x sigmax2)) x sigmax

a= sigmay - (((sigmax x sigmay-n x sigmaxy)/(  sigmax x sigmax - n   x sigmax2)) x sigmax) / n
"""
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import pandas as pd

def getAandB(sigmax, sigmay, sigmaxy, sigmax2, n):
    b = (n * sigmaxy - sigmax * sigmay) / (n * sigmax2 - sigmax * sigmax)
    a = (sigmay - b * sigmax) / n
    return a, b

def calculateAllSigma(x, y):
    sigmax, sigmay, sigmaxy, sigmax2,sigmay2 = 0, 0, 0, 0,0
    n = len(x)
    for i in range(n):
        sigmax += x[i]
        sigmay += y[i]
        sigmaxy += x[i] * y[i]
        sigmax2 += x[i] * x[i]
        sigmay2 += y[i] * y[i]
    return sigmax, sigmay, sigmaxy, sigmax2,sigmay2

def findCorrelation(sigmax, sigmay, sigmaxy, sigmax2, sigmay2, n):
    numerator = n * sigmaxy - sigmax * sigmay
    denominator = ((n * sigmax2 - sigmax**2) * (n * sigmay2 - sigmay**2)) ** 0.5
    r = numerator / denominator
    return r

def line(x, a, b):
    return a + b * x

data = pd.read_csv("sales_data.csv")

x = data["Month"]
y = data["Sales"]
sx, sy, sxy, sx2,sy2 = calculateAllSigma(x, y)

n = len(x)
a, b = getAandB(sx, sy, sxy, sx2, n)
r  = findCorrelation(sx,sy,sxy,sx2,sy2,n)
print(f"a = {a}, b = {b}")
print(f"correlation (r) = {r}")
predictedY = [line(i, a, b) for i in x]
plt.plot(x, y)
plt.plot(x, predictedY)
plt.xlabel("Days")
plt.ylabel("Price")
plt.title("Linear Regression on TCS Stock")
plt.show()