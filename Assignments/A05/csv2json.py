import csv
import json
from rich import print
import random

data = {}
with open ('./familyData/dwarf_family_tree.csv') as f:
    csvRead = csv.DictReader(f)
    for rows in csvRead:
        key = rows["#pid"]
        data[key] = rows

clans = ['Stonehammer', 'Ironbeard', 'Deepforge', 'Thunderpeak', 'Silveraxe', 'Frostbeard', 'Boulderfist', 'Fireheart', 'Goldhammer', 'Swiftsteel']
fnameQMale = []
fnameQFemale = []
lnameQ = []
namingDict = {}
with open('./familyData/mockaroo_family_tree_2.csv') as f:
    csvRead = csv.DictReader(f)
    for rows in csvRead:
        key = rows["id"]
        namingDict[key] = rows
    for id in namingDict:
        person = namingDict[id]
        if person['gender'] == "Male":
            fnameQMale.append(person['first_name'])
        else:
            fnameQFemale.append(person['first_name'])
        lnameQ.append(person['last_name'])

finalDict = {}
for id in data:
    person = data[id]
    person["fname"] = fnameQMale.pop() if person['gender'] == 'M' else fnameQFemale.pop()
    person["lname"] = lnameQ.pop()
    person.pop('name', None)
    person.pop('generation', None)
    person.pop('myear', None)
    person.pop('mage', None)
    person.pop('ptype', None)
    person.pop('parentNodeId', None)
    person.pop('#pid', None)
    


with open('./familyData/dwarf_family_tree.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=4))

