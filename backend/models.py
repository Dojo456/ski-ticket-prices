import datetime
import pydantic


class PydanticFromLocation(pydantic.BaseModel):
    location_name: str


class PydanticDatePrice(PydanticFromLocation, pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    date: datetime.date
    price: int


class PydanticCalendar(PydanticFromLocation, pydantic.BaseModel):
    dates: list[PydanticDatePrice]
