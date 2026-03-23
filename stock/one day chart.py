import yfinance as yf
import matplotlib.pyplot as plt

stock = "RELIANCE.NS"

# 1 Day intraday data (1 minute interval)
data = yf.download(stock, period="1d", interval="1m")

# Current price (latest close)
current_price = data["Close"].iloc[-1]

print("Current Price :", current_price)

# Chart
plt.plot(data["Close"])
plt.title(stock + " 1 Day Chart")
plt.xlabel("Time")
plt.ylabel("Price")
plt.show()