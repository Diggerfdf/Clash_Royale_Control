import json
from pymongo import MongoClient
from pathlib import Path

# -------------Connection Config---------------
MONGO_URI = ("mongodb+srv://diggerfdf:Mnemosine2501@cluster0.ro0c4tj.mongodb.net/"
            "?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = "clash_royale_manager"
COLLECTION_NAME = "cards"

# Directory Config
BASE_DIR = Path(__file__).parent.parent  # parent of Scripts/
JSON_FILE = BASE_DIR / "data" / "cards_base.json"

# ----------------------------------


def main():
    # connect to Atlas
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # load JSON
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # insert into collection
    if isinstance(data, list):
        result = collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} documents.")
    else:
        result = collection.insert_one(data)
        print(f"Inserted 1 document with id {result.inserted_id}")

if __name__ == "__main__":
    main()
