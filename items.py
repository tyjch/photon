import json
from pprint import pprint

json_uri = 'items.json'
items = json.load(open(json_uri))

localized_names = [i['LocalizedNames'] for i in items]

item_dict = {i['UniqueName']: i['LocalizedNames'][0]['Value'] if i['LocalizedNames'] else None for i in items}