import datetime
import typing

import pydantic
import database


class PydanticFromResort(pydantic.BaseModel):
    resort_name: str


class PydanticResort(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    name: str

    def to_orm(self) -> database.Resort:
        return database.Resort(name=self.name)


class PydanticLiftTicket(PydanticFromResort, pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    date: datetime.date
    price: int

    def to_orm(self) -> database.LiftTicket:
        return database.LiftTicket(
            resort_name=self.resort_name, date=self.date, price=self.price
        )


class PydanticCalendar(PydanticFromResort, pydantic.BaseModel):
    dates: list[PydanticLiftTicket]
