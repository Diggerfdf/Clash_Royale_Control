import json
import os
import sys

# --- Config ---
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS_BASE_PATH = os.path.join(BASE_PATH, "data", "cards_base.json")
PLAYER_NAME = "otacon"
PLAYER_DB_PATH = os.path.join(BASE_PATH, "data", "players_data", f"{PLAYER_NAME}.json")

# --- CLI Flags ---
CONTINUE_MODE = "--continue" in sys.argv


# --- Load Functions ---
def load_cards_base():
    with open(CARDS_BASE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("cards", [])


def load_existing_player_cards():
    if not os.path.exists(PLAYER_DB_PATH):
        return []
    with open(PLAYER_DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("cards", [])


# --- Save Function ---
def save_player_db(player_name, player_cards):
    players_dir = os.path.join(BASE_PATH, "data", "players_data")
    os.makedirs(players_dir, exist_ok=True)

    path = os.path.join(players_dir, f"{player_name}.json")
    output = {"player": player_name, "cards": player_cards}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)


# --- Input Helpers ---
def get_tags_input(card_name):
    raw_tags = input(
        f"  -> Tags for {card_name}? (comma-separated, optional): "
    ).strip()
    return (
        [tag.strip() for tag in raw_tags.split(",") if tag.strip()] if raw_tags else []
    )


# --- Main ---
def main():
    cards_base = load_cards_base()
    existing_player_cards = load_existing_player_cards()

    try:
        existing_ids = {
            card["id"] for card in existing_player_cards if isinstance(card, dict)
        }
    except Exception:
        print("⚠️ Failed to parse existing player cards.")
        existing_ids = set()

    # Map existing player cards by id for quick update
    updated_cards = {c["id"]: c for c in existing_player_cards}
    history = []

    # Determine starting index for continue mode
    start_index = 0
    if CONTINUE_MODE and existing_player_cards:
        # Find index of last saved card in cards_base
        last_card_id = existing_player_cards[-1]["id"]
        # Find the position in cards_base for last_card_id, then start after that
        for i, card in enumerate(cards_base):
            if card.get("id") == last_card_id:
                start_index = i + 1
                break

    print("\n--- Clash Royale Card Collection Input ---")
    print(f"📂 Continue Mode: {'ON' if CONTINUE_MODE else 'OFF'}")
    print("💡 Type level (e.g. 12) if owned, press ENTER to skip.")
    print("   z = undo last, s = save, q = save & quit.\n")

    index = start_index
    while index < len(cards_base):
        card = cards_base[index]
        card_id = card.get("id", f"card_{index}")
        card_name = card.get("name", card_id)

        # In continue mode, skip cards already in updated_cards
        if CONTINUE_MODE and card_id in updated_cards:
            index += 1
            continue

        # Ask for level
        level_input = (
            input(f"{card_name} (level / Enter=skip / z=undo / s=save / q=quit): ")
            .strip()
            .lower()
        )

        # Undo
        if level_input == "z":
            if history:
                index = history.pop()
                # Also remove last updated card if any
                if index < len(cards_base):
                    last_card = cards_base[index]
                    last_id = last_card.get("id")
                    if last_id in updated_cards:
                        del updated_cards[last_id]
                continue
            else:
                print("⚠️ Nothing to undo.")
                continue

        # Save progress & keep going
        if level_input == "s":
            save_player_db(PLAYER_NAME, list(updated_cards.values()))
            print("💾 Progress saved.")
            continue

        # Save progress & quit
        if level_input == "q":
            save_player_db(PLAYER_NAME, list(updated_cards.values()))
            print("💾 Progress saved. 👋 Quitting...")
            return

        # Skip if blank
        if not level_input:
            history.append(index)
            index += 1
            continue

        # Parse level
        try:
            level = int(level_input)
        except ValueError:
            print("  !! Invalid level input. Please enter a number.")
            continue

        # Evolution
        evolution = False
        if card.get("can_evolve", False):
            evo_input = (
                input(f"  -> Evolution unlocked for {card_name}? (y/N): ")
                .strip()
                .lower()
            )
            evolution = evo_input == "y"

        # Tags
        tags = get_tags_input(card_name)

        # Update DB entry
        entry = {"id": card_id, "level": level}
        if card.get("can_evolve", False):
            entry["evolution"] = evolution
        if tags:
            entry["tags"] = tags

        updated_cards[card_id] = entry

        history.append(index)
        index += 1

    # Save at the end
    save_player_db(PLAYER_NAME, list(updated_cards.values()))
    print(f"\n✅ Player DB saved to {PLAYER_DB_PATH}")
    print(f"🧾 Total cards owned: {len(updated_cards)}")


if __name__ == "__main__":
    main()
