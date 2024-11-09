from template import *


class JayPeak(Template):
    @property
    @override
    def name(self) -> str:
        return "Jay Peak"

    @override
    def make_request(self) -> dict[str, Any]:
        import requests

        url = "https://book.jaypeakresort.com/Ecomm/JSON/ActivityCalendar/"

        payload = "salesId=8101337&supplierId=&productCategoryId=117&days=1&ageCategory=8&startMonth=12&startYear=2024&numberMonths=1&packageId=&packageComponentId=&language=en-US&destination="
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "PostmanRuntime/7.42.0",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()

    @override
    def parse_data(self, data: dict) -> PydanticCalendar:
        prices = data

        return PydanticCalendar(
            location_name=self.name,
            dates=[
                PydanticDatePrice(
                    price=price["Price"],
                    location_name=self.name,
                    date=datetime.datetime.strptime(price["Date"], "%Y-%m-%d"),
                )
                for price in prices
                if price["Price"]
            ],
        )
