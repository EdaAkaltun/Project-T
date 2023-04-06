import requests
import json


################################## GET ENVIROMENT TYPE ###################################
def gettypelocation(lon, lat):
    # Build the OSM API query URL
    url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zoom=18&addressdetails=1'.format(lon, lat)

    # Send a GET request to the API and get the response
    response = requests.get(url)

    # Parse the response JSON data
    data = json.loads(response.content)

    # Check type
    if 'city' in data['address']:
        print('The coordinates are in the city of', data['address']['city'])
        enviroment = "city"
    elif 'village' in data['address']:
        print('The coordinates are in the village of', data['address']['village'])
        enviroment = "village"
    else:
        print('The coordinates are in the plains.')
        enviroment = "plains"
    return enviroment