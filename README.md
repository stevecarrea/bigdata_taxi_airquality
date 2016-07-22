# Using NYC Taxi Data as a Predictor of Urban Air Quality

This project analyzes over 700 million NYC taxi trips based on data from the NYC Taxi and Limousine Commision, in conjunction with air quality measurements recorded by federal regulatory air monitoring stations. This is a big data analysis performed using Hadoop within an AWS cluster. 
 
### Team Members:
Steve Carrea, Paul Cho, Bruno Pasini 

### Abstract:
Motor vehicles emit pollutants that cause harm to human health and the environment. Nitrogen oxides (NOx), carbon monoxide (CO), volatile organic compounds (VOC) and particulate matter (PM) are released through the combustion of gasoline, diesel, and other motor vehicle fuels. These mobile sources constitute a major source of urban air pollution, and NYC collects increasingly amounts of data relating to these sources of pollution. The focus of this study was to determine the impact on local air quality from motor vehicles by using NYC taxis as a proxy; and thereby acting as potential sensors for traffic-induced air pollution. This study specifically focused on taxi data, as supplied by the NYC Taxi and Limousine Commission in an attempt to identify a relationship between average taxi speed and air quality measurements as obtained from various air monitors. The team created a MapReduce program to ingest data from roughly 700 million taxi trips and perform the analysis. A hadoop-streaming program was written in Python to perform the calculations on a daily basis from 2010 through 2013 using hourly averages for taxi speed and air quality. The result is a table of correlation coefficients (r values) for average taxi speed and air quality on a daily basis. Weak correlations were found based on the current methodology and improvements are discussed in the conclusion. Specifically, we find that federal reference air monitors are not located well for this specific study and instead propose to use air monitoring data from the New York City Community Air Survey for a subsequent iteration. Data from these monitors are located closer to roadways.

### Introduction:
The main objective of this research was to determine if any relationship can be identified between NYC taxi data and air pollution measurements. It is expected that air pollution measurements will vary as nearby vehicle traffic density and speed change. The significance of this research is the possibility of predicting and mitigating where and when traffic-induced pollution may be relatively worse within the urban environment. This may be used to mitigate health effects from air pollution or for implementation of policy measures related to greenhouse gas reduction efforts. A brief review of literature showed similar research studies, but none that used NYC taxi data and derived speed values as the predictor. Other research studies used traffic counts from the Department of Transportation or other methods of obtaining traffic density. One study in particular, from Riga City, is mentioned in the conclusions as showing similar results and weak correlation based on the current data and methodology.

### Data:

#### Taxi Data
The team used NYC taxi data as produced by the NYC Taxi and Limousine Commission from 2010 through 2013, which amounted to about 700 million taxi trips. A subset was selected of about 2.38 million taxi trips. From each trip, the team used the location (latitude, longitude) of the pick up and drop off points, trip duration, and trip distance. 

####  Air Quality Data
The team decided to use air quality data as produced at hourly intervals by monitors operated by the New York State Department of Environmental Conservation. This monitoring network was established to measure and monitor regional air quality. State air monitors are few and far in between and are not typically located near major roadways since they serve to measure regional air quality as opposed to local air quality. We still began our approach with State data since measurements are readily available on an hourly basis.

### Method:

The timeframe for analysis was 2010 through 2013. During this timeframe, the team calculated the average taxi speed on an hourly basis for those trips that either began or ended within a specified bounding box. An arbitrary initial bounding box was set around each air quality monitor.

#### Hadoop Streaming Program

The program uses data from all NYC taxi trips taken between 2010 through 2013, hourly measurements of pollutants from three air quality monitors in NYC, and hourly weather data from a monitor in Central Park. This data is sent to mappers as explained below. The final output from the reducer consists of aggregated values for average taxi speed and air pollution measurements in order to calculate correlation coefficients between average taxi speed and air pollution on a daily basis. It also consists of relevant weather conditions for each day.  

