import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Basic moving average crossover strategy
class MovingAverageCrossover:
    def __init__(self, symbol, short_window=20, long_window=50):
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.data = None

    def download_data(self, start="2020-01-01", end="2024-01-01"):
        self.data = yf.download(self.symbol, start=start, end=end)
        self.data["Short_MA"] = self.data["Close"].rolling(self.short_window).mean()
        self.data["Long_MA"] = self.data["Close"].rolling(self.long_window).mean()

    def generate_signals(self):
        self.data["Signal"] = 0
        self.data["Signal"][self.short_window:] = (
            self.data["Short_MA"][self.short_window:] > self.data["Long_MA"][self.short_window:]
        ).astype(int)
        self.data["Position"] = self.data["Signal"].diff()

    def plot_signals(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data["Close"], label="Price", alpha=0.6)
        plt.plot(self.data["Short_MA"], label="Short MA")
        plt.plot(self.data["Long_MA"], label="Long MA")
        plt.plot(self.data[self.data["Position"] == 1.0].index,
                 self.data["Short_MA"][self.data["Position"] == 1.0],
                 "^", markersize=10, color="g", label="Buy")
        plt.plot(self.data[self.data["Position"] == -1.0].index,
                 self.data["Short_MA"][self.data["Position"] == -1.0],
                 "v", markersize=10, color="r", label="Sell")
        plt.title(f"{self.symbol} - MA Crossover Strategy")
        plt.legend()
        plt.grid()

# Run the script
if __name__ == "__main__":
    mac = MovingAverageCrossover("AAPL")
    mac.download_data()
    mac.generate_signals()
    mac.plot_signals()
    plt.show()