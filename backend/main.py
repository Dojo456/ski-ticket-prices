import os
import pathlib
from types import ModuleType

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

import models
import database


def load_resorts() -> dict[str, models.PydanticCalendar]:
    resort_modules: dict[str, ModuleType] = {}

    for path in os.listdir("resorts"):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            path, pathlib.Path(__file__).parent.joinpath("resorts").joinpath(path)
        )

        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            resort_modules[module.__name__[:-3]] = module

    return {v.resort_name: v.main() for v in resort_modules.values()}


if __name__ == "__main__":
    resorts = load_resorts()

    engine = database.connect()

    with Session(engine) as session:
        # Insert resorts using insert().on_conflict_do_nothing()
        for resort in resorts.keys():
            stmt = insert(database.Resort).values(name=resort)
            stmt = stmt.on_conflict_do_nothing(index_elements=["name"])

            session.execute(stmt)

        session.flush()

        # Insert dates using insert().on_conflict_do_nothing()
        for calendar in resorts.values():
            for ticket in calendar.dates:
                orm_ticket = ticket.to_orm()

                stmt = insert(database.LiftTicket).values(
                    resort_name=orm_ticket.resort_name,
                    date=orm_ticket.date,
                    price=orm_ticket.price,
                )
                stmt = stmt.on_conflict_do_update(
                    index_elements=["resort_name", "date"],
                    set_=dict(price=orm_ticket.price),
                )

                session.execute(stmt)

        session.commit()
