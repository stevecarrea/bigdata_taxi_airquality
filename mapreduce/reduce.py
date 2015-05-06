import sys
import csv
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np

def avg_speed(speeds):
    return math.ceil(reduce(lambda x, y: x + y, speeds) / len(speeds) * 100) / 100

def daily_stats(hourly_data):
    # produce key-value pairs for each hour
    # with slope and rsquared



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


    measurements = {}
    for line in sys.stdin:
        
        line = line.strip()  # remove leading and trailing whitespace
        row = line.split("\t", 1)

        location = row[0]
        hour = row[1]
        day = hour[:-9]

        if len(row) == 3:  # (location, hour, measure)
            speed = row[3]  # speed in mph, calculated in mapper
            tag = "speed"
        else:  # (location, hour, pollutant name, measure)
            pollutant = row[2] # name of pollutant
            measure = row[3]
            tag = "pollutant"

        if day != last_day:
            if last_day:
                # do logic of last_day here (generate graph)
                daily_stats(hourly_data)
            hourly_data = {}

        if tag == "speed":
            if hour != last_hour:
                speeds = []  # empty the array after each hour
            speeds.append(speed)

        if tag != last_tag:
            avg_speed = avg_speed(speeds)  # calculate average speed for each hour
            hourly_data[hour] = { "avg_speed" : avg_speed, "PM25 Acceptable": 0, "Ozone" : 0, "CO" : 0, "PM25 Raw" : 0 }

        if tag == "pollutant":
            hourly_data[hour][pollutant] = measure

        last_hour = hour
        last_location = location
        last_tag = tag
        last_day = day


run_reducer()