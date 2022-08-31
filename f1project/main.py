import requests
import json
from tkinter import *


root = Tk()
root.title('formula one')
root.geometry('1920x1920')
myscroll = Scrollbar(root)
myscroll.pack(side=RIGHT, fill=Y)
exit = Button(root, text = 'exit', bd = '110', command = root.destroy)
exit.pack(side='top')
driverstandings = Button(root, text = 'driverstandings', bd = '110', command = root.destroy)
driverstandings.pack(side='top')
raceresults = Button(root, text = 'raceresults', bd = '110', command = root.destroy)
raceresults.pack(side='top')
drivers = Button(root, text = 'drivers', bd = '110', command = root.destroy)
drivers.pack(side='top')
constructors = Button(root, text = 'constructors', bd = '110', command = root.destroy)
constructors.pack(side='top')
circuits = Button(root, text = 'circuits', bd = '110', command = root.destroy)
circuits.pack(side='top')
root.mainloop()


def driver_standings_selection():  #(driver, year)
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


#def driver_selection(driver):
    #total points, race wins, podiums etc
    #image of driver + bio
    #twitter feed of driver account
    driver_standings_selection(driver, year)
    race_results_selection(driver, year)


#def race_results_selection(year, driver, circuit):

#def circuits_selection():
    circuit = userinput(ciruit)
    race_results_selection(0, 0, ciruit)
    #2 image of circuit
    #1 video of circuit if possible
    #twitter feed of circuit account


section = 'driver standings'
if section == 'drivers':
    drivers_selection()
if section == 'seasons':
    seasons_selection()
if section == 'qualifying':
    qualifying_selection()
if section == 'race results':
    race_results_selection()
if section == 'driver standings':
    driver_standings_selection()
if section == 'constructors':
    constructors_selection()
if section == 'races':
    races_selection()
if section == 'sprint results':
    sprint_results_selection()
if section == 'pit stops':
    pit_stop_selection()
if section == 'constructor standings':
    constructor_standings_selection()
if section == 'cicuits':
    circuits_selection()
if section == 'lap times':
    lap_times_selection()
if section == 'constructor results':
    constructor_results_selection()


