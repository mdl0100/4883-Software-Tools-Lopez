import json
from json import load, loads, dump, dumps
from rich import print
import random


def createOrgFile():
  with open("dwarf_family_tree.json") as f:
    #data = json.loads(f.read())
    data = json.load(f)
  clanDict = {}

  for p in data:
    if not p['clanName'] in clanDict:
      clanDict[p['clanName']]= []
      
    clanDict[p['clanName']].append(p)

  print(clanDict)
  for clan,clanList in clanDict.items():
    print(f"{clan}: size:{len(clanList)}")



if __name__ == '__main__':
  createOrgFile()

# # load = loads a string file to  an object
# # loads = loads a string to an object
# # dump = write a string to a file
# # dumps = write a json object to a string



# # for person in data:
# #   print(person['clanName'])

# print(data[100])

# with open("dwarf2.json", 'w') as f:
#   json.dump(data, f, indent=4, sort_keys=True)




# L = [[1,2,3],[6,7,8],[88,99,77,101,777]]

# print(L)

# for row in L:
#   for item in row:
#     print(item,end=" ")
#   print()

# print()
# person =  {
#     "id": "0",
#     "generation": "0",
#     "fname": "Gustavus",
#     "lname": "Banfill",
#     "gender": "M",
#     "birthDate": "7/21/1701",
#     "deathDate": "2/9/1767",
#     "age": 66,
#     "marriedYear": "1719",
#     "marriedAge": "18",
#     "personality": "ESTP",
#     "clanName": "Blacksteel",
#     "spouseId": "",
#     "fatherId": "",
#     "motherId": "",
#     "parentNodeId": "-1"
# }
# print()

# for kv in person:
#   print(kv,person[kv])

# keys = person.keys()

# print(keys)

# for k,v in person.items():
#   print(k,"=",v)

# xy = (random.randint(1,99),random.randint(1,99))

# print(xy)

# x,y = xy

# print(x,"---",y)
