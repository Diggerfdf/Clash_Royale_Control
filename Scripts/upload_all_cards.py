import json
from pathlib import Path
from pymongo import MongoClient, UpdateOne

# ---------------- CONFIG ----------------
MONGO_URI = (
    "mongodb+srv://diggerfdf:Mnemosine2501@cluster0.ro0c4tj.mongodb.net/"
    "?retryWrites=true&w=majority&appName=Cluster0"
)
DB_NAME = "clash_royale_manager"

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
# ----------------------------------------

UPSERT = True  # True = update existing docs instead of skipping


def upload_file(file_path, db):
    collection_name = file_path.stem
    collection = db[collection_name]

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    operations = []
    if isinstance(data, list):
        for doc in data:
            if UPSERT:
                operations.append(
                    UpdateOne({"id": doc.get("id")}, {"$set": doc}, upsert=True)
                )
            else:
                if collection.count_documents({"id": doc.get("id")}, limit=1) == 0:
                    operations.append(
                        UpdateOne({"id": doc.get("id")}, {"$set": doc}, upsert=True)
                    )
    else:
        if UPSERT:
            operations.append(
                UpdateOne({"id": data.get("id")}, {"$set": data}, upsert=True)
            )
        else:
            if collection.count_documents({"id": data.get("id")}, limit=1) == 0:
                operations.append(
                    UpdateOne({"id": data.get("id")}, {"$set": data}, upsert=True)
                )

    if operations:
        result = collection.bulk_write(operations)
        print(
            f"[{collection_name}] Upserted {result.upserted_count} documents, modified {result.modified_count}."
        )
    else:
        print(f"[{collection_name}] Nothing to do.")


def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    json_files = list(DATA_DIR.rglob("*.json"))  # recursively find all JSONs
    if not json_files:
        print("No JSON files found!")
        return

    for file_path in json_files:
        upload_file(file_path, db)


if __name__ == "__main__":
    main()
