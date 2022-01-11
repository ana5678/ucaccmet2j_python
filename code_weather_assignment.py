import json

with open("precipitation.json") as precipitation_file:
    precipitation_data = json.load(precipitation_file)
    total_monthly_precipitation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #Go through the list, entry by entry and identify the entries that belong to the Seattle station
    for measurement in precipitation_data:
        if measurement['station'] == 'GHCND:US1WAKG0038':
            #Find the date of the measurement and extract the month from that date
            #Use the month as an index to store the total precipitation per month in a list
            date = measurement['date'].split('-')
            date[1] = int(date[1])
            total_monthly_precipitation[date[1]-1] += measurement['value']

        #Create the data structure that stores the total monthly precipitation per station
    Seattle_results = {
            'station': 'GHCND:US1WAKG0038',
            'state': 'WA',
            'totalMonthlyPrecipitation': total_monthly_precipitation
        }


with open('result1.json', 'w') as results_file:
    json.dump({'Seattle': Seattle_results}, results_file)