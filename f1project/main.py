import json
import wikipediaapi
from tkinter import *
from ergast import Ergast

global database
dsw = None
csw = None
d_frame = None
dsw_frame = None
csw_frame = None


def driver_standings_selection(event):
    global dsw, d_frame, dsw_frame, database
    selection = event.widget.curselection()
    if len(selection) != 1:
        return
    for slave in dsw_frame.grid_slaves():
        slave.destroy()
    driver_key = database.driver_list[selection[0]]['driverId']
    standings_table = database.get_driver_standings(driver_key)
    Label(dsw_frame, text='Year').grid(row=0, column=0)
    Label(dsw_frame, text='Position').grid(row=0, column=1)
    Label(dsw_frame, text='Points').grid(row=0, column=2)
    Label(dsw_frame, text='Wins').grid(row=0, column=3)
    Label(dsw_frame, text='Constructor').grid(row=0, column=4)
    for i in range(len(standings_table['StandingsLists'])):
        sl = standings_table['StandingsLists'][i]
        Label(dsw_frame, text=sl['season']).grid(row=i + 1, column=0)
        Label(dsw_frame, text=sl['DriverStandings'][0]['position']).grid(row=i + 1, column=1)
        Label(dsw_frame, text=sl['DriverStandings'][0]['points']).grid(row=i + 1, column=2)
        Label(dsw_frame, text=sl['DriverStandings'][0]['wins']).grid(row=i + 1, column=3)
        Label(dsw_frame, text=sl['DriverStandings'][0]['Constructors'][0]['name']).grid(row=i + 1, column=4)

    seasons_list = database.get_seasons_for_driver(driver_key)
    seasons_list.reverse()
    selected_season = StringVar()
    selected_season.set(seasons_list[0])
    seasons_menu = OptionMenu(d_frame, selected_season, *seasons_list)
    seasons_menu.grid(row=0, column=0)
    #seasons_menu.bind('<<OptionMenuSelect>>', driver_standings_selection)


def circuit_selection(event):
    global csw, csw_frame, database
    selection = event.widget.curselection()
    if len(selection) != 1:
        return
    for slave in csw_frame.grid_slaves():
        slave.destroy()
    circuit = database.circuit_list[selection[0]]
    circuit_key = circuit['circuitId']
    location_text = f"{circuit['circuitName']}, {circuit['Location']['locality']}, {circuit['Location']['country']}"
    wiki_text = get_wikipedia_summary(circuit['url'].split('/')[-1])
    Label(csw_frame, text=location_text).grid(row=0, column=0)
    Label(csw_frame, text=wiki_text, width=80, wraplength=560, ).grid(row=2, column=0)
    #Label(dsw_frame, text='Points').grid(row=0, column=2)
    #Label(dsw_frame, text='Wins').grid(row=0, column=3)
    #Label(dsw_frame, text='Constructor').grid(row=0, column=4)
    #for i in range(len(standings_table['StandingsLists'])):
    #    sl = standings_table['StandingsLists'][i]
    #    Label(dsw_frame, text=sl['season']).grid(row=i + 1, column=0)
    #    Label(dsw_frame, text=sl['DriverStandings'][0]['position']).grid(row=i + 1, column=1)
    #    Label(dsw_frame, text=sl['DriverStandings'][0]['points']).grid(row=i + 1, column=2)
    #    Label(dsw_frame, text=sl['DriverStandings'][0]['wins']).grid(row=i + 1, column=3)
    #    Label(dsw_frame, text=sl['DriverStandings'][0]['Constructors'][0]['name']).grid(row=i + 1, column=4)


def get_wikipedia_summary(page):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    wiki = wiki_wiki.page(page)
    return wiki.summary

        # ds = st['DriverStandings']
        #print(repr(ds))
        #for d in ds:
       #  print(d['Driver']['givenName'])


#def driver_selection(driver):
    #total points, race wins, podiums etc
    #image of driver + bio
    #twitter feed of driver account
    #driver_standings_selection(driver, year)
    #race_results_selection(driver, year)


#def race_results_selection(year, driver, circuit):


def driver_standings_window_destroy(event):
    global dsw
    dsw = None


def driver_standings_window():
    global dsw, d_frame, dsw_frame, database
    if dsw:
        dsw.tkraise()
    else:
        dsw = Tk()
        dsw.title('Drivers')
        dsw.geometry('1000x600')
        dsw.bind('<Destroy>', driver_standings_window_destroy)
        driver_listbox = Listbox(dsw, width=30)
        driver_listbox.bind('<<ListboxSelect>>', driver_standings_selection)
        my_scroll = Scrollbar(dsw, command=driver_listbox.yview)
        driver_listbox.config(yscrollcommand=my_scroll.set)
        my_scroll.pack(side=LEFT, fill=Y)
        driver_listbox.pack(side=LEFT, fill=Y)
        d_frame = Frame(dsw,)
        d_frame.pack(side='right', fill='both')
        dsw_frame = Frame(d_frame,)
        dsw_frame.grid(row=0, column=2)

        for d in database.driver_list:
            driver_listbox.insert('end', d['givenName'] + ' ' + d['familyName'])


def circuit_window_destroy(event):
    global csw
    csw = None


def circuit_window():
    global csw, csw_frame, database
    if csw:
        csw.tkraise()
    else:
        csw = Tk()
        csw.title('circuit information')
        csw.geometry('1000x600')
        csw.bind('<Destroy>', circuit_window_destroy)
        circuit_listbox = Listbox(csw, width=30)
        circuit_listbox.bind('<<ListboxSelect>>', circuit_selection)
        my_scroll2 = Scrollbar(csw, command=circuit_listbox.yview)
        circuit_listbox.config(yscrollcommand=my_scroll2.set)
        my_scroll2.pack(side=LEFT, fill=Y)
        circuit_listbox.pack(side=LEFT, fill=Y)
        csw_frame = Frame(csw,)
        csw_frame.pack(side='top', fill=NONE, expand=True)
        for c in database.circuit_list:
            circuit_listbox.insert('end', c['circuitName'] + ', ' + c['Location']['country'])


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
    driver_standings = Button(button_frame, text='Drivers', bd='5', height=20, width=40, command=driver_standings_window)
    driver_standings.grid(row=0, column=1, pady=2)
    race_results = Button(button_frame, text='race results', bd='5', height=20, width=40, command=root.destroy)
    race_results.grid(row=0, column=2, pady=2)
    constructors = Button(button_frame, text='constructors', bd='5', height=20, width=40, command=root.destroy)
    constructors.grid(row=1, column=1, pady=2)
    circuits = Button(button_frame, text='circuits', bd='5', height=20, width=40, command=circuit_window)
    circuits.grid(row=1, column=2, pady=2)
    root.mainloop()


def save_database(db, filename):
    db.save_to_file(filename)


def load_database(db, filename):
    db.load_from_file(filename)


def get_database_from_web(db):
    db.get_data()


if __name__ == '__main__':
    global database
    database = Ergast()
    try:
        # raise json.decoder.JSONDecodeError('blah', 'dgya', 1)
        get_database_from_web(database)
        save_database(database, 'database.bin')
    except (json.decoder.JSONDecodeError, ConnectionRefusedError):
        load_database(database, 'database.bin')
    main_window()
