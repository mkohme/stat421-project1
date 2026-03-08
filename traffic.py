import requests
import pandas as pd
import datetime

API_KEY = "HJXDhhgMRpkwzsQMqz3blgHp9HHrrTbi"

lat = 37.5407
lon = -77.4360

url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={API_KEY}"

response = requests.get(url)
data = response.json()

traffic_data = {
    "timestamp": datetime.datetime.now(),
    "current_speed": data["flowSegmentData"]["currentSpeed"],
    "free_flow_speed": data["flowSegmentData"]["freeFlowSpeed"],
    "confidence": data["flowSegmentData"]["confidence"]
}

df = pd.DataFrame([traffic_data])

df.to_csv("data/traffic_data.csv", index=False)

print(df)