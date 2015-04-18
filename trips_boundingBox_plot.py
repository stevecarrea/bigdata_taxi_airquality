import sys
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

#file = sys.argv[1]
file = '/Users/Steve/GDrive/NYU_CUSP/Big_Data/project/trip_data_1.csv'

trips_data = open(file)
reader = csv.reader(trips_data)
next(reader)

x = []
y = []
for row in reader:

    try:
        pickup_lon = float(row[10])
        pickup_lat = float(row[11])
        pickup_date = datetime.strptime(row[5][:-9], '%Y-%m-%d').date()
        dropoff_lon = float(row[12])
        dropoff_lat = float(row[13])
        dropoff_date = datetime.strptime(row[6][:-9], '%Y-%m-%d').date()
        trip_distance = float(row[9])
        trip_duration = float(row[8])  # seconds




        # Division Street bounding box
        if(pickup_lon >= -73.997271 and pickup_lon <= -73.991832 and pickup_lat >= 40.713466 and pickup_lat <= 40.715052):

            if(dropoff_lon >= -73.997271 and dropoff_lon <= -73.991832 and dropoff_lat >= 40.713466 and dropoff_lat <= 40.715052):
                speed = ( trip_distance / trip_duration ) * 3600
                if speed > 0 and speed <= 50:
                    #print 'Date: ', pickup_date, 'Speed: ', round(speed, 2)
                    x.append(pickup_date)
                    y.append(speed)
                    plt.plot(x, y, 'bo-')
    except:
        pass


plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()
plt.title('Average Taxi Speed vs Air Quality Measurements')
plt.ylabel('Average Taxi Speed')
plt.grid()
plt.show()