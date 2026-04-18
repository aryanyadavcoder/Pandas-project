import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def getAandB(sigmax, sigmay, sigmaxy, sigmax2, n):
    b = (n * sigmaxy - sigmax * sigmay) / (n * sigmax2 - sigmax * sigmax)
    a = (sigmay - b * sigmax) / n
    return a, b

def calculateAllSigma(x, y):
    sigmax, sigmay, sigmaxy, sigmax2, sigmay2 = 0, 0, 0, 0, 0
    n = len(x)
    for i in range(n):
        sigmax += x[i]
        sigmay += y[i]
        sigmaxy += x[i] * y[i]
        sigmax2 += x[i] * x[i]
        sigmay2 += y[i] * y[i]
    return sigmax, sigmay, sigmaxy, sigmax2, sigmay2

def findCorrelation(sigmax, sigmay, sigmaxy, sigmax2, sigmay2, n):
    numerator = n * sigmaxy - sigmax * sigmay
    denominator = ((n * sigmax2 - sigmax**2) * (n * sigmay2 - sigmay**2)) ** 0.5
    return numerator / denominator

def line(x, a, b):
    return a + b * x

dates = pd.date_range(start="2025-01-01", end="2025-12-31")

np.random.seed(0)
sales = np.random.randint(200, 500, size=len(dates))

data = {
    "Date": dates,
    "Sales": sales
}

df = pd.DataFrame(data)

y = df["Sales"].values
x = np.arange(len(y))

sx, sy, sxy, sx2, sy2 = calculateAllSigma(x, y)

n = len(x)
a, b = getAandB(sx, sy, sxy, sx2, n)
r = findCorrelation(sx, sy, sxy, sx2, sy2, n)

print(f"a = {a}, b = {b}")
print(f"correlation (r) = {r}")

predictedY = [line(i, a, b) for i in x]

plt.plot(x, y, marker='o', label="Actual Sales")
plt.plot(x, predictedY, linestyle='--', label="Regression Line")
plt.xlabel("Days")
plt.ylabel("Sales")
plt.legend()
plt.title("Linear Regression on Sales Data")
plt.show()