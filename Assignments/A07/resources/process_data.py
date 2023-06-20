import json

with open('./airports-better.json') as f:
    airports = json.load(f)
    countries = []
    cities = []
    compare = ()
    for i in len(airports):
        cities.append(f'')