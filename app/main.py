import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MovingAverageCrossoverStrategy:
    def __init__(self, short_window: int = 20, long_window: int = 50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, prices: pd.Series) -> pd.DataFrame:
        df = pd.DataFrame(index=prices.index)
        df["price"] = prices
        df["short_ma"] = df["price"].rolling(self.short_window).mean()
        df["long_ma"] = df["price"].rolling(self.long_window).mean()
        df["signal"] = 0

        # ✅ positional slicing using .iloc
        df.iloc[self.short_window:, df.columns.get_loc("signal")] = np.where(
            df["short_ma"].iloc[self.short_window:] > df["long_ma"].iloc[self.short_window:],
            1,
            0
        )

        df["positions"] = df["signal"].diff().fillna(0)
        return df

    def backtest(self, prices: pd.Series) -> pd.DataFrame:
        df = self.generate_signals(prices)
        df["returns"] = df["price"].pct_change()
        df["strategy_returns"] = df["signal"].shift(1) * df["returns"]
        df["equity_curve"] = (1 + df["strategy_returns"]).cumprod()
        return df

    def plot_results(self, df: pd.DataFrame):
        plt.figure(figsize=(14,6))
        plt.plot(df["price"], label="Price")
        plt.plot(df["short_ma"], label=f"Short MA ({self.short_window})")
        plt.plot(df["long_ma"], label=f"Long MA ({self.long_window})")
        plt.scatter(df.index[df["positions"] == 1], df["price"][df["positions"] == 1],
                    marker="^", color="g", label="Buy")
        plt.scatter(df.index[df["positions"] == -1], df["price"][df["positions"] == -1],
                    marker="v", color="r", label="Sell")
        plt.title("Moving Average Crossover Strategy")
        plt.legend()
        plt.show()

        # Equity curve
        plt.figure(figsize=(14,4))
        plt.plot(df.index, df["equity_curve"], label="Equity Curve", color="blue")
        plt.title("Strategy Equity Curve")
        plt.legend()
        plt.show()
