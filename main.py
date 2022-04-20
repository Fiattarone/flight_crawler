from data_manager import DataManager
import flight_data
import notification_manager
import twilio
from flight_search import FlightSearch

KIWI_API_KEY: str
FLIGHT_TERM = "PRG"

FlightSearch(api_key=KIWI_API_KEY, flight_acronym=FLIGHT_TERM)
DataManager()