import requests
import json
from pprint import pprint
from flight_data import FlightData

SHEETY_ENDPOINT: str

sheety_header = {
                "Authorization": str
            }


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.response = ""
        response = requests.get(url=SHEETY_ENDPOINT, headers=sheety_header)
        response.raise_for_status()
        self.get_response = response.json()
        self.city_to_code = {}

        # print(self.get_response)

    def set_flight_data(self, flight_data):
        #make this a put request that uses a for loop to update the individual cell for each city
        # print("flight data incoming")
        # pprint(flight_data)
        # flight data goes in here, but how do we pull the name from the city dictionary
        for idx, city in enumerate(flight_data):
            sheety_json = {
                "price": {
                    "iataCode": city["code"]
                }
            }
            # hold = city["code"]
            self.city_to_code[city["name"]] = city["code"]

            # response = requests.put(url=f"{SHEETY_ENDPOINT}/{idx+2}", json=sheety_json, headers=sheety_header)
            # response.raise_for_status()

            print(f"{city['code']} has been written to Google Sheets. ")
            self.response = "response.text"
        return self.response

    def overwrite_lowest_price(self, city, lowest_price):
        sheet = self.get_response["prices"]
        print("overwriting currently.." + city, + lowest_price)
        for idx, row in enumerate(sheet):
            if row["city"] == city:
                sheety_json = {
                    "price": {
                        "lowestPrice": lowest_price
                    }
                }
                response = requests.put(url=f"{SHEETY_ENDPOINT}/{idx+2}", json=sheety_json, headers=sheety_header)
                response.raise_for_status()

