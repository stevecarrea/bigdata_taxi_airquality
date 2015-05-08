#!/usr/bin/python
import sys
import csv
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np

# Input:
# (hour, sky_condition, relative_humidity, wind_speed, wind_direction)
# (location, hour, speed)
# (location, hour, pollutant name, measurement)
# Output:
# (location, time, number_of_taxis, avg_speed, pm25_acceptable, ozone, co, pm25_raw, sky_condition, relative_humidity, wind_speed, wind_direction)

def average_speed(speeds):
    return math.ceil(reduce(lambda x, y: x + y, speeds) / len(speeds) * 100) / 100

def run_reducer():
    print "Location, Time, Number Of Taxis, Average Speed, PM25 Acceptable, Ozone, CO, PM25 Raw, Sky Condition, Relative Humidity, Wind Speed, Wind Direction"

    last_location = None
    last_hour = None
    last_tag = None
    last_day = None
    air_hourly = {}
    weather_hourly = {}
    speeds = []
    speed_first = False

    for line in sys.stdin:
        
        # line = line  # remove leading and trailing whitespace
        row = line.strip().split("\t")

        if len(row) == 3:  # (location, hour, measure)
            try:
                location = row[0]
                hour = row[1]
                speed = float(row[2])  # speed in mph, calculated in mapper
                tag = "speed"
            except TypeError:
                continue
        elif len(row) == 4:  # (location, hour, pollutant name, measure)
            location = row[0]
            hour = row[1]
            pollutant = row[2] # name of pollutant
            measure = row[3]
            tag = "pollutant"
        elif len(row) == 5:  # (hour, sky_condition, relative_humidity, wind_speed, wind_direction)
            hour = row[0]
            sky_condition = row[1]
            relative_humidity = row[2]
            wind_speed = row[3]
            wind_direction = row[4]
            tag = "weather"
        else:
            continue

        day = hour[:-9]

        if tag == "weather":
            weather_hourly[hour] = { "sky_condition" : sky_condition, "relative_humidity" : relative_humidity, "wind_speed": wind_speed, "wind_direction" : wind_direction }
        else:
            if hour != last_hour and speed_first:
                try:
                    print "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (last_location, last_hour, air_hourly[last_hour]["taxis_count"], air_hourly[last_hour]["avg_speed"], air_hourly[last_hour]["PM25 Acceptable"], air_hourly[last_hour]["Ozone"], air_hourly[last_hour]["CO"], air_hourly[last_hour]["PM25 Raw"], weather_hourly[last_hour]["sky_condition"], weather_hourly[last_hour]["relative_humidity"], weather_hourly[last_hour]["wind_speed"], weather_hourly[last_hour]["wind_direction"])
                # print air_hourly
                except KeyError:
                    print "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (last_location, last_hour, "", "", "", "", "", "", "", "", "", "")

            if day != last_day:
                if last_day:
                    # do logic of last_day here, when we looped over the day (generate graph)
                    pass
                air_hourly = {}
                speed_first = False

            if tag == "speed":
                speed_first = True
                if hour != last_hour:
                    speeds = []  # empty the array after each hour
                speeds.append(speed)

            if tag != last_tag and speed_first:
                taxis_count = len(speeds)
                avg_speed = average_speed(speeds)  # calculate average speed for each hour
                air_hourly[hour] = { "taxis_count" : taxis_count, "avg_speed" : avg_speed, "PM25 Acceptable": "", "Ozone" : "", "CO" : "", "PM25 Raw" : "" }

            if tag == "pollutant" and speed_first:
                try:
                    air_hourly[hour][pollutant] = measure
                except KeyError:
                    air_hourly[hour] = { "taxis_count" : "", "avg_speed" : "", "PM25 Acceptable": "", "Ozone" : "", "CO" : "", "PM25 Raw" : "" }              

            last_hour = hour
            last_location = location
            last_tag = tag
            last_day = day

if __name__ == '__main__':
    run_reducer()
