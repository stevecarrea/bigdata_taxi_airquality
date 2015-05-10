import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from datetime import datetime

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
def daily_stats(df):  

    df_CCNY = df[(df.Location == 'CCNY')]  # Subset dataframe for specific monitor location
    for pollutant in air_monitors['CCNY']:
        for i in xrange(0, len(air_monitors['CCNY'])):     
            df.groupby(df['Time'].dt.day).plot(x='Average_Speed', y=air_monitors['CCNY'][i], style = 'o', title='CCNY'+": "+air_monitors['CCNY'][i]+" "+str(i))
            plt.savefig('plots/plot'+str('CCNY_')+str(air_monitors['CCNY'][i])+'_'+str(i)+'.png') 

    df_PS19 = df[(df.Location == 'PS19')]
    for pollutant in air_monitors['PS19']:
        for i in xrange(0, len(air_monitors['PS19'])):     
            df.groupby(df['Time'].dt.day).plot(x='Average_Speed', y=air_monitors['PS19'][i], style = 'o', title='PS19'+": "+air_monitors['PS19'][i]+" "+str(i))
            plt.savefig('plots/plot'+str('PS19_')+str(air_monitors['PS19'][i])+'_'+str(i)+'.png') 

    df_DivisionStreet = df[(df.Location == 'DivisionStreet')]
    for pollutant in air_monitors['DivisionStreet']:
        for i in xrange(0, len(air_monitors['DivisionStreet'])):     
            df.groupby(df['Time'].dt.day).plot(x='Average_Speed', y=air_monitors['DivisionStreet'][i], style = 'o', title='DivisionStreet'+": "+air_monitors['DivisionStreet'][i]+" "+str(i))
            plt.savefig('plots/plot'+str('DivisionStreet_')+str(air_monitors['DivisionStreet'][i])+'_'+str(i)+'.png') 


# Plot number of taxis per hour for each monitor for entire time period to see density over time
def plot_density(x):
    pass



air_monitors = { 'CCNY': ('PM25_Acceptable', 'PM25_Raw', 'CO', 'Ozone'),
                 'PS19': ('PM25_Acceptable', 'PM25_Raw'),
                 'DivisionStreet': ('PM25_Acceptable', 'PM25_Raw') }

# Headers as: Location,Time,Number_Taxis,Average_Speed,PM25_Acceptable,Ozone,CO,PM25_Raw,Sky_Condition,Relative_Humidity,Wind_Speed,Wind_Direction

# Read file output from MapReduce, comma-separated
df = pd.read_csv('part-00000', delimiter=',')

# Convert raw dates to datetime objects
df['Time'] = df['Time'].map(parse_date)

#print df
#print_full(df)
#plot_avgSpeed()
daily_stats(df)



