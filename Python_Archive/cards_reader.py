import json

with open("cards_db.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    
print("Card Count: ", len(data["cards"]))

