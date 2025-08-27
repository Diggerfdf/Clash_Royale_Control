import os
import json

# Get the absolute path to the root project folder, no matter where script is run from
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

MAIN_DB_PATH = os.path.join(PROJECT_ROOT, "data", "cards_db.json")
BASE_DB_PATH = os.path.join(PROJECT_ROOT, "data", "cards_base.json")
PLAYER_DB_PATH = os.path.join(PROJECT_ROOT, "data", "players_data", "digger_db.json")


def split_card_database():
    if not os.path.exists(MAIN_DB_PATH):
        print(f"[ERROR] Cannot find main DB file: {MAIN_DB_PATH}")
        return

    with open(MAIN_DB_PATH, "r", encoding="utf-8") as f:
        full_data = json.load(f)

    if "cards" not in full_data:
        print(f"[ERROR] Invalid format: expected a 'cards' key at root.")
        return

    all_cards = full_data["cards"]
    base_cards = []
    player_cards = []

    for card in all_cards:
        # Shared info
        base_cards.append(
            {
                "id": card["id"],
                "name": card["name"],
                "cost": card["cost"],
                "type": card["type"],
                "rarity": card["rarity"],
            }
        )

        # Player-specific info
        player_cards.append(
            {
                "id": card["id"],
                "level": card.get("level", 1),
                "evolution": card.get("evolution", False),
                "tags": card.get("tags", []),
            }
        )

    with open(BASE_DB_PATH, "w", encoding="utf-8") as f:
        json.dump({"cards": base_cards}, f, indent=2, ensure_ascii=False)

    with open(PLAYER_DB_PATH, "w", encoding="utf-8") as f:
        json.dump({"cards": player_cards}, f, indent=2, ensure_ascii=False)

    print(f"[OK] Split completed!")
    print(f"  → Base cards:      {BASE_DB_PATH}")
    print(f"  → Digger's cards:  {PLAYER_DB_PATH}")


if __name__ == "__main__":
    split_card_database()
