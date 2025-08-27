import json
import difflib
from datetime import date

# Load the cards database from JSON file (your real card data)
with open("cards_db.json", "r", encoding="utf-8") as infile:
    raw_data = json.load(infile)
cards = raw_data["cards"]  # assuming your JSON root has key "cards"

# Build quick lookup dict for card names, lowercase for forgiving input
name_to_card = {card["name"].lower(): card for card in cards}


def find_card_by_name(name):
    name_lower = name.lower()
    if name_lower in name_to_card:
        return name_to_card[name_lower]
    else:
        close = difflib.get_close_matches(name_lower, name_to_card.keys(), n=1)
        if close:
            print(f"Did you mean '{close[0]}'? Using that instead.")
            return name_to_card[close[0]]
        else:
            raise ValueError(f"Card '{name}' not found in database.")


def input_deck():
    deck = []
    print("Type the exact card names, one by one (8 cards total):")
    for i in range(8):
        while True:
            try:
                name = input(f"Card {i+1}: ").strip()
                card = find_card_by_name(name)
                deck.append(
                    {
                        "id": card["id"],
                        "cost": card["cost"],
                        "level": card["level"],
                        "rarity": card["rarity"],
                    }
                )
                break
            except ValueError as e:
                print(e)
                print("Try again.")
    return deck


def main():
    deck_name = input("Enter a name for this deck: ").strip()
    deck_cards = input_deck()
    creator = input("Deck creator (Digger, Gabe, Otacon, INTERNET...): ").strip()
    today = date.today().isoformat()

    deck_entry = {
        "deck_name": deck_name,
        "date": today,
        "creator": creator,
        "cards": deck_cards,
    }

    try:
        with open("decks.json", "r", encoding="utf-8") as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    existing.append(deck_entry)

    with open("decks.json", "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4)

    print(f"Deck '{deck_name}' saved to decks.json")


if __name__ == "__main__":
    main()
