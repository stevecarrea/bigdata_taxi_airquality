# Using NYC Taxi Data as a Predictor of Urban Air Quality

This project analyzes over 700 million NYC taxi trips based on data from the NYC Taxi and Limousine Commision, in conjunction with air quality measurements recorded by federal regulatory air monitoring stations. This is a big data analysis performed using Hadoop within an AWS cluster. 
 
### Team Members:
Steve Carrea, Paul Cho, Bruno Pasini 

### Abstract:
Motor vehicles emit pollutants that cause harm to human health and the environment. Nitrogen oxides (NOx), carbon monoxide (CO), volatile organic compounds (VOC) and particulate matter (PM) are released through the combustion of gasoline, diesel, and other motor vehicle fuels. These mobile sources constitute a major source of urban air pollution, and NYC collects increasingly amounts of data relating to these sources of pollution. The focus of this study was to determine the impact on local air quality from motor vehicles by using NYC taxis as a proxy; and thereby acting as potential sensors for traffic-induced air pollution. This study specifically focused on taxi data, as supplied by the NYC Taxi and Limousine Commission in an attempt to identify a relationship between average taxi speed and air quality measurements as obtained from various air monitors. The team created a MapReduce program to ingest data from roughly 700 million taxi trips and perform the analysis. A hadoop-streaming program was written in Python to perform the calculations on a daily basis from 2010 through 2013 using hourly averages for taxi speed and air quality. The result is a table of correlation coefficients (r values) for average taxi speed and air quality on a daily basis. Weak correlations were found based on the current methodology and improvements are discussed in the conclusion. Specifically, we find that federal reference air monitors are not located close enough to roadways for this specific study and instead propose to use air monitoring data from the New York City Community Air Survey for a subsequent iteration. 

### Introduction:
The main objective of this research was to determine if any relationship can be identified between NYC taxi data and air pollution measurements. It is expected that air pollution measurements will vary as nearby vehicle traffic density and speed change. The significance of this research is the possibility of predicting and mitigating where and when traffic-induced pollution may be relatively worse within the urban environment. This may be used to mitigate health effects from air pollution or for implementation of policy measures related to greenhouse gas reduction efforts. A brief review of literature showed similar research studies, but none that used NYC taxi data and derived speed values as the predictor. Other research studies used traffic counts from the Department of Transportation or other methods of obtaining traffic density. One study in particular, from Riga City, is mentioned in the conclusions as showing similar results and weak correlation based on the current data and methodology.

### Data:

#### Taxi Data
The team used NYC taxi data as produced by the NYC Taxi and Limousine Commission from 2010 through 2013, which amounted to about 700 million taxi trips. A subset was selected of about 2.38 million taxi trips. From each trip, the team used the location (latitude, longitude) of the pick up and drop off points, trip duration, and trip distance. 

####  Air Quality Data
The team decided to use air quality data as produced at hourly intervals by monitors operated by the New York State Department of Environmental Conservation. This monitoring network was established to measure and monitor regional air quality. State air monitors are few and far in between and are not typically located near major roadways since they serve to measure regional air quality as opposed to local air quality. We still began our approach with State data since measurements are readily available on an hourly basis.

### Method:

The timeframe for analysis was 2010 through 2013. During this timeframe, the team calculated the average taxi speed on an hourly basis for those trips that either began or ended within a specified bounding box. An arbitrary initial bounding box was set around each air quality monitor.

#### Bounding Box Evaluation
For each air monitor, the team first tested various sizes of bounding boxes to determine which was best suited for the analysis. This was done by building an array of bounding boxes, each being incremented by a certain factor. The results below show the chosen bounding boxes for each station.

The team analyzed trips that either originated or ended within an arbitrary bounding box, chosen for its location relative to roads in proximity to the air monitor of interest. The air monitor was placed near the center of the bounding box, which was rectangular. The two points in the above table are needed to test for whether the trip originated or ended within the box.

#### Hadoop Streaming Program

The program uses data from all NYC taxi trips taken between 2010 through 2013, hourly measurements of pollutants from three air quality monitors in NYC, and hourly weather data from a monitor in Central Park. This data is sent to mappers as explained below. The final output from the reducer consists of aggregated values for average taxi speed and air pollution measurements in order to calculate correlation coefficients between average taxi speed and air pollution on a daily basis. It also consists of relevant weather conditions for each day.  

##### Map Function

The map function consists of three functions: trips, air quality, and weather.

The trips function operates on the taxi trip data. The mapper selects data for analysis based on whether or not a trip originates or ends within one of three predefined bounding boxes. If so, the map function will output a tuple of <Location,Hour,Speed> for all trips where location is the monitor station within the bounding box, and the speed is calculated as: 

speed = ( trip_distance / trip_duration ) * 3600

An additional constraint used was to only consider trips where trip_distance < 1.5 miles so to use trips that occurred relatively closer to the air monitor than others. The average and median trip distance was found to be near 2 miles.

The air quality function operates on the air quality data. The mapper selects all data input for a specific air monitor and parses it by hour, emitting the following tuple:

<Location, Hour, Pollutant Name, Measure>

The weather function operates on the meteorological data, as obtained from Central Park. The mapper selects all data input for the specified monitor and emits the following tuple:

<Hour, Sky Condition, Relative Humidity, Wind Speed, Wind Direction>

To summarize, the following tuples are output from each mapper:

For taxi input, emit: <Location,Hour,Speed> 
For pollutant measurement, emit: <Location, Hour, Pollutant Name, Measure>
For weather input, emit: <Hour, Sky Condition, Relative Humidity, Wind Speed, Wind Direction>

##### Reduce Function

The reduce function consists of two functions, one to calculate the average taxi speeds for each hour and location, and the second to join this output with the pollutants data, which is aggregated in a single row for each hour and location, and ultimately joins this with the hourly weather data.

As mentioned above within the Map Function discussion, the following is received by the reducer:

<Location,Hour,Speed>
<Location, Hour, Pollutant Name, Measure>
<Hour, Sky Condition, Relative Humidity, Wind Speed, Wind Direction>

The reducer will output the average speed for each hour, the number of taxis that compose the average, the pollutants measure in that location and hour and the weather data as the following tuple:

<Location, Time, Number Of Taxis, Average Speed, PM25 Acceptable, Ozone, CO, PM25 Raw, Sky Condition, Relative Humidity, Wind Speed, Wind Direction>

##### Hadoop Configuration

We had to specify MapReduce to run with only one reducer and also that the first three values separated by a tab were part of the key in the map output.

-D mapreduce.job.reduces=1
-D stream.num.map.output.key.fields=3

### Challenges:

The team was unsure what size bounding box to use. If too small, then there may not be enough data points to establish any relationship. If too large, then the area would not correspond to that which may affect a given air monitor. Various sizes were tested to ensure that at least a few trips occurred during each hour.

### Conclusion:

Based on the results, weak correlation was found between average taxi speed and any pollutant for each station. After reviewing weather data, it was found that on days with relatively higher R values (greater than 0.5), wind conditions averaged roughly 6 mph, which is relatively low. Therefore, it is possible that the higher correlation is related to the decrease in natural ventilation.

These results are very similar to those produced from a study conducted in Riga City, Latvia. In the Riga City study, similar correlations were found between traffic intensity (vehicles/hr) and various pollutants including those related to this study: particulate matter, nitrogen dioxide, and carbon monoxide. The better correlations from the Riga City study were found with nitrogen dioxide (NO2), as compared with our research which found better correlation with ozone (O3). Nitrogen oxides ultimately produce ozone after being released into the atmosphere. 

Both the Riga City study and our study attempted to use stationary source monitors that were not necessarily located near street level or significant areas of pollution produced from traffic sources.

The team may follow-up with improvements to this method to produce better results.

