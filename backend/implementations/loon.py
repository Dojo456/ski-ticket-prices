import datetime
from typing import Any, override
from template import Template
from models import PydanticCalendar, PydanticDatePrice


class Loon(Template):
    @property
    @override
    def name(self) -> str:
        return "Loon"

    @override
    def make_request(self) -> dict[str, Any]:
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

    @override
    def parse_data(self, data: dict) -> PydanticCalendar:
        prices = data["Variants"][0]["DayPriceLists"]

        return PydanticCalendar(
            location_name=self.name,
            dates=[
                PydanticDatePrice(
                    price=price["InventoryPriceListLevelPriceDollars"],
                    location_name=self.name,
                    date=datetime.datetime.strptime(price["Date"], "%Y-%m-%d"),
                )
                for price in prices
                if price["Price"]
            ],
        )
