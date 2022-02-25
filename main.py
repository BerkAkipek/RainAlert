import requests
import os
from dotenv import load_dotenv, find_dotenv
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

load_dotenv(find_dotenv())
OWM_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.environ.get("OWM_API_KEY")
LAT = 41.008240
LNG = 28.978359

account_sid = "AC14674ed0141cc274ee9ced5c19cbbf1c"
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
my_number = os.getenv('my_number')

parameters = {
    "lat": LAT,
    "lon": LNG,
    "exclude": "current,minutely,daily",
    "appid": API_KEY,
}

response = requests.get(OWM_API_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()

# TODO: Print "Bring an umbrella." if any of the next twelve hours weather condition code is less then 700.

required_data = data['hourly'][0:12]
id_s = [data['weather'][0]['id'] for data in required_data if data['weather'][0]['id'] < 700]
will_rain = False

for data in required_data:
    if data['weather'][0]['id'] < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body = "It will Rain. Take an umbrella. Be cool, patient and polite.",
        from_ = my_number,
        to = "+905077801634"
    )
else:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body = "There is no rain today. Be cool, patient and polite.",
        from_ = my_number,
        to = "+905077801634")

print(message.status)
