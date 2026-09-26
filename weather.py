import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

if not api_key:
    raise ValueError("Weather API key not found")

while True:

    city = "1"

    while city.replace(" ", "").isalpha() == False:
        city = input("Enter the city name: ")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=params,
            timeout=5
        )

        response.raise_for_status()

        print("Success!")
        print(response.status_code)

        data = response.json()

        print(
            f"weather in {data['name']}\n"
            f"weather: {data['weather'][0]['description']}\n"
            f"temperature: {data['main']['temp']} °C\n"
            f"feels like: {data['main']['feels_like']} °C\n"
            f"humidity: {data['main']['humidity']}%\n"
            f"wind speed: {data['wind']['speed']} m/s"
        )

    except requests.ConnectionError:
        print("Error: Connection failed")

    except requests.Timeout:
        print("Error: Request timed out")

    except requests.HTTPError as error:

        response = error.response

        if response is None:
            print("Error: HTTP request failed without a response")
            continue

        if response.status_code == 401:
            print("Error: Unauthorized. Check your API key.")

        elif response.status_code == 404:
            print("Error: City not found. Please check the city name.")

        else:
            print(
                f"Error: HTTP error occurred. "
                f"Status code: {response.status_code}"
            )

    if input("Do you want to check another city? (y/n): ").lower() != "y":
        break
