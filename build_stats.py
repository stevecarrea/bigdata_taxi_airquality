import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from datetime import datetime
from scipy.stats import linregress
import numpy as np

# Parse dates into datetime objects
def parse_date(raw_date):
    return datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S')

# Print full data frame
def print_full(df):
    pd.set_option('display.max_rows', len(df))
    print(df)
    pd.reset_option('display.max_rows')

# Plot average speed per hour for each monitor for entire time period to see variability
def plot_avgSpeed():

    for monitor in air_monitors:
        df_monitor = df[df['Location'] == monitor]['Average_Speed']
        df_monitor.plot(style = 'o', title = monitor)
        plt.show()

# Get slope and r-squared value for each day of the best fit line b/w avg speed and pollutant
output = []
def daily_stats(df):  
    # CCNY 
    df_ccny = df[df['Location'] == 'CCNY']
    for i, group in df_ccny.groupby(df_ccny['Time'].dt.date):
        monitor = 'CCNY'
        pollutant = 'PM25_Acceptable'
        
        # get slope, intercept, and r-value
        slope, intercept, r, p, stderr = linregress(group['Average_Speed'], group[pollutant])
        print i, slope, r
        output.append((i, slope, r))
        # plot and draw best fit line
        group.plot(x='Average_Speed', y=pollutant, style = 'o', title=monitor+": "+pollutant+" "+str(i))
        N=2
        points = np.linspace(group['Average_Speed'].min(), group[pollutant].max(), N)
        #plt.plot(points, slope*points + intercept)
        #plt.savefig('plots/plot'+str(monitor)+str(pollutant)+'_'+str(i)+'.png') 

    with open('output_final.csv', "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in output:
                writer.writerow(line)

# Plot number of taxis per hour for each monitor for entire time period to see density over time
def plot_density(x):
    pass

air_monitors = { 'CCNY': ('PM25_Acceptable', 'PM25_Raw', 'CO', 'Ozone'),
                 'PS19': ('PM25_Acceptable', 'PM25_Raw'),
                 'DivisionStreet': ('PM25_Acceptable', 'PM25_Raw') }

# Read file output from MapReduce, comma-separated
# Headers as: Location,Time,Number_Taxis,Average_Speed,PM25_Acceptable,Ozone,CO,PM25_Raw,Sky_Condition,Relative_Humidity,Wind_Speed,Wind_Direction
df = pd.read_csv('part-00000', delimiter=',')

# Convert raw dates to datetime objects
df['Time'] = df['Time'].map(parse_date)

#print df
#print_full(df)
#plot_avgSpeed()
#daily_stats(df)

daily_stats(df)




