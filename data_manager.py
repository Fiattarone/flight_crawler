import requests

SHEETY_ENDPOINT: str


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        response.raise_for_status()

        print(response.json())