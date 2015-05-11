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

def clean_averages(x):
    try:
        if x != 'nan':
            return float(x)
        else:
            pass
    except:
        pass

# Get slope and r-squared value for each day of the best fit line b/w avg speed and pollutant
output = []
def daily_stats(df):  
    # CCNY 
    df_ccny = df[df['Location'] == 'PS19']

    # df_ccny = df

    for i, group in df_ccny.groupby(df_ccny['Time'].dt.date):
        try:
            monitor = 'PS19'
            pollutant = 'PM25_Acceptable'
            
            wind_speed = np.mean(group['Wind_Speed'].apply(lambda x: clean_averages(x)).values)
            relative_humidity = np.mean(group['Relative_Humidity'])
            # wind_direction = np.mean(group['Wind_Direction'].apply(lambda x: clean_averages(x)).values)

            # get slope, intercept, and r-value

            slope, intercept, r, p, stderr = linregress(group['Average_Speed'], group[pollutant])
            print i, slope, r, wind_speed, relative_humidity
            output.append((i, slope, r, wind_speed, relative_humidity))
            
            # plot and draw best fit line
            group.plot(x='Average_Speed', y=pollutant, style = 'o', title=monitor+": "+pollutant+" "+str(i))
            N=2
            points = np.linspace(group['Average_Speed'].min(), group[pollutant].max(), N)
            plt.plot(points, slope*points + intercept)
            #plt.savefig('plots-ccny/plot'+str(monitor)+str(pollutant)+'_'+str(i)+'.png') 
        except:
            pass

    with open('ps19_output_final_pm25.csv', "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["Date", "Slope", "R-Value", "Wind Speed", "Relative Humidity"])
            for line in output:
                writer.writerow(line)

    # # PS19 
    # df_ps19 = df[df['Location'] == 'PS19']
    # for i, group in df_ps19.groupby(df_ps19['Time'].dt.date):
    #     monitor = 'PS19'
    #     pollutant = 'PM25_Acceptable'
        
    #     # get slope, intercept, and r-value
    #     slope, intercept, r, p, stderr = linregress(group['Average_Speed'], group[pollutant])
    #     print i, slope, r
    #     output.append((i, slope, r))
    #     # plot and draw best fit line
    #     group.plot(x='Average_Speed', y=pollutant, style = 'o', title=monitor+": "+pollutant+" "+str(i))
    #     N=2
    #     points = np.linspace(group['Average_Speed'].min(), group[pollutant].max(), N)
    #     #plt.plot(points, slope*points + intercept)
    #     #plt.savefig('plots-ps19/plot'+str(monitor)+str(pollutant)+'_'+str(i)+'.png') 

    # with open('ps19_output_final.csv', "wb") as csv_file:
    #         writer = csv.writer(csv_file, delimiter=',')
    #         writer.writerow(["Date", "Slope", "R-Value"])
    #         for line in output:
    #             writer.writerow(line)

    # # DivisionStreet 
    # df_divisionStreet = df[df['Location'] == 'DivisionStreet']
    # for i, group in df_divisionStreet.groupby(df_divisionStreet['Time'].dt.date):
    #     monitor = 'DivisionStreet'
    #     pollutant = 'PM25_Acceptable'
        
    #     # get slope, intercept, and r-value
    #     slope, intercept, r, p, stderr = linregress(group['Average_Speed'], group[pollutant])
    #     print i, slope, r
    #     output.append((i, slope, r))
    #     # plot and draw best fit line
    #     group.plot(x='Average_Speed', y=pollutant, style = 'o', title=monitor+": "+pollutant+" "+str(i))
    #     N=2
    #     points = np.linspace(group['Average_Speed'].min(), group[pollutant].max(), N)
    #     #plt.plot(points, slope*points + intercept)
    #     #plt.savefig('plots-divisionStreet/plot'+str(monitor)+str(pollutant)+'_'+str(i)+'.png') 

    # with open('divisionStreet_output_final.csv', "wb") as csv_file:
    #         writer = csv.writer(csv_file, delimiter=',')
    #         writer.writerow(["Date", "Slope", "R-Value"])
    #         for line in output:
    #             writer.writerow(line)

# Plot number of taxis per hour for each monitor for entire time period to see density over time
def plot_density(x):
    pass

air_monitors = { 'CCNY': ('PM25_Acceptable', 'PM25_Raw', 'CO', 'Ozone'),
                 'PS19': ('PM25_Acceptable', 'PM25_Raw'),
                 'DivisionStreet': ('PM25_Acceptable', 'PM25_Raw') }

# Read file output from MapReduce, comma-separated
# Headers as: Location,Time,Number_Taxis,Average_Speed,PM25_Acceptable,Ozone,CO,PM25_Raw,Sky_Condition,Relative_Humidity,Wind_Speed,Wind_Direction
df = pd.read_csv('part-00000.csv', delimiter=',')

# Convert raw dates to datetime objects
df['Time'] = df['Time'].map(parse_date)

#print df
#print_full(df)
#plot_avgSpeed()
#daily_stats(df)

daily_stats(df)




