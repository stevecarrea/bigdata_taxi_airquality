#!/usr/bin/python
import sys
import csv
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np

def average_speed(speeds):
    return math.ceil(reduce(lambda x, y: x + y, speeds) / len(speeds) * 100) / 100

def daily_stats(hourly_data):
    # produce key-value pairs for each hour
    # with slope and rsquared
    { "avg_speed" : avg_speed, "PM25 Acceptable": 0, "Ozone" : 0, "CO" : 0, "PM25 Raw" : 0 }

def run_reducer():
    # output from mapper.
    # (location, hour, speed)
    # (location, hour, pollutant name, measurement)

    # DivisionStreet  2013-01-03 01:00:00 12.6
    # DivisionStreet  2013-01-03 01:00:00 12.93
    # DivisionStreet  2013-01-03 01:00:00 8.5
    # DivisionStreet  2013-01-03 01:00:00 9.23
    # DivisionStreet  2013-01-03 01:00:00 9.42
    # DivisionStreet  2013-01-03 01:00:00 PM25 Acceptable 5.6
    # DivisionStreet  2013-01-03 01:00:00 PM25 Raw    2.9

    last_location = None
    last_hour = None
    last_tag = None
    last_day = None
    daily_data = {}
    speeds = []
    speed_first = False

    measurements = {}
    for line in sys.stdin:
        
        # line = line  # remove leading and trailing whitespace
        row = line.strip().split("\t")

        location = row[0]
        hour = row[1]
        day = hour[:-9]

        if len(row) == 3:  # (location, hour, measure)
            try:
                speed = float(row[2])  # speed in mph, calculated in mapper
                tag = "speed"
            except TypeError:
                continue
            # print 3
        elif len(row) == 4:  # (location, hour, pollutant name, measure)
            pollutant = row[2] # name of pollutant
            measure = row[3]
            tag = "pollutant"
            # print 3
        else:
            # print "else"
            continue

        if hour != last_hour and speed_first:
            print "%s,%s,%s,%s,%s,%s,%s" % (last_location, last_hour, hourly_data[last_hour]["avg_speed"], hourly_data[last_hour]["PM25 Acceptable"], hourly_data[last_hour]["Ozone"], hourly_data[last_hour]["CO"], hourly_data[last_hour]["PM25 Raw"])
            # print hourly_data
            pass

        if day != last_day:
            if last_day:
                # do logic of last_day here, when we looped over the day (generate graph)
                pass
            hourly_data = {}
            speed_first = False

        if tag == "speed":
            speed_first = True
            if hour != last_hour:
                speeds = []  # empty the array after each hour
            speeds.append(speed)

        # print tag
        # print last_tag
        # print tag != last_tag
        # print speed_first
        # print hour

        if tag != last_tag and speed_first:
            avg_speed = average_speed(speeds)  # calculate average speed for each hour
            hourly_data[hour] = { "avg_speed" : avg_speed, "PM25 Acceptable": "", "Ozone" : "", "CO" : "", "PM25 Raw" : "" }

        if tag == "pollutant" and speed_first:
            try:
                hourly_data[hour][pollutant] = measure
            except KeyError:
                hourly_data[hour] = { "avg_speed" : "", "PM25 Acceptable": "", "Ozone" : "", "CO" : "", "PM25 Raw" : "" }                


        last_hour = hour
        last_location = location
        last_tag = tag
        last_day = day

if __name__ == '__main__':
    run_reducer()
