import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import json

# Load Your cards_db.json
with open("cards_db.json", "r", encoding="utf-8") as file:
    data = json.load(file)

cards = data["cards"]

# === Filters ===
MIN_COST = 0
MAX_COST = 9  # Elixir cost (e.g., 2)
FILTER_TYPE = ""  # Options: "troop", "spedd", "Building"

# FILTER_RARITY = "rare" or regex on name
FILTER_NAME = ""  # <- Empty = Disabled, fill in "goblin" to search
FILTER_RARITY = (
    ""  # <- Empty = Disabled. Examples "common", "epic", "rare", "Legendary", Champion
)

# === Filter Logic ===
rarity_icons = {"common": "🔵", "rare": "🟠", "epic": "🟣", "legendary": "🌈", "champion": "👑"}

filtered = [
    card
    for card in cards
    if MIN_COST <= card["cost"] <= MAX_COST
    and (FILTER_TYPE == "" or card["type"] == FILTER_TYPE)
    and (FILTER_NAME == "" or FILTER_NAME.lower() in card["name"].lower())
    and (FILTER_RARITY == "" or card["rarity"].lower() == FILTER_RARITY.lower())
]


# === Output ===
header = f"=== Cards with elixir cost from {MIN_COST} to {MAX_COST}"
if FILTER_TYPE:
    header += f", type '{FILTER_TYPE}'"
if FILTER_NAME:
    header += f", name including '{FILTER_NAME}'"
if FILTER_RARITY:
    header += f", and rarity '{FILTER_RARITY}'"
header += " ==="

print(header)


for card in filtered:
    print(
        f"- {card['name']} | cost: {card['cost']} | {rarity_icons[card['rarity']]} {card['rarity']}"
    )


print(f"\ntotal: {len(filtered)} card(s) found.")
