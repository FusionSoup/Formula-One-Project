import json
import wikipediaapi
from tkinter import *
from tkinter import ttk
from ergast import Ergast


class F1Gui:
    def __init__(self, root, database):
        self.root = root
        self.database = database
        self.frame = ttk.Frame(self.root, padding="5")
        self.frame.grid(column=0, row=0, sticky=[N, E, W, S])
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.dsw = None
        self.d_frame = None
        self.dsw_frame = None
        self.driver_standings = None
        self.csw = None
        self.csw_frame = None

    def driver_standings_selection(self, event):
        selection = event.widget.curselection()
        if len(selection) != 1:
            return
        for slave in self.dsw_frame.grid_slaves():
            slave.destroy()
        driver_key = self.database.driver_list[selection[0]]['driverId']
        standings_table = self.database.get_driver_standings(driver_key)
        Label(self.dsw_frame, text='Year').grid(row=0, column=0)
        Label(self.dsw_frame, text='Position').grid(row=0, column=1)
        Label(self.dsw_frame, text='Points').grid(row=0, column=2)
        Label(self.dsw_frame, text='Wins').grid(row=0, column=3)
        Label(self.dsw_frame, text='Constructor').grid(row=0, column=4)
        for i in range(len(standings_table['StandingsLists'])):
            sl = standings_table['StandingsLists'][i]
            Label(self.dsw_frame, text=sl['season']).grid(row=i + 1, column=0)
            Label(self.dsw_frame, text=sl['DriverStandings'][0]['position']).grid(row=i + 1, column=1)
            Label(self.dsw_frame, text=sl['DriverStandings'][0]['points']).grid(row=i + 1, column=2)
            Label(self.dsw_frame, text=sl['DriverStandings'][0]['wins']).grid(row=i + 1, column=3)
            Label(self.dsw_frame, text=sl['DriverStandings'][0]['Constructors'][0]['name']).grid(row=i + 1, column=4)

        seasons_list = self.database.get_seasons_for_driver(driver_key)
        seasons_list.reverse()
        selected_season = StringVar()
        seasons_menu = OptionMenu(self.d_frame, selected_season, *seasons_list)
        seasons_menu.grid(row=0, column=0)
        selected_season.set(seasons_list[0])
        # seasons_menu.bind('<<OptionMenuSelect>>', driver_standings_selection)

    def circuit_selection(self, event):
        selection = event.widget.curselection()
        if len(selection) != 1:
            return
        for slave in self.csw_frame.grid_slaves():
            slave.destroy()
        circuit = self.database.circuit_list[selection[0]]
        circuit_key = circuit['circuitId']
        location_text = f"{circuit['circuitName']}, {circuit['Location']['locality']}, {circuit['Location']['country']}"
        wiki_text = self.get_wikipedia_summary(circuit['url'].split('/')[-1])
        Label(self.csw_frame, text=location_text).grid(row=0, column=0)
        Label(self.csw_frame, text=wiki_text, width=80, wraplength=560, ).grid(row=2, column=0)
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

    def get_wikipedia_summary(self, page):
        wiki_wiki = wikipediaapi.Wikipedia('en')
        wiki = wiki_wiki.page(page)
        return wiki.summary

    def driver_standings_window_destroy(self, event):
        self.dsw = None

    def driver_standings_window(self):
        if self.dsw:
            self.dsw.tkraise()
        else:
            self.dsw = Tk()
            self.dsw.title('Drivers')
            self.dsw.geometry('1000x600')
            self.dsw.bind('<Destroy>', self.driver_standings_window_destroy)
            driver_listbox = Listbox(self.dsw, width=30)
            driver_listbox.bind('<<ListboxSelect>>', self.driver_standings_selection)
            my_scroll = Scrollbar(self.dsw, command=driver_listbox.yview)
            driver_listbox.config(yscrollcommand=my_scroll.set)
            my_scroll.pack(side=LEFT, fill=Y)
            driver_listbox.pack(side=LEFT, fill=Y)
            self.d_frame = ttk.Frame(self.dsw)
            self.d_frame.pack(side='right', fill='both')
            self.dsw_frame = ttk.Frame(self.d_frame)
            self.dsw_frame.grid(row=0, column=2)

            for d in database.driver_list:
                driver_listbox.insert('end', d['givenName'] + ' ' + d['familyName'])

    def circuit_window_destroy(self, event):
        self.csw = None

    def circuit_window(self):
        if self.csw:
            self.csw.tkraise()
        else:
            self.csw = Tk()
            self.csw.title('circuit information')
            self.csw.geometry('1000x600')
            self.csw.bind('<Destroy>', self.circuit_window_destroy)
            circuit_listbox = Listbox(self.csw, width=30)
            circuit_listbox.bind('<<ListboxSelect>>', self.circuit_selection)
            my_scroll2 = Scrollbar(self.csw, command=circuit_listbox.yview)
            circuit_listbox.config(yscrollcommand=my_scroll2.set)
            my_scroll2.pack(side=LEFT, fill=Y)
            circuit_listbox.pack(side=LEFT, fill=Y)
            self.csw_frame = ttk.Frame(self.csw)
            self.csw_frame.pack(side='top', fill=NONE, expand=True)
            for c in self.database.circuit_list:
                circuit_listbox.insert('end', c['circuitName'] + ', ' + c['Location']['country'])

    def main_window(self):
        self.root.title('Formula One')
        self.root.geometry('1200x900')
        # my_scroll = ttk.Scrollbar(self.frame)
        # my_scroll.pack(side=RIGHT, fill=Y)
        button_frame = ttk.LabelFrame(self.frame, height=400, width=800)
        button_frame.pack(side='top')
        exiting = ttk.Button(button_frame, text='exit', width=40, command=root.destroy)
        exiting.grid(row=0, column=0, pady=2)
        self.driver_standings = ttk.Button(button_frame, text='Drivers', width=40,
                                           command=self.driver_standings_window)
        self.driver_standings.grid(row=0, column=1, pady=2)
        race_results = ttk.Button(button_frame, text='race results', width=40, command=root.destroy)
        race_results.grid(row=0, column=2, pady=2)
        constructors = ttk.Button(button_frame, text='constructors', width=40, command=root.destroy)
        constructors.grid(row=1, column=1, pady=2)
        circuits = ttk.Button(button_frame, text='circuits', width=40, command=self.circuit_window)
        circuits.grid(row=1, column=2, pady=2)
        root.mainloop()


def save_database(db, filename):
    db.save_to_file(filename)


def load_database(db, filename):
    db.load_from_file(filename)


def get_database_from_web(db):
    db.get_data()


if __name__ == '__main__':
    database = Ergast()
    try:
        # raise json.decoder.JSONDecodeError('blah', 'dgya', 1)
        get_database_from_web(database)
        save_database(database, 'database.bin')
    except (json.decoder.JSONDecodeError, ConnectionRefusedError):
        load_database(database, 'database.bin')

    root = Tk()
    f1Gui = F1Gui(root, database)
    f1Gui.main_window()
