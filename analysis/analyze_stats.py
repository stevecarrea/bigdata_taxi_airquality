import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from datetime import datetime
from scipy.stats import linregress
import numpy as np


# Set default formatting for plots
pd.set_option('display.mpl_style', 'default')

station = 'CCNY'
pollutant = 'Ozone'
r_value = 'R-Value-Absolute'

# NEED TO CHANGE FILE SOURCE FOR EACH STATION AND POLLUTANT
df = pd.read_csv('stats-refined/ccny_output_final_ozone_refined.csv', delimiter=',')
# slope, intercept, r, p, stderr = linregress(df['Date'], df['R-Value-Absolute'])
# N=2
# points = np.linspace(df['Date'].min(), df['R-Value-Absolute'].max(), N)
# plt.plot(points, slope*points + intercept)

df.plot(x='Date', y=r_value, style='o', legend=False, label=None)

plt.title(station+" Daily " + r_value + " for Taxi Speed vs " + pollutant)
plt.xlabel('')
plt.ylabel(r_value)
plt.show()
pylab.show(block=True)
