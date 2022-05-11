import requests
# from data_manager import DataManager
from pprint import pprint
from flight_data import FlightData

KIWI_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
KIWI_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
KIWI_API_KEY: str


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        # self.flight_response = []
        self.response = ""
        self.flight_data = []

    def get_flight_codes(self, flight_acronym):
        kiwi_headers = {
            "apikey": KIWI_API_KEY,
            "locale": "en-US",
            "location_types": "airport",
            "limit": "10",
            "active_only": "True"
        }

        kiwi_query = {
            "term": flight_acronym
        }

        response = requests.get(url=KIWI_ENDPOINT, headers=kiwi_headers, params=kiwi_query)
        response.raise_for_status()

        # pprint(response.json())
        self.response = response.json()
        return self.response

    def find_flights(self, origin, destinations, from_time, to_time, city_to_code_hashmap) -> list[FlightData]:
        search_header = {
            "apikey": KIWI_API_KEY
        }
        pprint(city_to_code_hashmap)
        pprint(destinations)
        for city in destinations:
            # What is happening below is we're grabbing the city name and not the city code -- we can allegedly
            # only search by city code
            name_of_city = city_to_code_hashmap[city]
            pprint(name_of_city)
            kiwi_query = {
                "fly_from": origin,
                "fly_to": name_of_city,
                "date_from": from_time.strftime("%d/%m/%Y"),
                "date_to": to_time.strftime("%d/%m/%Y"),
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "flight_type": "round",
                "one_for_city": 1,
                "max_stopovers": 0,
                "curr": "USD"
            }

            response = requests.get(url=KIWI_SEARCH_ENDPOINT, headers=search_header, params=kiwi_query)
            data = ""
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                pass
            finally:
                try:
                    data = response.json()["data"][0]
                    flight_obj = FlightData(price=data["price"], bags_price=data["bags_price"],
                                            departure_airport_code=data["cityCodeFrom"],
                                            departure_date=from_time.strftime("%d/%m/%Y"),
                                            destination_city=city,
                                            destination_city_code=data["cityCodeTo"],
                                            departure_city=data["cityFrom"], return_date=to_time.strftime("%d/%m/%Y"),
                                            ticket_URL=data["deep_link"])
                    pprint(data["bags_price"])
                    pprint(data["price"])
                except IndexError:
                    print(f"No flights found for {city}.")
                else:
                    self.flight_data.append(flight_obj)
        pprint(self.flight_data)
        # for flight in self.flight_data:
        #     pprint(vars(flight))
        return self.flight_data

