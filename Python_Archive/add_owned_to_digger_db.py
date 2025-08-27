import os
import json


def get_data_file(*path_parts):
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(ROOT_DIR, "data", *path_parts)


def mark_all_cards_owned():
    PLAYER_DB = get_data_file("players_data", "digger_merged.json")

    if not os.path.exists(PLAYER_DB):
        print(f"[ERROR] Cannot find the file: {PLAYER_DB}")
        return

    with open(PLAYER_DB, "r", encoding="utf-8") as f:
        all_cards = json.load(f)

    updated_cards = []
    for card in all_cards:
        new_card = {
            "id": card["id"],
            "level": card["level"],
            "evolution": card.get("evolution", False),
            "owned": True,
            "tags": card.get("tags", []),
        }
        updated_cards.append(new_card)

    output_path = get_data_file("players_data", "digger_merged_owned.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(updated_cards, f, indent=2, ensure_ascii=False)

    print(
        f"[OK] All cards marked as owned (correct order) and saved to:\n → {output_path}"
    )


if __name__ == "__main__":
    mark_all_cards_owned()
