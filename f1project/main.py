import requests
import json
from tkinter import *


dsw = None

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

def driver_standings_window():
    global dsw
    if dsw:
        dsw.tkraise()
    else:
        dsw = Tk()
        dsw.title('driver standings')
        dsw.geometry('1000x600')
        my_scroll = Scrollbar(dsw)
        my_scroll.pack(side=RIGHT, fill=Y)


def main_window():
    root = Tk()
    root.title('formula one')
    root.geometry('1200x900')
    my_scroll = Scrollbar(root)
    my_scroll.pack(side=RIGHT, fill=Y)
    button_frame = LabelFrame(root, height=400, width=800, bd='5')
    button_frame.pack(side='top')
    exiting = Button(button_frame, text='exit', bd='5', height=20, width=40, command=root.destroy)
    exiting.grid(row=0, column=0, pady=2)
    driver_standings = Button(button_frame, text='driver standings', bd='5', height=20, width=40, command=driver_standings_window)
    driver_standings.grid(row=0, column=1, pady=2)
    race_results = Button(button_frame, text='race results', bd='5', height=20, width=40, command=root.destroy)
    race_results.grid(row=0, column=2, pady=2)
    drivers = Button(button_frame, text='drivers', bd='5', height=20, width=40, command=root.destroy)
    drivers.grid(row=1, column=0, pady=2)
    constructors = Button(button_frame, text='constructors', bd='5', height=20, width=40, command=root.destroy)
    constructors.grid(row=1, column=1, pady=2)
    circuits = Button(button_frame, text='circuits', bd='5', height=20, width=40, command=root.destroy)
    circuits.grid(row=1, column=2, pady=2)
    root.mainloop()

if __name__ == '__main__':
    main_window()