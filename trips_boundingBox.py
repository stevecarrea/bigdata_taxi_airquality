import datetime
import sys
import csv
import operator

count = 0
with open('/Users/Steve/GDrive/NYU_CUSP/Big_Data/project/trip_data_1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        try:
            pickup_lon = float(row[10])
            pickup_lat = float(row[11])
            pickup_date = row[5]
            dropoff_lon = float(row[12])
            dropoff_lat = float(row[13])
            dropoff_date = row[6]
            trip_distance = float(row[9])
            trip_duration = float(row[8])  # seconds

            # NYC bounding box
            # if(lon >= -74.2557 and lon <= -73.6895 and lat >= 40.4957 and lat <= 40.9176):
            #     count += 1

            # Division Street bounding box
            if(pickup_lon >= -73.997271 and pickup_lon <= -73.991832 and pickup_lat >= 40.713466 and pickup_lat <= 40.715052):

                if(dropoff_lon >= -73.997271 and dropoff_lon <= -73.991832 and dropoff_lat >= 40.713466 and dropoff_lat <= 40.715052):
                    speed = ( trip_distance / trip_duration ) * 3600
                    print 'Date: ', pickup_date, 'Speed: ', round(speed, 2)
                    count += 1
        except:
            pass

print 'Count: ', count

