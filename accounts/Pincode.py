import requests
import json
from src.myproject.settings import GOOGLE_API_KEY

# address = 'Khadakpada, Kalyan West, Maharashtra, India'
#
# address2 = 'IIT BOMBAY, Powai, Mumbai'
#
# address3 = 'Naupada, Thane, India'


def get_pincode(address):
    key = GOOGLE_API_KEY

    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, key)

    response = requests.get(url)

    tresponse = json.loads(response.text)

    # print(response.text)

    if tresponse['status']=='OK':
        for component in tresponse['results'][0]['address_components']:
            if 'postal_code' in component['types']:
                return component['long_name']

# print(get_pincode('Bldg. no. 16, Nebula Darshan, Khadakpada, Kalyan West, Maharashtra, India'))