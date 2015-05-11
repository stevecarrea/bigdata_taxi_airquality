import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from datetime import datetime

# Set default formatting for plots
pd.set_option('display.mpl_style', 'default')

df = pd.read_csv('ccny_output_final.csv', delimiter=',')

df.plot(x='Date', y='R-Value', style='o', legend=False, label=None)

plt.title('CCNY Daily R-Values for Taxi Speed vs PM25 Acceptable')
plt.xlabel('')
plt.ylabel('R-Value')
plt.show()
pylab.show(block=True)