## Libraries
import pandas as pd
import string
import os

## Load data
df= pd.read_csv("raw_data/uk_road_safety_2022.csv",encoding="latin1")

# Convert Date and Time to datetime and specific colums
df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="%d/%m/%Y %H:%M", errors="coerce")
df["hour"] = df["datetime"].dt.hour
df["day"] = df["datetime"].dt.day_name()
df["day_number"] = df["datetime"].dt.dayofweek  # Monday=0
df["month"]= df["datetime"].dt.month
df["year"] = df["datetime"].dt.year

# Mapp conditions to standardise them and applying them to each column

# weather_conditions map
weather_mapping = {
    1: "Fine",
    2: "Rain",
    3: "Snow",
    4: "Fine + Wind",
    5: "Rain + Wind",
    6: "Snow + Wind",
    7: "Fog",
    8: "Other",
    9: "Unknown"
}
# applying map 
df["weather_conditions"] = df["weather_conditions"].map(weather_mapping)

# Creating a group column for simplification
df["weather_conditions_group"] = df["weather_conditions"].replace({
    "Fine": "Fine",
    "Rain": "Rain",
    "Snow": "Snow",
    "Fine + Wind": "Fine",
    "Rain + Wind": "Rain",
    "Snow + Wind": "Snow",
    "Fog": "Fog",
    "Other": "Other",
    "Unknown": "Unknown"
})

light_map = {
    1: "Daylight",
    4: "Dark - lights lit",
    5: "Dark - lights unlit",
    6: "Dark - no lighting",
    7: "Dark - lighting unknown"
}
df["light_conditions"] = df["light_conditions"].map(light_map)

# light_conditions group - column

df["light_conditions_group"] = df["light_conditions"].replace({
    "Daylight": "Day",
    "Dark - lights lit": "Dark",
    "Dark - lights unlit": "Dark",
    "Dark - no lighting": "Dark",
    "Dark - lighting unknown": "Dark"
})

road_surface_map = {
    1: "Dry",
    2: "Wet or damp",
    3: "Snow",
    4: "Frost or ice",
    5: "Flood over 3cm deep",
    6: "Oil or diesel",
    7: "Mud"
}
df["road_surface_conditions"] = df["road_surface_conditions"].map(road_surface_map)

# road_surface_conditions group - column

df["road_surface_conditions_group"] = df["road_surface_conditions"].replace({
    "Dry": "Dry",
    "Wet or damp": "Wet",
    "Snow": "Snow/Ice",
    "Frost or ice": "Snow/Ice",
    "Flood over 3cm deep": "Wet",
    "Oil or diesel": "Hazardous",
    "Mud": "Hazardous"
})
df = df[df["road_surface_conditions_group"]!= "Hazardous"] # removing hazardous road conditions

# Drop missing rows in latitude and longitude
print(df["longitude"].isnull().sum())
print(df["latitude"].isnull().sum())
df = df.dropna(subset=["latitude", "longitude"])

print(df[["longitude", "latitude"]].isnull().sum())

# Map accident severity
accident_severity_map ={
    1: "Fatal",
    2: "Serious",
    3: "Slight"
}

df["accident_severity"] = df["accident_severity"].map(accident_severity_map)


final_cols = [
    "datetime",
    "hour",
    "day",
    "day_number",
    "month",
    "year",
    "weather_conditions",
    "weather_conditions_group",
    "light_conditions",
    "light_conditions_group",
    "road_surface_conditions",
    "road_surface_conditions_group",
    "accident_severity",
    "accident_reference",
    "number_of_vehicles",
    "number_of_casualties",
    "longitude",
    "latitude",
    "speed_limit",
    "urban_or_rural_area"
]

df_final = df[final_cols].copy()

df_final["longitude"] = pd.to_numeric(df_final["longitude"], errors="coerce")
df_final["latitude"] = pd.to_numeric(df_final["latitude"], errors="coerce")

df_final = df_final.dropna(subset=["longitude", "latitude"])


df_final.to_csv(
    "./processed_data/uk_road_safety_sql_ready.csv",
    index=False,
    encoding="utf-8-sig"
)
