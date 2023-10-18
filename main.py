import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 37.568459
MY_LONG = -84.296791
MY_EMAIL = "zakihorakhsh2028@gmail.com"
PASSWORD = "izbt umrb wxek jfxb"


def is_iss_overhead():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    data = iss_response.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    if MY_LONG-5 <= longitude <= MY_LONG+5 and MY_LAT-5 <= latitude <= MY_LAT+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()["results"]
    sunrise = int(data["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["sunset"].split("T")[1].split(":")[0])

    now = datetime.now().hour
    if now >= sunset or now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="ayoubim@berea.edu",
                msg=f"subject:Look Up!\n\nThe ISS is above you in the sky."
            )
