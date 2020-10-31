import json
import numpy as np

with open("betterIntents.json") as f:
    data = json.load(f)

new_data = []

for intent in data["intents"]:
    if not new_data:
        print(intent)
    datum = {}
    datum["tag"] = intent["intent"]
    datum["patterns"] = intent["text"]
    datum["responses"] = intent["responses"]
    datum["context"] = [""]
    new_data.append(datum)

intent = {}
intent['intents'] = new_data

filename = 'test_conversation.json'
json_obj = json.dumps(intent, indent = 4)

with open(filename, 'w',) as outfile:
	outfile.write(json_obj)
