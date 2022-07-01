import requests
import json

table = requests.get("http://ergast.com/api/f1/drivers/alonso/driverStandings.json")

standings = json.loads(table.content)

#print(standings)
standings_table = standings['MRData']['StandingsTable']
print(standings_table)

for st in standings_table['StandingsLists']:
    print(st)
