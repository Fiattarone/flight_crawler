import requests
import smtplib

SHEETY_ENDPOINT: str

sheety_header = {
                "Authorization": str
            }

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        response = requests.get(url=SHEETY_ENDPOINT, headers=sheety_header)
        response.raise_for_status()
        # self.response = response
        # print(self.response)
        self.emails = [contact["email"] for contact in response.json()["users"]]

    def send_emails(self, flight_data):
        my_email: str
        my_password: str
        with smtplib.SMTP("smtp.gmail.com", port=587) as econnection:
            econnection.starttls()
            econnection.login(user=my_email, password=my_password)
            for email in self.emails:
                for flight in flight_data:
                    econnection.sendmail(from_addr=my_email, to_addrs=email,
                                         msg=f"subject: Flight Deals!\n\n{vars(flight)}")