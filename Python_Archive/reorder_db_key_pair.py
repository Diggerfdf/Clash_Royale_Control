import json

preferred_order = ["id", "name", "cost", "level", "evolution", "type", "rarity", "tags"]

with open("cards_db.json", "r", encoding="utf-8") as infile:
    raw_data = json.load(infile)

cards = raw_data["cards"]
corrected_cards = []

for card in cards:
    # Add evolution=false if missing
    if "evolution" not in card:
        card["evolution"] = False

    new_card = {}

    # Add keys in preferred order
    for key in preferred_order:
        if key in card:
            new_card[key] = card[key]

    # Add any extra keys at the end
    for key in card:
        if key not in preferred_order:
            new_card[key] = card[key]

    corrected_cards.append(new_card)

with open("db_corrected.json", "w", encoding="utf-8") as outfile:
    json.dump({"cards": corrected_cards}, outfile, indent=2, ensure_ascii=False)

print("Done. db_corrected.json created with reordered keys and evolution flags.")
