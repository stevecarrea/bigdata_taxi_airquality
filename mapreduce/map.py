#!/usr/bin/python
import sys
import os
import csv
import StringIO
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np

# file_path = os.environ.get('mapreduce_map_input_file', 'stdin')
# file_name = os.path.split(file_path)[-1][:-4]

def import_air(line):
    # import air quality data for each hour

    locations = { "134" : "DivisionStreet", "135" : "CCNY", "128" : "PS19" }
    pollutants = { "88502" : "PM25 Acceptable", "44201" : "Ozone", "42101" : "CO", "88501" : "PM25 Raw" }

    try:
        date_time = line[10]+' '+line[11][:-3]
        location = locations[line[6]]
        pollutant = pollutants[line[7]]
        measurement_date = datetime.strptime(date_time, '%Y-%m-%d %H')  # 2013-01-27 11:45:00
        monitor_measurement = float(line[16])  # DivisionStreet, PM2.5
        print '%s\t%s\t%s\t%s' % (location, measurement_date, pollutant, monitor_measurement)
    except KeyError:
        pass

def import_trips(line):
    # import trips data that fall within a bounding boxes and pass along the date_hour and speed
    try:
        pickup_lon = float(line[10])
        pickup_lat = float(line[11])
        pickup_date = datetime.strptime(line[5][:-6], '%Y-%m-%d %H') # 2013-01-27 11:45:00
        dropoff_date = datetime.strptime(line[6][:-6], '%Y-%m-%d %H')
        dropoff_lon = float(line[12])
        dropoff_lat = float(line[13])
        trip_distance = float(line[9])
        trip_duration = float(line[8])  # seconds

        boxes = \
            [ \
                { "lat" : [40.713221, 40.715319], "lon" : [-73.998166,-73.993370], "location" : "DivisionStreet" }, \
                { "lat" : [40.813844, 40.821606], "lon" : [-73.968777,-73.938522], "location" : "CCNY" }, \
                { "lat" : [40.728960, 40.729627], "lon" : [-73.992799,-73.977178], "location" : "PS19" } \
            ] \
        
        for box in boxes:
            if(pickup_lon >= box["lon"][0] and pickup_lon <= box["lon"][1] and pickup_lat >= box["lat"][0] and pickup_lat <= box["lat"][1]) or \
                (dropoff_lon >= box["lon"][0] and dropoff_lon <= box["lon"][1] and dropoff_lat >= box["lat"][0] and dropoff_lat <= box["lat"][1]):
                    if trip_distance < 1.5:
                        speed = ( trip_distance / trip_duration ) * 3600
                        if speed > 0 and speed < 50:
                            print '%s\t%s\t%s' % (box["location"], pickup_date, round(speed, 2))

    except:
        pass

def import_weather(line):  # NEED TO SKIP HEADER ROW
    # import weather from central park weather station
    # try:
    date_time = line[1]+' '+line[2][:-2]
    date = str(datetime.strptime(date_time, "%Y%m%d %H"))
    sky_condition = str(line[4])
    rel_humidity = int(line[22])
    wind_speed = line[24]
    wind_direction = line[26]
    print '%s\t%s\t%s\t%s\t%s' % (date, sky_condition, rel_humidity, wind_speed, wind_direction)
    # except:
    #     pass


def run_mapper():
    # chose which function to run based on the file read by mapper
    # cnt = 0
    for line in sys.stdin:
        line = line.strip().split(',')
        if len(line) == 25:
            import_air(line)
            # cnt +=1
        # if cnt == 1000:
        #     break
        elif len(line) == 44:
            import_weather(line)
        else:
            import_trips(line)

if __name__ == '__main__':
    run_mapper()

