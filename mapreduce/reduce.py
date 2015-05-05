import sys
import csv
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np


def averageSpeed(loc, hour, speed):
	stats_daily = {}
	previous_hour = None
	for hour in line:
	    if len(measurements[hour]) > 1 and measurements[hour][0] < 200:  # only dates with air measurement < 200 and avg speed present
	        # take avg of all speeds in the array after air measurement within dictionary for each hour

	        if hour.strftime('%Y-%m-%d') == previous_hour or previous_hour == None:

	            avg_speed = math.ceil(reduce(lambda x, y: x + y, measurements[hour][1]) / len(measurements[hour][1]) * 100) / 100
	            print 'Hour: ', hour, 'Average Speed: ', round(avg_speed, 2)

def dailyStats():
# produce key-value pairs for each hour
# with slope and rsquared



def runReducer():
	# output from mapper.
	# (location, hour, pollutant, measurement)
	# (location, hour, speed)

	pollutant = None
	speed = None

    for line in sys.stdin:
    	
        line = line.strip()  # remove leading and trailing whitespace
    	row = line.split("\t", 1)
    	if len(row) == 3:
    		row[0] = loc
    		row[1] = hour
    		row[2] = speed
    		averageSpeed(loc,hour,speed)
    	else:
    		row[0] = loc
    		row[1] = hour
    		row[2] = pollutant
    		row[3] = measure
    		averageSpeed(loc,hour,pollutant,measure)

    	# hour = key.split(' ', 1)[1]

    	# if value.split(' ', 1)[0] == "Pollutant":
    	# 	pollutant = value.split(' ', 1)[1]
    	# else:
    	# 	speed = value.split(' ', 1)[1]

    	# if value[1] in pollutants:
    	# 	dailyStats(key, value)
    	# else:
    	# 	averageSpeed(key, value)

runReducer()