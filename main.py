from pprint import pprint

from data_manager import DataManager
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from flight_search import FlightSearch
from datetime import datetime as dt
from datetime import timedelta
from notification_manager import NotificationManager

ORIGIN = "SMF"
TWILIO_SID_KEY: str
TWILIO_AUTH: str


dm, flight_searcher = DataManager(), FlightSearch()
destinations = [area["city"] for area in dm.get_response["prices"]]
dm.set_flight_data(flight_data=[(flight_searcher.get_flight_codes(flight_acronym=city))["locations"][0]
                   for city in destinations])

# for city in destinations:
#     dm.set_flight_data(flight_data=flight_searcher.get_flight_codes(flight_acronym=city).response)

flights = flight_searcher.find_flights(origin=ORIGIN, destinations=destinations,
                                       from_time=dt.now()+timedelta(days=30),
                                       to_time=dt.now()+timedelta(days=37),
                                       city_to_code_hashmap=dm.city_to_code)

lowest_price = {row["city"]: int(row["lowestPrice"]) for row in dm.get_response["prices"]}

pprint(lowest_price)
pprint(type(lowest_price))

for flight in flights:
    try:
        print(flight.destination_city)
        print(lowest_price[flight.destination_city])
        print(type(lowest_price[flight.destination_city]))
        print(type(flight.price))
        print(int(flight.price) < lowest_price[flight.destination_city])
        # overwrite old lowest price with a put request
        if int(flight.price) < lowest_price[flight.destination_city]:
            dm.overwrite_lowest_price(flight.destination_city, flight.price)
            print("Overwrote")

    # except KeyError:
    #     pprint(vars(flight))
    finally:
        print("Out")

NotificationManager().send_emails(flights)
for ticket_info in flights:
    proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {"https": os.environ["http-proxy"]}
    client = Client(TWILIO_SID_KEY, TWILIO_AUTH, http_client=proxy_client)
    message = client.messages.create(
        body=f"|\n\n {ticket_info.departure_city} ({ticket_info.departure_airport_code}) -> "
             f"{ticket_info.destination_city} ({ticket_info.destination_city_code}):\n\nPrice: {ticket_info.price}\nBag"
             f"Price: {ticket_info.bags_price}\n\nLeaving: {ticket_info.departure_date}\n\n"
             f"Returning:\n\"{ticket_info.return_date}\"\n\nURL: {ticket_info.ticket_URL}",
        from_="+14707307976",
        to="+18317373286"
    )
    print(message.status)