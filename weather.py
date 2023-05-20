import argparse
import json
import sys
from configparser import ConfigParser
from urllib import parse, request, error

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather_data(url):
    try:
        response = request.urlopen(url)
    except error.HTTPError as http_error:
        if http_error.code == 401:  # 401 - Unauthorized
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404:  # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong... ({http_error.code})")
    data = response.read()
    return json.loads(data)


def read_user_cli_args():
    parser = argparse.ArgumentParser(
        description="gets weather and temperature information for a city"
    )
    parser.add_argument(
        "city", nargs="+", type=str, help="enter the city name"
    )
    return parser.parse_args()


def build_weather_query(city_input, imperial=False):

    api_key = __get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&appid={api_key}"
    )
    return url


def __get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]


if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city)
    weather_data = get_weather_data(query_url)
    city = weather_data["name"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    print(f"{city}", end="")
    print(f"\t{weather_description.capitalize()}", end=" ")
    print(f"({temperature}F)")
