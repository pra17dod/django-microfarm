from django.conf import settings
from django.utils.timezone import now
import datetime
import requests
import re


class WateringRequired:
    """
    WateringRequired creates a instance of the user-provided parameters required to
    to check if watering is required or not.
    """

    def __init__(
        self,
        start_week: int,
        end_week: int,
        if_rain: bool,
        last_watered_at: datetime.datetime,
        lower_temp: float,
        max_hours_for_next_rain: int,
        min_hours_gap_btw_watering: int,
        latitude: float,
        longitude: float,
        timezone: str,
    ):
        """
        Constructs a new WateringRequired of user-provided parameters.
        """

        self.start_week = int(start_week)
        self.end_week = int(end_week)
        self.if_rain = bool(if_rain)
        self.last_watered_at = last_watered_at
        self.lower_temp = float(lower_temp)
        self.max_hours_for_next_rain = int(max_hours_for_next_rain)
        self.min_hours_gap_btw_watering = int(min_hours_gap_btw_watering)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.timezone = str(timezone)

    def weather_api(self) -> requests.models.Response:
        """
        Returns Weather API response.
        """

        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}"
            f"&lon={self.longitude}&units=metric&appid={settings.WEATHER_API_KEY}"
        )
        return response

    def forecast_api(self) -> requests.models.Response:
        """
        Returns Forecast API response.
        """

        response = requests.get(
            "https://pro.openweathermap.org/data/2.5/forecast/hourly?"
            f"lat={self.latitude}&lon={self.longitude}&units=metric&"
            f"cnt={self.max_hours_for_next_rain}&appid={settings.FORECAST_API_KEY}"
        )
        return response

    def time_diff_in_hours(
        self, to_time: datetime.datetime, from_time: datetime.datetime
    ) -> int:
        """
        Returns time difference of datetime.datetime format times in hours.
        """

        delta = abs(to_time - from_time)
        return int(delta.days * 24 + delta.seconds / 3600.0)

    def is_current_week_in_range(self) -> bool:
        """
        Checks if current week number is in the range of start week and end week.

        returns: A boolean about today is in week range or not.
        """

        current_week = datetime.date.today().isocalendar()[1]
        return current_week in range(self.start_week, self.end_week + 1)

    def weather_now(self) -> tuple:
        """
        Checks if it is going to rain using the Weather API.

        returns: A boolean about it is raining or not and current temperature.
        """

        weather_response = self.weather_api()
        weather_data = weather_response.json()
        weather = weather_data["weather"][0]["main"].lower()
        current_temp = weather_data["main"]["temp"]
        return (bool(re.search("rain", weather)), current_temp)

    def will_rain(self) -> bool:
        """
        Checks if it is going to rain in next hours, (here, 'hours' are the 'max hours
        for next rain') using the Forecast API.

        returns: A boolean about it is going to rain or not.
        """

        forecast_response = self.forecast_api()
        forecast_data = forecast_response.json()
        forecast = ""
        for record in forecast_data["list"]:
            forecast += f"{(record['weather'][0]['main']).lower()} "
        return bool(re.search("rain", forecast))

    def watering_required(self) -> tuple:
        """
        Checks if watering required or not, based on current week, last-time
        watered at, current weather and weather forecast.

        returns: A tuple of boolean of watering required or not and reason for
                 the same.
        """

        if not self.is_current_week_in_range():
            return (False, f"Today not in Watering Period")
        else:
            last_watered_time_diff = self.time_diff_in_hours(
                now(), self.last_watered_at
            )
            if last_watered_time_diff < self.min_hours_gap_btw_watering:
                return (False, f"Watered {last_watered_time_diff} hours ago")
            else:
                is_raining_now, current_tmp = self.weather_now()
                if current_tmp <= self.lower_temp:
                    return (False, f"Current temp. is {current_tmp} deg. C")
                else:
                    if is_raining_now:
                        return (self.if_rain, f"It is raining")
                    else:
                        if self.will_rain():
                            return (
                                self.if_rain,
                                f"It will rain in next {self.max_hours_for_next_rain} hours",
                            )
                        else:
                            return (
                                True,
                                f"Its not raining and also will not rain in next {self.max_hours_for_next_rain} hours",
                            )


if __name__ == "__main__":

    import os, sys

    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microfarm.settings")
    import django

    django.setup()

    # Example Input: 10 48 False 2021 6 27 14 48 17 4 21.77 77.15
    start_week = int(input("Enter start week: "))
    end_week = int(input("Enter end week: "))
    if_rain = bool(input("If raining then watering? (True/False): "))
    year, month, day, hour, minute, second = list(
        map(int, input("Enter datetime (Y M D H M S): ").split(" "))
    )
    last_watered_at = datetime.datetime(year, month, day, hour, minute, second).replace(
        tzinfo=datetime.timezone.utc
    )
    lower_temp = float(input("Enter lower temp below which watering not needed: "))
    max_hours_for_next_rain = int(input("Enter max hours for next rain: "))
    min_hours_gap_btw_watering = int(input("Enter min hours gap between watering: "))
    latitude = float(input("Enter latitude: "))
    longitude = float(input("Enter longitude: "))
    timezone = str(input("Enter timezone name e.g., Asia/Kolkata: "))

    watering_rule = WateringRequired(
        start_week,
        end_week,
        if_rain,
        last_watered_at,
        lower_temp,
        max_hours_for_next_rain,
        min_hours_gap_btw_watering,
        latitude,
        longitude,
        timezone,
    )

    print(watering_rule.watering_required())
