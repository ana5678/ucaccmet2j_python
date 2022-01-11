import json
with open('stations.csv') as stations_file:
    #Read the contents of the file into a data structure: a list of dictionaries
    stations = []
    headers = stations_file.readline()
    for line in stations_file:
        city, state, station_name = line.strip().split(',')
        stations.append({'city': city, 'state': state, 'station_name':station_name})

with open("precipitation.json") as precipitation_file:
    precipitation_data = json.load(precipitation_file)
    #Go through the list, entry by entry and identify the entries that belong to each station
    index = 0
    results = {}
    for index in range(4):
        total_monthly_precipitation = [0] * 12
        for measurement in precipitation_data:
            if measurement['station'] == stations[index]['station_name']:
                #Find the date of the measurement and extract the month from that date
                #Use the month as an index to store the total precipitation per month in a list
                date = measurement['date'].split('-')
                date[1] = int(date[1])
                total_monthly_precipitation[date[1]-1] += measurement['value']

        #Create the data structure that stores the total monthly precipitation per station
        results[stations[index]['city']] = {
            'station': stations[index]['station_name'],
            'state': stations[index]['state'],
            'totalMonthlyPrecipitation': total_monthly_precipitation
        }

        #Calcultate the total yearly precipitation
        total_yearly_precipitation = sum(total_monthly_precipitation)
        results[stations[index]['city']]['totalYearlyPrecipitation'] = total_yearly_precipitation
        #Make a list of the relative precipitation per month
        #The values are numbers with two decimals
        relative_monthly_precipitation = [0]*12
        month = 0
        for precipitation in total_monthly_precipitation:
            relative_monthly_precipitation[month] = precipitation/total_yearly_precipitation
            relative_monthly_precipitation[month] = round(relative_monthly_precipitation[month], 2)
            month += 1
        results[stations[index]['city']]['relativeMonthlyPrecipitation'] = relative_monthly_precipitation
#Compute the sum of yearly precipitation in every state
index = 0
total_yearly_precipitation_all_stations = 0
for index in range(4):
    total_yearly_precipitation_all_stations += results[stations[index]['city']]['totalYearlyPrecipitation']
#Compute the relative yearly precipitation and add it to the results data structure
index = 0
for index in range(4):
    results[stations[index]['city']]['relativeYearlyPrecipitation'] = round(results[stations[index]['city']]['totalYearlyPrecipitation']/total_yearly_precipitation_all_stations, 2)
#What is the percentage of rain that fell in Seattle from the total yearly precipitation in every state
index = 0
for index in range(4):
    if results[stations[index]['city']]['station'] == "GHCND:US1WAKG0038":
        print('The percentage of yearly precipitation in Seattle is', results[stations[index]['city']]['relativeYearlyPrecipitation']*100, '%')
with open('result3.json', 'w') as results_file:
    json.dump(results, results_file)