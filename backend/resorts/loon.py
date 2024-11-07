from models import *

resort_name = "Loon"


def make_request():
    import json

    import requests

    url = "https://shop.loonmtn.com/api/v1/product-variant"

    payload = json.dumps(
        {
            "ProductAttributeValueIds": [877, 882],
            "ProductId": 121,
            "StartDate": "2024-11-09T00:00:00.000Z",
            "EndDate": "2025-05-31T00:00:00.000Z",
        }
    )
    headers = {
        "Content-Type": "application/json-patch+json",
        "Cookie": "ARRAffinity=dfb97241280d443f31b522d16d7899e2aa2745cf57284f3e5139ee42bd7f77e2; ARRAffinitySameSite=dfb97241280d443f31b522d16d7899e2aa2745cf57284f3e5139ee42bd7f77e2",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def main() -> PydanticCalendar:
    data = make_request()

    prices = data["Variants"][0]["DayPriceLists"]

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
