from django.conf import settings
import requests


def timezone_api(latitude: float, longitude: float) -> dict:
    """
    Returns the TimezoneDb API response containing timezone details
    """
    response = requests.get(
        "https://api.timezonedb.com/v2.1/get-time-zone?key="
        f"{settings.TIMEZONE_API_KEY}&format=json&by=position"
        f"&lat={latitude}&lng={longitude}"
    )
    response_dict = response.json()
    return response_dict


def get_timezone(latitude: float, longitude: float) -> str:
    """
    To get the timezone of the place on the basis of the geo-coordinates.

    params: latitude and longitude of the place
    returns: name of timezone e.g., Asia/Kolkata.
    """
    response_dict = timezone_api(latitude, longitude)
    timezone_name = response_dict["zoneName"]
    return timezone_name


if __name__ == "__main__":

    import os, sys

    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microfarm.settings")
    import django

    django.setup()

    latitude = float(input("Enter latitude: "))
    longitude = float(input("Enter longitude: "))

    print(get_timezone(latitude, longitude))
