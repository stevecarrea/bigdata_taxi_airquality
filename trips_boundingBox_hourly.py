import csv
from datetime import datetime
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

x = []
y = []
x_air = []
y_air = []
count = 0
speeds = {}
start_time = datetime.now()
measurements = {}
with open('/Users/Steve/Github/bigdata_taxi_airquality/data/nysdec_queenscollege_2013.01_NOx.csv', 'r') as csvfile_air:
    reader = csv.reader(csvfile_air)
    next(reader)
    for row in reader:
        try:
            date_time = row[0]+' '+row[1]
            measurement_date = datetime.strptime(date_time, '%Y-%m-%d %H:%M')  # 2013-01-27
            monitor_measurement = float(row[4])  # NOx
            if measurement_date not in measurements.keys():
                measurements[measurement_date] = []
            measurements[measurement_date].append(monitor_measurement)
        except:
            pass

    for date in sorted(measurements):
        x_air.append(date)
        y_air.append(measurements[date])

with open('/Users/Steve/Github/bigdata_taxi_airquality/data/trip_data_1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        # if count >= 5:  # for testing
        #     break
        try:
            count += 1
            pickup_lon = float(row[10])
            pickup_lat = float(row[11])
            pickup_date = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')  # 2013-01-27 11:45:00
            dropoff_date = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
            dropoff_lon = float(row[12])
            dropoff_lat = float(row[13])
            trip_distance = float(row[9])
            trip_duration = float(row[8])  # seconds
            # NYC bounding box
            # if(lon >= -74.2557 and lon <= -73.6895 and lat >= 40.4957 and lat <= 40.9176):
            #     count += 1

            # Division Street bounding box
            # Southwest coordinate: 40.713221, -73.998166
            # Northeast coordinate: 40.715319, -73.993370

            # Queens College bounding box
            # Southwest coordinate: 40.726365, -73.837724
            # Northwest coordinate: 40.743795, -73.812404
            if(pickup_lon >= -73.837724 and pickup_lon <= -73.812404 and pickup_lat >= 40.726365 and pickup_lat <= 40.743795) or \
                (dropoff_lon >= -73.837724 and dropoff_lon <= -73.812404 and dropoff_lat >= 40.726365 and dropoff_lat <= 40.743795):
                    if trip_distance < 1.5:
                        speed = ( trip_distance / trip_duration ) * 3600
                        if speed > 0 and speed < 50:

                            x.append(pickup_date)
                            y.append(speed)

                            print 'Date: ', pickup_date, 'Speed: ', round(speed, 2)
                            count += 1
        except:
            pass
print 'Count: ', count

c = datetime.now() - start_time
print 'It took', divmod(c.days * 86400 + c.seconds, 60), '(minutes, seconds).'

fig = plt.figure()
ax1 = fig.add_subplot(211)
plt.plot(x, y, 'bo-', color='r', label='Avg Speed')
plt.title('Average Taxi Speed vs Air Quality Measurements')
plt.gca().set_ylim([0, 50])
plt.ylabel('Average Taxi Speed')
ax1.grid(b=True, which='major')
ax1.grid(b=True, which='minor')

ax2 = fig.add_subplot(212, sharex=ax1)
plt.plot(x_air, y_air, 'bo-', color='b', label='NOx')

plt.setp(ax1.get_xticklabels(), visible=False)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
plt.gcf().autofmt_xdate()
plt.gca().set_ylim([0, 250])
plt.ylabel('NOx')
ax2.grid(b=True, which='major')
ax2.grid(b=True, which='minor')


plt.show()