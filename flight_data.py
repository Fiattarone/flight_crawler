class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, departure_city, departure_airport_code, destination_city, destination_city_code,
                 departure_date, return_date, bags_price, ticket_URL):
        self.price = price
        self.bags_price = bags_price
        self.departure_city = departure_city
        self.departure_airport_code = departure_airport_code
        self.destination_city = destination_city
        self.destination_city_code = destination_city_code
        self.departure_date = departure_date
        self.return_date = return_date
        self.ticket_URL = ticket_URL
