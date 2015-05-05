import csv
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

x = []
y_date = []
y_speed = []
y_air = []
count = 0
speeds = {}
start_time = datetime.now()
measurements = {}

with open('/Users/brunomacedo/Desktop/NYU-Poly/3rd-Semester/Big-Data/project/nysdec_queenscollege_jan2013_NOx.csv', 'r') as csvfile_air:
    reader = csv.reader(csvfile_air)
    next(reader)
    for row in reader:
        try:
            date_time = row[0]+' '+row[1][:-3]
            measurement_date = datetime.strptime(date_time, '%Y-%m-%d %H')  # 2013-01-27
            monitor_measurement = float(row[2])  # PM2.5
            if measurement_date not in measurements:
                measurements[measurement_date] = []
            measurements[measurement_date].append(monitor_measurement)
            print 'Date: ', measurement_date, 'NOx: ', monitor_measurement
        except:
            pass

with open('/Users/brunomacedo/Desktop/NYU-Poly/3rd-Semester/Big-Data/project/trip_data_1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        # if count >= 50:  # for testing
        #     break
        try:
            pickup_lon = float(row[10])
            pickup_lat = float(row[11])
            pickup_date = datetime.strptime(row[5][:-6], '%Y-%m-%d %H')  # 2013-01-27 11:45:00
            dropoff_date = datetime.strptime(row[6][:-6], '%Y-%m-%d %H')
            dropoff_lon = float(row[12])
            dropoff_lat = float(row[13])
            trip_distance = float(row[9])
            trip_duration = float(row[8])  # seconds

            # Division Street bounding box
            # Southwest coordinate: 40.713221, -73.998166
            # Northeast coordinate: 40.715319, -73.993370

            # Queens College bounding box
            # Southwest coordinate: 40.726365, -73.837724
            # Northwest coordinate: 40.743795, -73.812404
            if(pickup_lon >= -73.998166 and pickup_lon <= -73.993370 and pickup_lat >= 40.713221 and pickup_lat <= 40.715319) or \
                (dropoff_lon >= -73.998166 and dropoff_lon <= -73.993370 and dropoff_lat >= 40.713221 and dropoff_lat <= 40.715319):
                    if trip_distance < 1.5:
                        speed = ( trip_distance / trip_duration ) * 3600
                        if speed > 0 and speed < 50:
                            if pickup_date not in measurements:
                                print 'Missing data for: ', pickup_date
                                pass
                            else:
                                if len(measurements[pickup_date]) == 1:
                                    measurements[pickup_date].append([])
                                measurements[pickup_date][1].append(speed)
                                print 'Date: ', pickup_date, 'Speed: ', round(speed, 2)
                                count += 1
        except:
            pass
print 'Count: ', count

stats_daily = {}
previous_hour = None
for hour in sorted(measurements.keys()):
    if len(measurements[hour]) > 1 and measurements[hour][0] < 200:  # only dates with air measurement < 200 and avg speed present
        # take avg of all speeds in the array after air measurement within dictionary for each hour

        if hour.strftime('%Y-%m-%d') == previous_hour or previous_hour == None:

            avg_speed = math.ceil(reduce(lambda x, y: x + y, measurements[hour][1]) / len(measurements[hour][1]) * 100) / 100
            print 'Hour: ', hour, 'Average Speed: ', round(avg_speed, 2)

            y_speed.append(avg_speed)  # append avg speed for hour
            y_air.append(measurements[hour][0])


        else:


            # calculate stats
            par = np.polyfit(y_speed, y_air, 1, full=True)
            slope=par[0][0]
            intercept=par[0][1]
            xd = y_speed
            yd = y_air
            xl = [min(xd), max(xd)]
            yl = [slope*xx + intercept  for xx in xl]
            # coefficient of determination, plot text
            variance = np.var(yd)
            residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)])
            Rsqr = np.round(1-residuals/variance, decimals=2)
            plt.text(.9*max(xd)+.1*min(xd),.9*max(yd)+.1*min(yd),'$R^2 = %0.2f$'% Rsqr, fontsize=30)

            plt.xlabel("X Description")
            plt.ylabel("Y Description")

            # error bounds


            plt.plot(xl, yl, '-r')


            stats_daily[hour.strftime('%Y-%m-%d')] = (slope, Rsqr)


            plt.title(hour.strftime('%Y-%m-%d'))
            plt.scatter(y_speed, y_air)

            plt.show()

            y_speed = []
            y_air = []

        previous_hour = hour.strftime('%Y-%m-%d')

# Write slope, r_squared values to csv
writer = csv.writer(open('/Users/Steve/Github/bigdata_taxi_airquality/stats_daily.csv', 'wb'))
writer.writerow(["Date", "slope", "r_squared"])
for key, value in stats_daily.items():
   writer.writerow([key, value[0], value[1]])

c = datetime.now() - start_time
print 'It took', divmod(c.days * 86400 + c.seconds, 60), '(minutes, seconds).'

# fig = plt.figure()
# ax1 = fig.add_subplot(211)
# plt.plot(x, y, 'bo-', color='r', label='Avg Speed')
# plt.title('Average Taxi Speed vs Air Quality Measurements')
# plt.gca().set_ylim([0, 50])
# plt.ylabel('Average Taxi Speed')
# ax1.grid(b=True, which='major')
# ax1.grid(b=True, which='minor')
#
# ax2 = fig.add_subplot(212, sharex=ax1)
# plt.plot(x_air, y_air, 'bo-', color='b', label='NOx')
#
# plt.setp(ax1.get_xticklabels(), visible=False)
#
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
# plt.gcf().autofmt_xdate()
# plt.gca().set_ylim([0, 250])
# plt.ylabel('NOx')
# ax2.grid(b=True, which='major')
# ax2.grid(b=True, which='minor')
#
# plt.show()

