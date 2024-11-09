import os
import pathlib
from dotenv import load_dotenv
from template import Template

load_dotenv()

import models
import database


def load_data() -> dict[str, models.PydanticCalendar]:
    implementations: dict[str, Template] = {}

    for path in os.listdir("implementations"):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            path,
            pathlib.Path(__file__).parent.joinpath("implementations").joinpath(path),
        )

        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            if module.__name__ == "template":
                continue

            for name, cls in module.__dict__.items():
                if (
                    isinstance(cls, type)
                    and cls != Template
                    and issubclass(cls, Template)
                ):
                    implementations[name] = cls()

    return {v.name: v.parse_data(v.make_request()) for v in implementations.values()}


if __name__ == "__main__":
    data = load_data()

    # Insert resorts
    for name in data.keys():
        locations_ref = database.locations_collection.document(name)
        locations_ref.set({"name": name}, merge=True)

    # Insert lift tickets
    batch = database.db.batch()
    batch_count = 0
    max_batch_size = 500  # Firestore batch limit

    for calendar in data.values():
        for date in calendar.dates:
            # Create a unique ID for each date document
            date_id = f"{date.location_name}_{date.date.isoformat()}"
            date_ref = database.prices_collection.document(date_id)

            date_data = {
                "location_name": date.location_name,
                "date": date.date.isoformat(),  # Use datetime instead of date
                "price": date.price,
            }

            batch.set(date_ref, date_data, merge=True)
            batch_count += 1

            # Commit batch when it reaches the limit
            if batch_count >= max_batch_size:
                batch.commit()
                batch = database.db.batch()
                batch_count = 0

    # Commit any remaining documents in the final batch
    if batch_count > 0:
        batch.commit()
