"""
Marcos Lopez
csv2json.py

This program serves to take the dwarf_family_tree.csv in ./familyData/ and convert it to a useable JSON file for the family tree assignment. 
The names of the dwarfs are changed in the process using the mockaroo_family_tree_2.csv file as the new names
The irrelevant keys from dwarf_family_tree.csv are stripped out of the dictionary
The improved dictionary is then exported as a json file using dumps, meaning that it'll be a string


A few notes about this file:
    - dwarf_family_tree.csv is read in and parsed into a dictionary
    - mockaroo_family_tree_2.csv is read in and parsed into a dictionary
        - 3 name stacks are created to hold last name, male first names, and female first names. 
    - the family dictionary is updated with the new names using the stacks

"""

import csv
import json
from rich import print

# Open dwarf_family_tree.csv and convert its contents to a Python dictionary
data = {}
with open ('./familyData/dwarf_family_tree.csv') as f:
    csvRead = csv.DictReader(f)
    for rows in csvRead:
        key = int(rows["#pid"])
        data[key] = rows

# Create 3 stacks for Male first names, Female First Names, and Last Names to replace the Dwarf names in data
fnameMaleStack = []
fnameFemaleStack = []
lnameStack = []

# Open the mockaroo data and extract male/female first names and last names
namingDict = {}
with open('./familyData/mockaroo_family_tree_2.csv') as f:
    csvRead = csv.DictReader(f)
    for rows in csvRead:
        key = rows["id"]
        namingDict[key] = rows
    # push names to the the correct stacks based on gender
    for id in namingDict:
        person = namingDict[id]
        if person['gender'] == "Male":
            fnameMaleStack.append(person['first_name'])
        else:
            fnameFemaleStack.append(person['first_name'])
    #last names of every person to added to the last name stack
        lnameStack.append(person['last_name'])

# Add in new first and last names for each person using the stacks
for id in data:
    person = data[id]
    person["fname"] = fnameMaleStack.pop() if person['gender'] == 'M' else fnameFemaleStack.pop()
    person["lname"] = lnameStack.pop()
    #Delete each unncessary attribute from the dictionary
    person.pop('name', None)        #dwarf's name deleted
    person.pop('generation', None)  #generate number deleted
    person.pop('myear', None)       #marriage year deleted
    person.pop('mage', None)        #marriage age deleted
    person.pop('ptype', None)       #personality type deleted
    person.pop('parentNodeId', None)#parentNodeId deleted
    person.pop('#pid', None)        #pid deleted, since it's also serving as the key for the dictionary


# export data as a json string dictionary using dumps
with open('./dwarf_family_tree.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=4))