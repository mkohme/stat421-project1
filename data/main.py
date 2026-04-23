import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression

# Reading in the datasets
weather = pd.read_csv("weather_data.csv")
traffic = pd.read_csv("traffic_data.csv")

print(weather.head())
print(traffic.head())

# ----- WEATHER DATA -----

# Convert these columns to numbers (turns bad values into NaN)
weather["temperature_c"] = pd.to_numeric(weather["temperature_c"], errors="coerce")
weather["humidity"] = pd.to_numeric(weather["humidity"], errors='coerce')
weather["wind_kph"] = pd.to_numeric(weather["wind_kph"], errors='coerce')

# Replace any NaNs with the median of each column
weather["temperature_c"] = weather["temperature_c"].fillna(weather["temperature_c"].median())
weather["humidity"] = weather["humidity"].fillna(weather["humidity"].median())
weather["wind_kph"] = weather["wind_kph"].fillna(weather["wind_kph"].median())

# Clean the weather condition text (lowercase + remove extra spaces)
weather["condition"] = weather["condition"].str.lower().str.strip()

# ----- TRAFFIC DATA -----

# Convert timestamp column into real datetime values
traffic["timestamp"] = pd.to_datetime(traffic["timestamp"], errors="coerce")

# Removes rows where the timestamp is missing
traffic = traffic.dropna(subset=['timestamp'])

# Converting the column values into numbers
traffic["current_speed"] = pd.to_numeric(traffic["current_speed"], errors="coerce")
traffic["free_flow_speed"] = pd.to_numeric(traffic["free_flow_speed"], errors="coerce")
traffic["confidence"] = pd.to_numeric(traffic["confidence"], errors="coerce")

# Converting bad values with median
traffic["current_speed"] = traffic["current_speed"].fillna(traffic["current_speed"].median())
traffic["free_flow_speed"] = traffic["free_flow_speed"].fillna(traffic["free_flow_speed"].median())
traffic["confidence"] = traffic["confidence"].fillna(traffic["confidence"].median())

# Creating new columns (date, hour, day of the week)
traffic["date"] = traffic["timestamp"].dt.date
traffic["hour"] = traffic["timestamp"].dt.hour
traffic["day_of_week"] = traffic["timestamp"].dt.day_of_week

# Rush hour indicator
# 0 --> Not rush hour
# 1 -->  Is rush hour
traffic["rush_hour"] = traffic["hour"].isin([7, 8, 9, 16, 17, 18]).astype(int)

# Congestion column
# Free‑flow speed = how fast cars move with no traffic
# If car moves less then 70% of the free flow speed --> suggest congestion
# 0 --> traffic is normal
# 1 --> traffic is congested
traffic["congestion"] = (traffic["current_speed"] < 0.7 * traffic["free_flow_speed"]).astype(int)

# ----- MERGE WEATHER + TRAFFIC -----

# Create the a weather date column 
# The csv file doesn't have a date column, so I just used today's date as a placeholder.
weather["date"]= pd.to_datetime("today").date()

# Merge the traffic and weather on the date column
merged = pd.merge(traffic, weather, on="date", how="left")

# Creates new columns for each condition (sunny, rainy, overcast) and is filled with 0 and 1
# 0 --> No
# 1 --> Yes
merged = pd.get_dummies(merged, columns=["condition"], prefix="cond")







