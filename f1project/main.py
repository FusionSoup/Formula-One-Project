import requests
import json

def driver_standings_selection():
    driver = input('driver?')
    year = input('year?, 0 for no year')
    if year == '0':
        table = requests.get("http://ergast.com/api/f1/drivers/"+driver+"/driverStandings.json")
        standings = json.loads(table.content)
        standings_table = standings['MRData']['StandingsTable']
        print(standings_table)
        #for st in standings_table['StandingsLists']:
           # if st['season'] == '2015': # and st['round'] == '18':
        # ds = st['DriverStandings']
        #print(repr(ds))
        #for d in ds:
       #  print(d['Driver']['givenName'])



section = 'driver standings'
if section == 'drivers':
    drivers_selection
if section == 'seasons':
    seasons_selection
if section == 'qualifying':
    qualifying_selection
if section == 'results':
    results_selection
if section == 'driver standings':
    driver_standings_selection
if section == 'constructors':
    constructors_selection
if section == 'races':
    races_selection
if section == 'sprint results':
    sprint_results_selection
if section == 'pit stops':
    pit_stop_selection
if section == 'constructor standings':
    constructor_standings_selection
if section == 'cicuits':
    circuits_selection
if section == 'lap times':
    lap_times_selection
if section == 'constructor results':
    constructor_results_selection


