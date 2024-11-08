import firebase_admin
from firebase_admin import firestore as firebase_firestore
from google.cloud import firestore

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.

app = firebase_admin.initialize_app(options={"database": "ski-ticket-prices"})

db = firestore.Client(database="ski-ticket-prices")

# Collection references
resorts_collection = db.collection("resorts")
tickets_collection = db.collection("lift_tickets")
