from models import *

resort_name = "Jay Peak"


def make_request():
    import requests

    url = "https://book.jaypeakresort.com/Ecomm/JSON/ActivityCalendar/"

    payload = "salesId=8101337&supplierId=&productCategoryId=117&days=1&ageCategory=8&startMonth=12&startYear=2024&numberMonths=1&packageId=&packageComponentId=&language=en-US&destination="
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "PostmanRuntime/7.42.0",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def main() -> PydanticCalendar:
    data = make_request()

    prices = data

    return PydanticCalendar(
        resort_name=resort_name,
        dates=[
            PydanticLiftTicket(
                price=price["Price"],
                resort_name=resort_name,
                date=datetime.datetime.strptime(price["Date"], "%Y-%m-%d"),
            )
            for price in prices
            if price["Price"]
        ],
    )
