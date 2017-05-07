import requests
import json
from myproject.settings import GOOGLE_API_KEY

# address = 'Khadakpada, Kalyan West, Maharashtra, India'
#
# address2 = 'IIT BOMBAY, Powai, Mumbai'
#
# address3 = 'Naupada, Thane, India'


def get_pincode(address):
    key = GOOGLE_API_KEY

    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, key)

    response = requests.get(url)

#response.text converts it to string in json format
#json.loads converts it to python dictionary
    response_dictionary = json.loads(response.text)

    if response_dictionary['status'] == 'OK':
        for address_component in response_dictionary['results'][0]['address_components']:
            if 'postal_code' in address_component['types']:
                return address_component['long_name']

print(get_pincode('Bldg. no. 16, Nebula Darshan, Khadakpada, Kalyan West, Maharashtra, India'))