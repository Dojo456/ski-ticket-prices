import os
import pathlib
from types import ModuleType
import datetime


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

    # Insert resorts
    for resort_name in resorts.keys():
        resort_ref = database.resorts_collection.document(resort_name)
        resort_ref.set({"name": resort_name}, merge=True)

    # Insert lift tickets
    batch = database.db.batch()
    batch_count = 0
    max_batch_size = 500  # Firestore batch limit

    for calendar in resorts.values():
        for ticket in calendar.dates:
            # Create a unique ID for each ticket document
            ticket_id = f"{ticket.resort_name}_{ticket.date.isoformat()}"
            ticket_ref = database.tickets_collection.document(ticket_id)

            ticket_data = {
                "resort_name": ticket.resort_name,
                "date": ticket.date.isoformat(),  # Use datetime instead of date
                "price": ticket.price,
            }

            batch.set(ticket_ref, ticket_data, merge=True)
            batch_count += 1

            # Commit batch when it reaches the limit
            if batch_count >= max_batch_size:
                batch.commit()
                batch = database.db.batch()
                batch_count = 0

    # Commit any remaining documents in the final batch
    if batch_count > 0:
        batch.commit()
