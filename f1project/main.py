import json
import wikipediaapi
from tkinter import *
from tkinter import ttk
from ergast import Ergast
from tk_html_widgets import HTMLScrolledText
from requests.exceptions import ConnectionError


class F1Gui:
    def __init__(self, _root, _database):
        self.root = _root
        self.database = _database
        self.frame = ttk.Frame(self.root, padding="5")
        self.frame.grid(column=0, row=0, sticky=[N, E, S, W])
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.dsw = None
        self.d_frame = None
        self.ds_frame = None
        self.csw = None
        self.csw_frame = None

    def driver_standings_selection(self, event):
        selection = event.widget.curselection()
        if len(selection) != 1:
            return
        # Clear d_frame
        for s in self.d_frame.grid_slaves():
            s.destroy()

        # Get info for the selected driver
        driver = self.database.driver_list[selection[0]]
        driver_key = driver['driverId']
        standings_table = self.database.get_driver_standings(driver_key)

        # Create driver standings frame
        self.ds_frame = ttk.Frame(self.d_frame)
        self.ds_frame.grid(row=0, rowspan=2, column=1, sticky=[N, E, S, W])
        Label(self.ds_frame, text='Year').grid(row=0, column=0)
        Label(self.ds_frame, text='Position').grid(row=0, column=1)
        Label(self.ds_frame, text='Points').grid(row=0, column=2)
        Label(self.ds_frame, text='Wins').grid(row=0, column=3)
        Label(self.ds_frame, text='Constructor').grid(row=0, column=4)
        for i in range(len(standings_table['StandingsLists'])):
            sl = standings_table['StandingsLists'][i]
            Label(self.ds_frame, text=sl['season']).grid(row=i + 1, column=0)
            Label(self.ds_frame, text=sl['DriverStandings'][0]['position']).grid(row=i + 1, column=1)
            Label(self.ds_frame, text=sl['DriverStandings'][0]['points']).grid(row=i + 1, column=2)
            Label(self.ds_frame, text=sl['DriverStandings'][0]['wins']).grid(row=i + 1, column=3)
            Label(self.ds_frame, text=sl['DriverStandings'][0]['Constructors'][0]['name']).grid(row=i + 1, column=4)

        # Create driver summary text
        dst = HTMLScrolledText(self.d_frame, width=70, height=15, padx=10, pady=1)
        dst.set_html(self.get_wikipedia_summary(driver['url'].split('/')[-1]))
        dst.configure(state='disabled')
        dst.grid(row=1, column=0, rowspan=2, sticky=[N, E, S, W])

        # Create season selector
        seasons_list = self.database.get_seasons_for_driver(driver_key)
        seasons_list.reverse()
        selected_season = StringVar()
        selected_season.set(seasons_list[0])
        seasons_menu = ttk.OptionMenu(self.d_frame, selected_season, seasons_list[0], *seasons_list,
                                      command=self.season_selection)
        seasons_menu.grid(row=0, column=0)

    def season_selection(self, selection):
        print('selected'+str(selection))

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
        wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.HTML)
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
            for i in range(3):
                self.d_frame.rowconfigure(i, weight=1)
            for j in range(2):
                self.d_frame.columnconfigure(j, weight=1)
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
        """Create the main menu"""
        self.root.title('Formula One')
        self.root.geometry('850x250')
        button_frame = ttk.LabelFrame(self.frame, text="Main menu")
        button_frame.grid(row=0, column=0, sticky=[N, E, S, W])
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Create the main menu buttons
        style = ttk.Style()
        style.configure('TButton', padding=5, width=40)
        exiting = ttk.Button(button_frame, text='exit', style='TButton', command=root.destroy)
        driver_standings = ttk.Button(button_frame, text='Drivers',
                                      command=self.driver_standings_window)
        race_results = ttk.Button(button_frame, text='race results', style='TButton', command=root.destroy)
        constructors = ttk.Button(button_frame, text='constructors', style='TButton', command=root.destroy)
        circuits = ttk.Button(button_frame, text='circuits', style='TButton', command=self.circuit_window)

        # Place the buttons in the grid
        exiting.         grid(row=0, column=0, pady=2, sticky=[N, E, S, W])
        driver_standings.grid(row=0, column=1, pady=2, sticky=[N, E, S, W])
        race_results.    grid(row=0, column=2, pady=2, sticky=[N, E, S, W])
        constructors.    grid(row=1, column=1, pady=2, sticky=[N, E, S, W])
        circuits.        grid(row=1, column=2, pady=2, sticky=[N, E, S, W])
        for i in range(2):
            button_frame.rowconfigure(i, weight=1)
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
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
    except (json.decoder.JSONDecodeError, ConnectionRefusedError, ConnectionError):
        load_database(database, 'database.bin')

    root = Tk()
    f1Gui = F1Gui(root, database)
    f1Gui.main_window()
