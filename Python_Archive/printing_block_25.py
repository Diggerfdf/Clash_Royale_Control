import json

BLOCK_SIZE = 25

with open("cards_db.json", "r", encoding="utf-8") as infile:
    raw_data = json.load(infile)

cards = raw_data["cards"]
total_cards = len(cards)

for start in range(0, total_cards, BLOCK_SIZE):
    end = min(start + BLOCK_SIZE, total_cards)
    print(f"\n=== BLOCK {start // BLOCK_SIZE + 1}: Cards {start + 1} to {end} ===\n")

    block = cards[start:end]
    for card in block:
        print(card)

print(f"\nDone printing {total_cards} cards in blocks of {BLOCK_SIZE}.")
