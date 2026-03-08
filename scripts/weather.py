import requests
import pandas as pd

API_KEY = "c6b239d8073b4049919201349260803 "

city = "Richmond"

url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"

response = requests.get(url)
data = response.json()

print(data)

weather_data = {
    "city": data["location"]["name"],
    "temperature_c": data["current"]["temp_c"],
    "humidity": data["current"]["humidity"],
    "wind_kph": data["current"]["wind_kph"],
    "condition": data["current"]["condition"]["text"]
}

df = pd.DataFrame([weather_data])

df.to_csv("data/weather_data.csv", index=False)

print(df)

