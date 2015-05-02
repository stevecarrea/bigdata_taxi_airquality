from __future__ import division
import csv
from datetime import datetime
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def resize_box(box, percent):
    lat_diff = box["lat"][1] - box["lat"][0]
    lon_diff = box["lon"][1] - box["lon"][0]
    new_lat_diff = lat_diff * math.sqrt(1 + percent / 100)
    new_lon_diff = lon_diff * math.sqrt(1 + percent / 100)
    resize_lat = (new_lat_diff - lat_diff) / 2
    resize_lon = (new_lon_diff - lon_diff) / 2
    new_p1 = { "lat" : (box["lat"][0] - resize_lat), "lon" : (box["lon"][0] - resize_lon) }
    new_p2 = { "lat" : (box["lat"][1] + resize_lat), "lon" : (box["lon"][1] + resize_lon) }
    output = { "lat" : [new_p1["lat"], new_p2["lat"]], "lon" : [new_p1["lon"], new_p2["lon"]] }
    return output

def daily():
    x = []
    y = []
    x_air = []
    y_air = []
    start_time = datetime.now()
    measurements = {}
    with open('/Users/brunomacedo/Desktop/NYU-Poly/3rd-Semester/Big-Data/project/nysdec_queenscollege_jan2013_NOx.csv', 'r') as csvfile_air:
        reader = csv.reader(csvfile_air)
        next(reader)
        for row in reader:
            try:
                # date_time = row[0]+' '+row[1]
                date_time = row[0]
                measurement_date = datetime.strptime(date_time, '%Y-%m-%d')  # 2013-01-27
                monitor_measurement = float(row[4])  # NOx
                if measurement_date not in measurements.keys():
                    measurements[measurement_date] = []
                measurements[measurement_date].append(monitor_measurement)
            except:
                pass

        for date in sorted(measurements):
            measurement = math.ceil(reduce(lambda x, y: x + y, measurements[date]) / len(measurements[date]) * 100) / 100
            x_air.append(date)
            y_air.append(measurement)
            print 'Date: ', date, ' | Average Measurement: ', round(measurement, 2), '| Number of Measurements: ', len(measurements[date])

    boxes = [ \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, -75), \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, -50), \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, 0), \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, 100), \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, 200) \
            ]

    boxes_speeds = []
    for i in range(0, len(boxes)):
        boxes_speeds.append({})
    
    with open('/Users/brunomacedo/Desktop/NYU-Poly/3rd-Semester/Big-Data/project/trip_data_1.csv', 'r') as csvfile:

        reader = csv.reader(csvfile)
        next(reader)

        speeds = {}
        count = 0

        for row in reader:
            # if count >= 5:  # for testing
            #     break
            try:
                # count += 1
                pickup_lon = float(row[10])
                pickup_lat = float(row[11])
                pickup_date = datetime.strptime(row[5][:-9], '%Y-%m-%d')  # 2013-01-27 11:45:00
                dropoff_date = datetime.strptime(row[6][:-9], '%Y-%m-%d')
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
                i = 0
                for box in boxes:
                    if(pickup_lon >= box["lon"][0] and pickup_lon <= box["lon"][1] and pickup_lat >= box["lat"][0] and pickup_lat <= box["lat"][1]) or \
                        (dropoff_lon >= box["lon"][0] and dropoff_lon <= box["lon"][1] and dropoff_lat >= box["lat"][0] and dropoff_lat <= box["lat"][1]):
                            if trip_distance < 2.0:
                                speed = ( trip_distance / trip_duration ) * 3600
                                if speed > 0 and speed < 50:
                                    if pickup_date not in boxes_speeds[i].keys():
                                        boxes_speeds[i][pickup_date] = []
                                    boxes_speeds[i][pickup_date].append(speed)

                                    # x.append(pickup_date)
                                    # y.append(speed)

                                    print 'Date: ', pickup_date, 'Speed: ', round(speed, 2)
                                    count += 1
                    i += 1
            except:
                pass

    print 'Count: ', count

    colors = ['r', 'g', 'y', 'k', 'c']

    for i in range(0, len(boxes)):
        x.append([])
        y.append([])

    for i in range(0, len(boxes)):
        for date in sorted(boxes_speeds[i]):
            speed = math.ceil(reduce(lambda x, y: x + y, boxes_speeds[i][date]) / len(boxes_speeds[i][date]) * 100) / 100
            x[i].append(date)
            y[i].append(speed)
            print 'Date: ', date, '| Average Speed: ', speed, '| Number of Taxis: ', len(boxes_speeds[i][date])

    c = datetime.now() - start_time
    print 'It took', divmod(c.days * 86400 + c.seconds, 60), '(minutes, seconds).'

    for i in range(0, len(boxes)):
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        plt.plot(x[i], y[i], 'bo-', color=colors[i], label='Avg Speed')
        plt.title('Average Taxi Speed vs Air Quality Measurements')
        plt.gca().set_ylim([0, 50])
        plt.ylabel('Average Taxi Speed')
        plt.grid()

        ax2 = fig.add_subplot(212, sharex=ax1)
        plt.plot(x_air, y_air, 'bo-', color='b', label='NOx')

        plt.setp(ax1.get_xticklabels(), visible=False)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
        plt.gcf().autofmt_xdate()
        plt.gca().set_ylim([0, 250])
        plt.ylabel('NOx')
        plt.grid()
        plt.show()

def hourly():
    x = []
    y = []
    # x_air = []
    # y_air = []
    y_speed = []
    y_air = []
    speeds = {}
    start_time = datetime.now()
    measurements = {}
    with open('/Users/brunomacedo/Desktop/NYU-Poly/3rd-Semester/Big-Data/project/nysdec_queenscollege_jan2013_NOx.csv', 'r') as csvfile_air:
        reader = csv.reader(csvfile_air)
        next(reader)
        for row in reader:
            try:
                date_time = row[0]+' '+row[1][:-3]
                measurement_date = datetime.strptime(date_time, '%Y-%m-%d %H')  # 2013-01-27 11:00:00
                monitor_measurement = float(row[4])  # NOx
                if measurement_date not in measurements:
                    measurements[measurement_date] = []
                measurements[measurement_date].append(monitor_measurement)
                print 'Date: ', measurement_date, 'NOx: ', monitor_measurement
            except:
                pass

        # for date in sorted(measurements):
        #     x_air.append(date)
        #     y_air.append(measurements[date])
        #     print 'Date and Hour: ', date, ' | Measurement: ', measurements[date]

    boxes = [ \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, -75), \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, -50), \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, 0), \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, 100), \
        resize_box({ "lat" : [40.726365, 40.743795], "lon" : [-73.837724,-73.812404] }, 200) \
            ]

    boxes_speeds = []
    for i in range(0, len(boxes)):
        boxes_speeds.append({ "x" : [], "y" : [] })

    with open('/Users/brunomacedo/Desktop/NYU-Poly/3rd-Semester/Big-Data/project/trip_data_1.csv', 'r') as csvfile:
        
        reader = csv.reader(csvfile)
        next(reader)

        speeds = {}
        count = 0

        for row in reader:
            if count >= 5:  # for testing
                break
            try:
                # count += 1
                pickup_lon = float(row[10])
                pickup_lat = float(row[11])
                pickup_date = datetime.strptime(row[5][:-6], '%Y-%m-%d %H')  # 2013-01-27 11:45:00
                dropoff_date = datetime.strptime(row[6][:-6], '%Y-%m-%d %H')
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

                

                i = 0
                for box in boxes:
                    if(pickup_lon >= box["lon"][0] and pickup_lon <= box["lon"][1] and pickup_lat >= box["lat"][0] and pickup_lat <= box["lat"][1]) or \
                        (dropoff_lon >= box["lon"][0] and dropoff_lon <= box["lon"][1] and dropoff_lat >= box["lat"][0] and dropoff_lat <= box["lat"][1]):
                            if trip_distance < 1.5:
                                speed = ( trip_distance / trip_duration ) * 3600
                                if speed > 0 and speed < 50:
                                    if pickup_date not in measurements:
                                        print 'Missing data for: ', pickup_date
                                        pass
                                    else:
                                        if len(measurements[pickup_date]) == 1:
                                            for i in range(0, len(boxes)):
                                                measurements[pickup_date].append([])
                                        measurements[pickup_date][i+1].append(speed)
                                        print 'Date: ', pickup_date, 'Speed: ', round(speed, 2)
                                        count += 1
                    i += 1
            except:
                pass
    print 'Count: ', count

    colors = ['r', 'g', 'y', 'k', 'c']

    for i in range(0, len(boxes)):
        for date in sorted(measurements):
            if len(measurements[date]) == len(boxes) + 1:
                if len(measurements[date][i+1]) > 1 and measurements[date][0] < 200:
                    avg_speed = math.ceil(reduce(lambda x, y: x + y, measurements[date][i+1]) / len(measurements[date][i+1]) * 100) / 100
                    y_speed.append(avg_speed)
                    y_air.append(measurements[date][0])

    c = datetime.now() - start_time
    print 'It took', divmod(c.days * 86400 + c.seconds, 60), '(minutes, seconds).'

    plt.scatter(y_speed, y_air)
    plt.show()

    # for i in range(0, len(boxes)):
    #     fig = plt.figure()
    #     ax1 = fig.add_subplot(211)
    #     plt.plot(boxes_speeds[i]["x"],boxes_speeds[i]["y"], 'bo-', color=colors[i], label='Avg Speed')
    #     plt.title('Average Taxi Speed vs Air Quality Measurements')
    #     plt.gca().set_ylim([0, 50])
    #     plt.ylabel('Average Taxi Speed')
    #     ax1.grid(b=True, which='major')
    #     ax1.grid(b=True, which='minor')

    #     ax2 = fig.add_subplot(212, sharex=ax1)
    #     plt.plot(x_air, y_air, 'bo-', color='b', label='NOx')

    #     plt.setp(ax1.get_xticklabels(), visible=False)

    #     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    #     plt.gcf().autofmt_xdate()
    #     plt.gca().set_ylim([0, 250])
    #     plt.ylabel('NOx')
    #     ax2.grid(b=True, which='major')
    #     ax2.grid(b=True, which='minor')
    #     plt.show()

# daily();
hourly();





