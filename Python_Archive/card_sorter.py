import json

with open("cards_db.json", "r", encoding="utf-8") as file:
    data = json.load(file)

cards = data["cards"]

# Sort by card name (case-insensitive)
sorted_cards = sorted(cards, key=lambda c: c["name"].lower())

# Print nicely
print("=== Sorted Cards list===")
for card in sorted_cards:
    print(f"- {card['name']} (ID: {card['id']})")
    