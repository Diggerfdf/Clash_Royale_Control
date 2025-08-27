import os
import json

DATA_FOLDER = os.path.join("data", "players_data")


def load_player_decks(player_id):
    filename = f"{player_id.lower()}_decks.json"
    filepath = os.path.join(DATA_FOLDER, filename)

    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            decks = json.load(file)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in file {filepath}: {e}")
        return

    if not decks:
        print(f"[INFO] No decks found for player '{player_id}'.")
        return

    print(f"\n--- Decks for player '{player_id}' ---")
    for i, deck in enumerate(decks, start=1):
        print(f"\nDeck #{i}: {deck['deck_name']}")
        print(f"  Date: {deck['date']}")
        print(f"  Creator: {deck['creator']}")
        print("  Cards:")
        for card in deck["cards"]:
            print(
                f"    - {card['id']} (Lvl {card['level']} | {card['rarity']} | {card['cost']} Elixir)"
            )
    print("\n[OK] All decks loaded successfully.")


if __name__ == "__main__":
    player_id = input("Enter player ID (e.g., digger, gabebot, otacon): ").strip()
    load_player_decks(player_id)
