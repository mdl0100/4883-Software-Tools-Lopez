"""
Marcos Lopez 
Assignment - A05 - Family Tree

This program takes in the dwarf_family_tree.json file and creates a .dot file and a family tree visualization of the 
"""

import json
import graphviz
from rich import print


with open('./dwarf_family_tree.json', 'r') as f:
    family = json.load(f)


family_int = {}
for key, person in family.items():
    family_int[int(key)] = person
    person['clan'] = int(person['clan'])
    person['parentId1'] = int(person['parentId1']) if person['parentId1'] else None
    person['parentId2'] = int(person['parentId2']) if person['parentId2'] else None
    person['spouseId'] = int(person['spouseId']) if person['spouseId'] != '' else -1
    person['gender'] = 0 if person['gender'] == "M"  else 1

print(family_int)

clans = ['Stonehammer', 'Ironbeard', 'Deepforge', 'Thunderpeak', 'Silveraxe', 'Frostbeard', 'Boulderfist', 'Fireheart', 'Goldhammer', 'Swiftsteel']
shapes = ['oval', 'egg']
colors = ['0000ff', '00ffff', '00ff00', 'ff00ff', 'ff9900', 'ffff00', 'ffffff', '660099', '996600', '336633']


dot = graphviz.Digraph(comment="The Dwarven Realm")
for key, person in family_int.items():
    fname = person['fname']
    lname = person['lname']
    gender = person['gender']
    dot.node(str(key), f'{fname} {lname}')

print(dot.source)
