import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os


siemens_data = os.path.join(os.path.dirname(__file__), 'SIEGY.csv')
df = pd.read_csv(siemens_data)

df = df.set_index(pd.DatetimeIndex(df['Date'].values))


'''Price difference from the previous day'''

price_difference = df['Adj Close'].diff(1).dropna()

up = price_difference.copy()
up[up<0] = 0

down = price_difference.copy()
down[down>0] = 0

average_gain = up.rolling(window=14).mean()
average_loss = abs(down.rolling(window=14).mean())

'''Calculate RSI:'''

RS = average_gain / average_loss
RSI = 100 - (100 / (1 + RS))

results = pd.DataFrame()
results['Adj Close'] = df['Adj Close']
results['RSI'] = RSI

plt.style.use('seaborn')

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

ax1.plot(results.index, results['Adj Close'], label = 'Siemens Adj. Close Price')

ax2.plot(results.index, results['RSI'], label = 'Siemens Adj. Close Price')
ax2.axhline(10, alpha = 0.6, color='red')
ax2.axhline(20, alpha = 0.4, color='red')
ax2.axhline(30, alpha = 0.2, color='red')
ax2.axhline(70, alpha = 0.2, color='green')
ax2.axhline(80, alpha = 0.4, color='green')
ax2.axhline(90, alpha = 0.6, color='green')


ax1.set_title('Siemens Price History')
ax2.set_title('RSI')

ax1.set_ylabel('Price in USD')

plt.show()


'''
under 20 - stock was oversold
over 80 - stock was overbought
'''




