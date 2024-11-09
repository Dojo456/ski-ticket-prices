import os
import firebase_admin
from firebase_admin import firestore as firebase_firestore
from google.cloud import firestore

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.

database_id = os.getenv("FIRESTORE_DATABASE_ID")

if not database_id:
    raise ValueError("FIRESTORE_DATABASE_ID is not set")

app = firebase_admin.initialize_app()

db = firestore.Client(database=database_id)

# Collection references
locations_collection = db.collection("locations")
prices_collection = db.collection("prices")
