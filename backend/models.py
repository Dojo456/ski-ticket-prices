import datetime
import pydantic


class PydanticFromResort(pydantic.BaseModel):
    resort_name: str


class PydanticLiftTicket(PydanticFromResort, pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    date: datetime.date
    price: int


class PydanticCalendar(PydanticFromResort, pydantic.BaseModel):
    dates: list[PydanticLiftTicket]
