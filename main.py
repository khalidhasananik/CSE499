import requests
import pandas as pd
from datetime import datetime, timedelta

# Constants
API_KEY = '8d41c409cd23d12b1a4a75903dc66503'
BASE_URL = "http://api.openweathermap.org/data/2.5/onecall/timemachine"
CITIES = [
    {"name": "Bagerhat", "lat": 22.6516, "lon": 89.7857},
    # Add more cities with lat and lon here
]
YEARS = [2024]  # Add years you want to retrieve data for

# Function to fetch weather data for a given location and time
def get_weather_data(lat, lon, dt):
    url = f"{BASE_URL}?lat={lat}&lon={lon}&dt={dt}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to extract monthly weather data
def get_monthly_weather_data(city, year):
    data = {"City": city['name'], "Year": year}
    for month in range(1, 13):  # Loop over 12 months
        monthly_temps = []
        monthly_min_temps = []
        monthly_humidity = []
        monthly_sunshine = []
        monthly_rainfall = []
        monthly_cloud = []
        monthly_wind_speeds = []
        days_in_month = (datetime(year, month % 12 + 1, 1) - timedelta(days=1)).day

        for day in range(1, days_in_month + 1):  # Loop over all days of the month
            date = datetime(year, month, day)
            timestamp = int(date.timestamp())
            weather_data = get_weather_data(city['lat'], city['lon'], timestamp)
            if weather_data:
                # Extract relevant data
                temp = weather_data['current']['temp']
                min_temp = weather_data['current'].get('temp_min', temp)  # Some APIs do not provide min temp separately
                humidity = weather_data['current']['humidity']
                sunshine = weather_data['current'].get('sunshine', 0)  # Sunshine may not be directly available
                rainfall = weather_data['current'].get('rain', {}).get('1h', 0)  # Rainfall over the last hour
                cloud = weather_data['current']['clouds']
                wind_speed = weather_data['current']['wind_speed']

                monthly_temps.append(temp)
                monthly_min_temps.append(min_temp)
                monthly_humidity.append(humidity)
                monthly_sunshine.append(sunshine)
                monthly_rainfall.append(rainfall)
                monthly_cloud.append(cloud)
                monthly_wind_speeds.append(wind_speed)

        # Calculate average values for each metric
        if monthly_temps and monthly_min_temps and monthly_humidity:
            data[f'MaxTemp - {datetime(year, month, 1).strftime("%b")}'] = sum(monthly_temps) / len(monthly_temps)
            data[f'MinTemp - {datetime(year, month, 1).strftime("%b")}'] = sum(monthly_min_temps) / len(monthly_min_temps)
            data[f'Humidity - {datetime(year, month, 1).strftime("%b")}'] = sum(monthly_humidity) / len(monthly_humidity)
            data[f'Sunshine - {datetime(year, month, 1).strftime("%b")}'] = sum(monthly_sunshine) / len(monthly_sunshine)
            data[f'Rainfall - {datetime(year, month, 1).strftime("%b")}'] = sum(monthly_rainfall) / len(monthly_rainfall)
            data[f'Cloud - {datetime(year, month, 1).strftime("%b")}'] = sum(monthly_cloud) / len(monthly_cloud)
            data[f'Wind - {datetime(year, month, 1).strftime("%b")}'] = sum(monthly_wind_speeds) / len(monthly_wind_speeds)
        else:
            # Fill with None if no data was available for the month
            data[f'MaxTemp - {datetime(year, month, 1).strftime("%b")}'] = None
            data[f'MinTemp - {datetime(year, month, 1).strftime("%b")}'] = None
            data[f'Humidity - {datetime(year, month, 1).strftime("%b")}'] = None
            data[f'Sunshine - {datetime(year, month, 1).strftime("%b")}'] = None
            data[f'Rainfall - {datetime(year, month, 1).strftime("%b")}'] = None
            data[f'Cloud - {datetime(year, month, 1).strftime("%b")}'] = None
            data[f'Wind - {datetime(year, month, 1).strftime("%b")}'] = None

    return data

# Generate data for all cities and years
final_data = []
for city in CITIES:
    for year in YEARS:
        monthly_data = get_monthly_weather_data(city, year)
        final_data.append(monthly_data)

# Convert to DataFrame and save to CSV
df = pd.DataFrame(final_data)
df.to_csv('weather_data.csv', index=False)
print("Weather data has been successfully saved to 'weather_data.csv'.")
