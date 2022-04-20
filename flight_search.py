import requests

KIWI_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self, api_key, flight_acronym):
        kiwi_headers = {
            "apikey": api_key
        }

        kiwi_query = {
            "term": flight_acronym
        }

        response = requests.get(url=KIWI_ENDPOINT, headers=kiwi_headers, params=kiwi_query)
        response.raise_for_status()

        # print(type(response.json()))
        self.response = response.json()