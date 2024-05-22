import requests
import json
from datetime import date
from datetime import timedelta

# Base url for the api requests
base_url = "http://api.weatherapi.com/v1/history.json"

# Insert your api key here
api_key = "63e386ae70db4cc0bad120657242205"


def get_forecast(city: str, iso_date: str) -> str:
    """
    Get forecast for the given city and date
    :param city: city name in english
    :param iso_date: date in iso format
    :return: json string with forecast data
    """
    try:
        request_string = "{}?api_key={}&dt={}&q={}".format(base_url, api_key, iso_date, city)
        request = requests.request("GET", request_string)
    except Exception as e:
        print(e)
        exit()

    try:
        assert request.status_code == 200
    except AssertionError:
        print("Request status: {}".format(request.status_code))
        print("Request contents: {}".format(request.content))
        exit()
    else:
        return request.text


def parse_forecast(data: str) -> float | None:
    """
    Parse forecast data and return average temperature
    :param data: json string with forecast data
    :return: average temperature or None if data is invalid
    """
    try:
        json_data = json.loads(data)

        day = json_data["forecast"]["forecastday"][0]["day"]
        avg_temp = day["avgtemp_c"]
    except Exception as e:
        print(e)
        return None
    else:
        return avg_temp


def get_last_week_average_temp(city: str) -> float:
    """
    Get average temperature over the past seven days
    :param city: city name in english
    :return: average temperature
    """
    today = date.today()
    temp_list = []

    # Weather api doesn't provide a way to get forecast for the past seven days using a single request for basic plan
    # So we have to make seven requests to get the forecast for each day

    # Get iso dates for the past seven days including today
    last_week = [(today - timedelta(days=i)).isoformat() for i in range(7)]

    for day in last_week:
        temp = parse_forecast(get_forecast(city, day))
        if temp is not None:
            temp_list.append(temp)

    try:
        assert len(temp_list) > 0
    except AssertionError:
        print("Not enough data")
        exit()
    else:
        return sum(temp_list) / len(temp_list)


if __name__ == "__main__":

    city = input("To get average temperature over the past seven days please enter city name in english: ")
    avarage_temp = get_last_week_average_temp(city)
    print("Average temperature over the past seven days in {} is: {} °Celsius".format(city, round(avarage_temp, 1)))


