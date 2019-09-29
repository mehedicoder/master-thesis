import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data_top.csv', header=None, index_col= 0)
data.plot(kind='bar')
plt.xlabel('keywords')
plt.ylabel('Counts')
plt.title('Top 20 Keywords vs Tweet counts')
plt.subplots_adjust(bottom=0.5)
plt.axhline(49, color='r', linestyle='dashed', linewidth=1)
plt.text(21, 55, "Average counts = 49", ha='right', va = 'center')
plt.show()