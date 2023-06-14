"""
Marcos Lopez 
Assignment - A05 - Family Tree

This program takes in the dwarf_family_tree.json file and creates a .dot file and a family tree visualization of the dwarf families
The clans are color coded, but not grouped by clans. Clans are inherited through the maternal line and through marriage

"""

import json
import graphviz

# load json family tree
with open('./dwarf_family_tree.json', 'r') as f:
    family = json.load(f)

# is a string, we will convert keys and same attributes to integers by making a new dictionary
family_int = {}
for key, person in family.items():
    family_int[int(key)] = person                                                       # enter person into new dictionary
    person['clan'] = int(person['clan'])                                                # Cast clan number to int
    person['parentId1'] = int(person['parentId1']) if person['parentId1'] else None     # Cast parentId1 to int or None
    person['parentId2'] = int(person['parentId2']) if person['parentId2'] else None     # Cast parentId2 to int or None
    person['spouseId'] = int(person['spouseId']) if person['spouseId'] != '' else None  # Cast spouseId to int or None
    person['gender'] = 0 if person['gender'] == "M"  else 1                             # Cast gender to 0 or 1

# clan numbers are associated with the follow clan and will be colored accordingly
clans = ['Stonehammer', 'Ironbeard', 'Deepforge', 'Thunderpeak', 'Silveraxe', 'Frostbeard']
colors = ['aliceblue', 'mediumpurple', 'cornflowerblue', 'gold', 'lightcyan', 'lavenderblush']

# Males will have square nodes, and females will have diamond
shapes = ['square', 'diamond']

# Create diagraph
dot = graphviz.Digraph(comment="The Dwarven Realm", graph_attr={'rankdir': "TB", 'splines': 'curves'})
# Extract Person data to create their node
for key, person in family_int.items():
    parent1 = person['parentId1']
    parent2 = person['parentId2']
    if parent1 != None:
        if family_int[parent1]['gender'] == 1:
            parent1, parent2 = parent2, parent1           
        person['lname'] = family_int[parent1]['lname']  # inherit father's last name
        person['clan'] = family_int[parent2]['clan']    # inherit father's paternal clan

    fname, lname = person['fname'], person['lname']     # First Name, Last Name
    gender = person['gender']                           # Gender
    byear, dyear = person['byear'], person['dyear']     # Birth and Death
    dage = person['dage']                               # Age at death
    spouse = person['spouseId']                         # Id of their Spouse, None if never married
    parent2 = person['parentId2']


    if spouse !=None:                                   # If there is a spouse listed, it's the wife
        clan = clans[family_int[spouse]['clan']]        #   Husband inherits Wife's clan
        fill = colors[family_int[spouse]['clan']]       #   Husband's fillcolor will be updated too
    else:
        clan = clans[person['clan']]                    # Otherwise, keeps orginal clan and color
        fill = colors[person['clan']]
    
    # Create a node that displays all above information on separate lines
    dot.node(str(key), label=f'Name: {fname} {lname}\\nBorn-Died: {byear}-{dyear}\\nAge: {dage}\\nClan: {clan}', shape=shapes[gender], color=fill, style="filled, rounded")
    # connect married people to a ghost node by concatenating their Id numbers and appending an X
    if spouse != None:
        small= min(key,spouse)                          # small Id number
        large = max(key,spouse)                         # large Id number
        nodule = f'{small}{large}X'                     # invisible node will be small + large + X
        sub = f'{small}{large}Z'                        # a subgraph will be made to group married people    
        temp = graphviz.Digraph(sub)                    
        temp.attr(rank="same", rankdir = 'RL')
        temp.node(nodule , shape='point')               # Create node between married couple
        temp.edge(str(key), nodule, arrowhead="None")   # Edge from male to nodule
        temp.edge(nodule, str(spouse), arrowhead="None")# Edge from nodule to female
        dot.subgraph(temp)                              # Cast as subgraph to main graph
    # Connect an edge from parent's marriage to self
    if person['parentId1'] != None:                     
        p1 = min(person['parentId1'], person['parentId2'])
        p2 = max(person['parentId1'], person['parentId2'])
        dot.edge(f'{p1}{p2}X', str(key))

# Write .dot file to make the family tree
with open('./family_tree.dot', 'w') as f:
   f.write(dot.source)