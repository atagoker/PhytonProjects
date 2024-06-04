import requests

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # For temperature in Celsius
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def display_weather(data):
    if data:
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        print(f"Current weather in {city}, {country}:")
        print(f"Temperature: {temp}°C")
        print(f"Condition: {weather}")
    else:
        print("Error retrieving weather data")

def main():
    api_key = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
    city = input("Enter the city name: ")
    weather_data = get_weather(api_key, city)
    display_weather(weather_data)

if __name__ == "__main__":
    main()
