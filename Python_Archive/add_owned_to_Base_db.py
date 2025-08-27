import os
import json


def get_data_file(*path_parts):
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(ROOT_DIR, "data", *path_parts)


def add_owned_false_to_base():
    BASE_DB = get_data_file("cards_base.json")

    if not os.path.exists(BASE_DB):
        print(f"[ERROR] Cannot find the base DB file: {BASE_DB}")
        return

    with open(BASE_DB, "r", encoding="utf-8") as f:
        base_data = json.load(f)  # <-- LOAD FULL DICT
        base_cards = base_data["cards"]  # <-- GET THE LIST

    updated_cards = []
    for card in base_cards:
        new_card = {
            "id": card["id"],
            "name": card["name"],
            "cost": card["cost"],
            "type": card["type"],
            "rarity": card["rarity"],
            **{
                k: v
                for k, v in card.items()
                if k not in ("id", "name", "cost", "type", "rarity")
            },
            "owned": False,
        }
        updated_cards.append(new_card)

    output_data = {"cards": updated_cards}
    output_path = get_data_file("cards_base.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(
        f"[OK] Added 'owned: false' to all base cards and saved to:\n → {output_path}"
    )


if __name__ == "__main__":
    add_owned_false_to_base()
