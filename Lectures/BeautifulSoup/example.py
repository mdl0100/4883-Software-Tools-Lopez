from bs4 import BeautifulSoup
import requests
from rich import print

# url = "https://www.nba.com/stats"
# response = requests.get(url)
# html_content = response.content

# print(html_content)

# with open('nba_stats.html', 'w') as f:
#   f.write(html_content.decode('utf-8'))

with open('nba_stats.html') as f:
  html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
statCat = soup.find_all("h2", {"class": "LeaderBoardCard_lbcTitle___WI9J"})

# print(statCat[0])

# for statClass in statCat:
#   print(statClass.text)

tbody = soup.find_all("tbody")

i = 0
statDict = {
  "player_stats":{},
  "team_stats":{}
}
for table in tbody:
  category = statCat[i].text.replace(' ', '_')
  # print(category,i)
  if i < 9:
    statDict['player_stats'][category] = []
  else:
    statDict['team_stats'][category] = []
  rows = table.find_all("tr")
  for row in rows:
    cols = row.find_all("td")
    tempData = []
    for col in cols:
      if i < 9:
        name = None
        team = None

        name = col.text[:-3]
        team = col.text[-3:]
        if name:
            tempData.append(name)
        if team:
            tempData.appent(team)

      else:
        print(f"~{col.text}~")
        tempData.append(f"{col.text}")
      statDict['team_stats'][category].append(tempData)
   

    # print("-" * 40)
  i += 1

print(statDict)