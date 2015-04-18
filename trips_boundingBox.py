import datetime
import sys
import csv
import operator
import time
from datetime import datetime
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

x = []
y = []
x1 = []
y1 = []
count = 0
speeds = {}
start_time = datetime.now()
measurements = {}
with open('/Users/Steve/GDrive/NYU_CUSP/Big_Data/project/nysdec_divisionstreet_jan2013.csv', 'r') as csvfile_air:
    reader = csv.reader(csvfile_air)
    next(reader)
    for row in reader:
        try:
            monitor_date = datetime.strptime(row[0], '%Y-%m-%d').date() # 2013-01-27
            monitor_measurement = float(row[2])
            if measurement_date not in measurements.keys():
                measurements[measurement_date] = []
            measurements[measurement_date].append(monitor_measurement)
        except:
            pass

    for date in sorted(measurements):
        x1.append(date)
        y1.append(math.ceil(reduce(lambda x, y: x + y, measurements[date]) / len(measurements[date]) * 100) / 100)


with open('/Users/Steve/GDrive/NYU_CUSP/Big_Data/project/trip_data_1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        # if count >= 5:
        #     break
        try:
            pickup_lon = float(row[10])
            pickup_lat = float(row[11])
            # pickup_date = time.strptime(row[5], "%Y-%m-%d %H:%M:%S") # 2013-01-27 11:45:00
            pickup_date = datetime.strptime(row[5][:-9], '%Y-%m-%d').date() # 2013-01-27 11:45:00
            dropoff_date = datetime.strptime(row[6][:-9], '%Y-%m-%d').date()
            dropoff_lon = float(row[12])
            dropoff_lat = float(row[13])
            trip_distance = float(row[9])
            trip_duration = float(row[8])  # seconds

            # NYC bounding box
            # if(lon >= -74.2557 and lon <= -73.6895 and lat >= 40.4957 and lat <= 40.9176):
            #     count += 1

            # Division Street bounding box
            if(pickup_lon >= -73.997271 and pickup_lon <= -73.991832 and pickup_lat >= 40.713466 and pickup_lat <= 40.715052):
                if(dropoff_lon >= -73.997271 and dropoff_lon <= -73.991832 and dropoff_lat >= 40.713466 and dropoff_lat <= 40.715052):
                    speed = ( trip_distance / trip_duration ) * 3600
                    if speed > 0 and speed < 100:
                        if pickup_date not in speeds.keys():
                            speeds[pickup_date] = []
                        speeds[pickup_date].append(speed)

                        print 'Date: ', pickup_date, 'Speed: ', round(speed, 2)
                        count += 1
        except:
            pass

print 'Count: ', count
for date in sorted(speeds):
    x.append(date)
    y.append(math.ceil(reduce(lambda x, y: x + y, speeds[date]) / len(speeds[date]) * 100) / 100)

    print 'Date: ', date, '| Average Speed: ', math.ceil(reduce(lambda x, y: x + y, speeds[date]) / len(speeds[date]) * 100) / 100, '| Number of Taxis: ', len(speeds[date])


c = datetime.now() - start_time
print 'It took', divmod(c.days * 86400 + c.seconds, 60), '(minutes, seconds).'

plt.plot(x, y)
plt.plot(x1, y1)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()
plt.title('Average Taxi Speed vs Air Quality Measurements')
plt.ylabel('Average Taxi Speed')
plt.grid()
plt.show()

# comment