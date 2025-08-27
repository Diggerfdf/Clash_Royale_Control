import json
import os


def load_cards(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict) and "cards" in data:
            return data["cards"]
        elif isinstance(data, list):
            return data
        else:
            print(f"[ERROR] Unrecognized format in {file_path}")
            return []


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved merged data to {file_path}")


def merge_cards(base_cards, player_cards):
    player_lookup = {card["id"]: card for card in player_cards}

    merged_cards = []
    for base_card in base_cards:
        merged_card = base_card.copy()
        player_card = player_lookup.get(base_card["id"])

        if player_card:
            # Inject player-specific data
            merged_card["level"] = player_card.get("level", 1)
            merged_card["evolution"] = player_card.get("evolution", False)
            merged_card["tags"] = player_card.get("tags", [])
        else:
            # Default values if player doesn't have the card
            merged_card["level"] = 0
            merged_card["evolution"] = False
            merged_card["tags"] = []

        merged_cards.append(merged_card)

    return merged_cards


def main():
    base_path = os.path.join("..", "data", "cards_base.json")
    player_path = os.path.join("..", "data", "players_data", "digger_db.json")
    output_path = os.path.join("..", "data", "players_data", "digger_merged.json")

    base_cards = load_cards(base_path)
    player_cards = load_cards(player_path)

    merged_cards = merge_cards(base_cards, player_cards)

    save_json(merged_cards, output_path)


if __name__ == "__main__":
    main()
