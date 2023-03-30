import json
import wikipediaapi
from tkinter import *
from tkinter import ttk
from ergast import Ergast
from tk_html_widgets import HTMLScrolledText
from requests.exceptions import ConnectionError
from PIL import ImageTk
import PIL
from simulation import *
import matplotlib.pyplot as plt
import math


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
        self.driver_key = None
        self.s_frame = None
        self.csw = None
        self.csw_frame = None
        self.c_frame = None
        self.circuit_key = None
        self.ssw = None
        self.rrw = None
        self.rrw_frame = None
        self.year = None
        self.cw = None
        self.cw_frame = None
        self.ct_frame = None
        self.constructor_key = None

    def driver_standings_selection(self, event):
        """Add widgets to screen once a driver has been selected"""
        selection = event.widget.curselection()
        if len(selection) != 1:
            return
        # Clear d_frame
        for s in self.d_frame.grid_slaves():
            s.destroy()

        # Get info for the selected driver
        driver = self.database.driver_list[selection[0]]
        self.driver_key = driver['driverId']
        standings_table = self.database.get_driver_standings(self.driver_key)

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

        # Load the image
        driver_name = driver['givenName'] + driver['familyName']
        try:
            im = PIL.Image.open(f'C:\\Work\\Formula-One-Project\\f1project\\drivers\\{driver_name}.jpg')
            im.resize((200, 200), PIL.Image.Resampling.BILINEAR)
            img = ImageTk.PhotoImage(im)
        except FileNotFoundError:
            img = None
        # Create a label widget with the image
        driver_image_label = Label(self.d_frame, image=img, text='No image')
        # Display the label widget
        driver_image_label.grid(row=2, column=1, sticky=[N, E, S, W])

        # Create season frame
        self.s_frame = ttk.Frame(self.d_frame)
        self.s_frame.grid(row=0, column=0, sticky=[N, E, S, W])

        # Create season selector
        seasons_list = self.database.get_seasons_for_driver(self.driver_key)
        seasons_list.reverse()
        selected_season = StringVar()
        selected_season.set(seasons_list[0])
        seasons_menu = ttk.OptionMenu(self.s_frame, selected_season, seasons_list[0], *seasons_list,
                                      command=self.driver_season_selection)
        seasons_menu.grid(row=0, column=0, columnspan=4)

    def driver_season_selection(self, selection):
        # Clear s_frame rows 1-end
        for s in self.s_frame.grid_slaves():
            if s.grid_info()['row'] > 0:
                s.destroy()
        results = self.database.get_driver_results_for_season(self.driver_key, selection)
        for i in range(len(results)):
            for j in range(len(results[i]) - 1):
                label = ttk.Label(self.s_frame, text=results[i][j])
                label.grid(column=j, row=i + 1)
                # Clicking on this row takes the user to that race
                label.bind('<Button-1>',
                           lambda evt, year=selection, circuit=results[i][-1]: self.circuit_click(year, circuit))

    def race_click(self, year, circuit_id):
        self.race_results_window(selected_year=year)

    def circuit_click(self, year, circuit_id):
        self.circuit_window(selected_circuit=circuit_id)

    def circuit_selection(self, event):
        selection = event.widget.curselection()
        if len(selection) != 1:
            return
        for slave in self.csw_frame.grid_slaves():
            slave.destroy()
        circuit = self.database.circuit_list[selection[0]]
        circuit_info = HTMLScrolledText(self.csw_frame, width=70, height=15, padx=10, pady=1)
        circuit_info.set_html(self.get_wikipedia_summary(circuit['url'].split('/')[-1]))
        circuit_info.configure(state='disabled')
        circuit_info.grid(row=1, column=0, rowspan=2, sticky=[N, E, S, W])

        # Create circuit season frame
        self.c_frame = ttk.Frame(self.csw_frame)
        self.c_frame.grid(row=0, column=0, sticky=[N, E, S, W])
        self.circuit_key = circuit['circuitId']
        seasons_list = self.database.get_seasons_for_circuit(self.circuit_key)
        seasons_list.reverse()
        selected_season = StringVar()
        if len(seasons_list) > 0:
            seasons_menu = ttk.OptionMenu(self.csw_frame, selected_season, seasons_list[0], *seasons_list,
                                          command=self.circuit_season_selection)
            seasons_menu.grid(row=0, column=0, columnspan=4)
            selected_season.set(seasons_list[0])

    def circuit_season_selection(self, selection):
        for s in self.c_frame.grid_slaves():
            if s.grid_info()['row'] > 0:
                s.destroy()
        results = self.database.get_circuit_results_for_season(self.circuit_key, selection)
        for i in range(len(results)):
            for j in range(2):
                label = ttk.Label(self.c_frame, text=results[i][j], name=results[i][-1] + str(j))
                label.grid(column=j, row=i + 1)
                # Clicking on this row takes the user to that race
                label.bind('<Button-1>',
                           lambda evt, year=selection, driver=results[i][2]: self.circuit_driver_click(evt, year, driver))

    def circuit_driver_click(self, evt, year, driver_id):
        self.driver_standings_window(selected_driver=driver_id)

    def get_wikipedia_summary(self, page):
        try:
            wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.HTML)
            wiki = wiki_wiki.page(page).summary
        except Exception:
            wiki = 'Wikipedia offline'
        return wiki

    def driver_standings_window_destroy(self, event):
        self.dsw = None

    def driver_standings_window(self, selected_driver=None):
        if self.dsw:
            self.dsw.tkraise()
        else:
            self.dsw = Toplevel()
            self.dsw.title('Drivers')
            self.dsw.geometry('1700x900')
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
            for i in range(len(self.database.driver_list)):
                if selected_driver == self.database.driver_list[i]['driverId']:
                    driver_listbox.select_set([i])
                    driver_listbox.event_generate('<<ListboxSelect>>')

    def circuit_window_destroy(self, event):
        self.csw = None

    def circuit_window(self, selected_circuit=None):
        if self.csw:
            self.csw.tkraise()
        else:
            self.csw = Toplevel()
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
            for i in range(len(self.database.circuit_list)):
                if selected_circuit == self.database.circuit_list[i]['circuitId']:
                    circuit_listbox.select_set([i])
                    circuit_listbox.event_generate('<<ListboxSelect>>')

    def simulation_window_destroy(self, event):
        self.ssw = None

    def simulation_window(self):
        cars = get_cars('2018', self.database)
        race = Race(cars)
        race.simulate()
        race.display_results('racesimulationgame')
        if self.ssw:
            self.ssw.tkraise()
        else:
            self.ssw = Toplevel()
            self.ssw.title('Simulation Game')
            self.ssw.geometry('1700x1000')
            self.ssw.bind('<Destroy>', self.simulation_window_destroy)
        # Add a Text widget to display the contents of the text file
        text_widget = Text(self.ssw)
        text_widget.pack(fill=BOTH, expand=YES)

        # Open the text file and read its contents into the Text widget
        with open('racesimulationgame', 'r') as f:
            contents = f.read()
            text_widget.insert(END, contents)

    def race_results_window(self, selected_year=None):
        if self.rrw:
            self.rrw.tkraise()
        else:
            self.rrw = Toplevel()
            self.rrw.title('race results')
            self.rrw.geometry('1000x600')
            self.rrw.bind('<Destroy>', self.race_results_window_destroy)
            years_listbox = Listbox(self.rrw, width=30)
            years_listbox.bind('<<ListboxSelect>>', self.year_selection)
            scroller = Scrollbar(self.rrw, command=years_listbox.yview)
            years_listbox.config(yscrollcommand=scroller.set)
            scroller.pack(side=LEFT, fill=Y)
            years_listbox.pack(side=LEFT, fill=Y)
            self.rrw_frame = ttk.Frame(self.rrw)
            self.rrw_frame.pack(side='top', fill=NONE, expand=True)
            years = self.database.year_list
            for c in years:
                years_listbox.insert(END, c)
            for i in range(len(self.database.year_list)):
                if selected_year == self.database.year_list[i]:
                    years_listbox.select_set([i])
                    years_listbox.event_generate('<<ListboxSelect>>')

    def year_selection(self, event):
        selection = event.widget.curselection()
        if len(selection) != 1:
            return
        for slave in self.rrw_frame.grid_slaves():
            slave.destroy()
        self.year = self.database.year_list[selection[0]]
        circuits_list = self.database.get_races_for_season(self.year)
        selected_circuit = StringVar()
        if len(circuits_list) > 0:
            selected_circuit.set(circuits_list[0])
            circuits_menu = ttk.OptionMenu(self.rrw_frame, selected_circuit, circuits_list[0], *circuits_list,
                                           command=self.race_results_selection)
            circuits_menu.grid(row=0, column=0, columnspan=4)

    def race_results_selection(self, selection):
        for s in self.rrw_frame.grid_slaves():
            if s.grid_info()['row'] > 0:
                s.destroy()
        circuit_id = ''
        for c in self.database.circuit_list:
            if c['circuitName'] == selection:
                circuit_id = c['circuitId']
                break
        ttk.Label(self.rrw_frame, text='Position')    .grid(column=0, row=1)
        ttk.Label(self.rrw_frame, text='Driver')      .grid(column=1, row=1)
        ttk.Label(self.rrw_frame, text='Constructor') .grid(column=2, row=1)
        ttk.Label(self.rrw_frame, text='Fastest lap') .grid(column=3, row=1)
        ttk.Label(self.rrw_frame, text='FL Avg Speed').grid(column=4, row=1)
        ttk.Label(self.rrw_frame, text='Points')      .grid(column=5, row=1)
        ttk.Label(self.rrw_frame, text='Grid')        .grid(column=6, row=1)
        ttk.Label(self.rrw_frame, text='Status')      .grid(column=7, row=1)
        results = self.database.get_race_results(circuit_id, self.year)
        for i in range(len(results)):
            for j in range(len(results[i]) - 1):
                label = ttk.Label(self.rrw_frame, text=results[i][j])
                label.grid(column=j, row=i + 2)
                # Clicking on the driver takes the user to that window
                if j == 1:
                    label.bind('<Button-1>',
                               lambda evt, driver=results[i][-1]: self.race_driver_click(evt, driver))
                if j == 3:
                    label.bind('<Button-1>',
                               lambda evt, driver_id=results[i][-1], driver_name=results[i][1], circuit_id=circuit_id,
                               circuit_name=selection, year=self.year:
                               self.plot_lap_times(driver_id, driver_name, circuit_id, circuit_name, year))
                    # TODO: Set labels to blue and underlined

    def race_driver_click(self, evt, driver_id):
        self.driver_standings_window(selected_driver=driver_id)

    def race_results_window_destroy(self, event):
        self.rrw = None

    @staticmethod
    def convert_to_float(lap_time_str):
        minutes, seconds = lap_time_str.split(":")
        seconds, millis = seconds.split(".")
        return float(minutes) * 60 + float(seconds) + float(millis) / 1000

    def convert_to_int(self, fllap):
        fllap = fllap
        int_max = round(float(max(fllap)), -1)
        return int_max

    def plot_lap_times(self, driver_id, driver_name, circuit_id, circuit_name, year):
        """ Plots a list of lap times on a graph using Matplotlib."""
        lap_time_list = database.get_list_of_lap_times(year, driver_id, circuit_id)

        # Convert lap time list to seconds
        for i in range(len(lap_time_list)):
            lap_time_list[i] = self.convert_to_float(lap_time_list[i])

        # Get the maximum and minimum lap times
        max_lap_time = max(lap_time_list)
        min_lap_time = min(lap_time_list)

        # Set x values as indices of the numbers_list
        x_values = range(len(lap_time_list))

        # Create a new figure and axis
        fig, ax = plt.subplots()

        # Plot the numbers as a line graph
        ax.plot(x_values, lap_time_list)

        # Set the y-tick values to be 5-second intervals from min to max lap time
        first_y_tick = int(5 * math.floor(min_lap_time / 5))
        last_y_tick = int(5 * math.ceil(max_lap_time / 5))
        ax.set_yticks(range(first_y_tick, last_y_tick, 5))

        ax.set_xlabel('Lap number')
        ax.set_ylabel('Lap time (seconds)')
        ax.set_title(f'{driver_name}, {circuit_name}, {year}')

        # Show the plot
        plt.show()

    def constructors_window(self):
        if self.cw:
            self.cw.tkraise()
        else:
            self.cw = Toplevel()
            self.cw.title('Constructor information')
            self.cw.geometry('1000x600')
            self.cw.bind('<Destroy>', self.constructors_window_destroy)
            constructors_listbox = Listbox(self.cw, width=30)
            constructors_listbox.bind('<<ListboxSelect>>', self.constructors_selection)
            my_scroll2 = Scrollbar(self.cw, command=constructors_listbox.yview)
            constructors_listbox.config(yscrollcommand=my_scroll2.set)
            my_scroll2.pack(side=LEFT, fill=Y)
            constructors_listbox.pack(side=LEFT, fill=Y)
            self.cw_frame = ttk.Frame(self.cw)
            self.cw_frame.pack(side='top', fill=NONE, expand=True)
            for c in self.database.constructor_list:
                constructors_listbox.insert('end', f"{c['name']} ({c['nationality']})")

    def constructors_window_destroy(self, event):
        self.cw = None

    def constructors_selection(self, event):
        selection = event.widget.curselection()
        if len(selection) != 1:
            return
        for slave in self.cw_frame.grid_slaves():
            slave.destroy()
        constructor = self.database.constructor_list[selection[0]]
        constructor_info = HTMLScrolledText(self.cw_frame, width=70, height=15, padx=10, pady=1)
        constructor_info.set_html(self.get_wikipedia_summary(constructor['url'].split('/')[-1]))
        constructor_info.configure(state='disabled')
        constructor_info.grid(row=1, column=0, rowspan=2, sticky=[N, E, S, W])

        # Create circuit season frame
        self.ct_frame = ttk.Frame(self.cw_frame)
        self.ct_frame.grid(row=0, column=0, sticky=[N, E, S, W])
        self.constructor_key = constructor['constructorId']

        seasons_list = self.database.get_seasons_for_constructor(self.constructor_key)
        seasons_list.reverse()
        selected_season = StringVar()
        if len(seasons_list) > 0:
            seasons_menu = ttk.OptionMenu(self.ct_frame, selected_season, seasons_list[0], *seasons_list,
                                          command=self.constructor_season_selection)
            seasons_menu.grid(row=0, column=0, columnspan=5)
            selected_season.set(seasons_list[0])

    def constructor_season_selection(self, selection):
        for s in self.ct_frame.grid_slaves():
            if s.grid_info()['row'] > 0:
                s.destroy()
        results = self.database.get_constructor_results_for_season(self.constructor_key, selection)
        for i in range(len(results)):
            for j in range(5):
                label = ttk.Label(self.ct_frame, text=results[i][j])
                label.grid(column=j, row=i + 1)
                # Clicking on this row takes the user to that race
                label.bind('<Button-1>',
                           lambda evt, year=selection, circuit=results[i][5]: self.race_click(evt, year, circuit))

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
        exiting = ttk.Button(button_frame, text='Exit', style='TButton', command=root.destroy)
        driver_standings = ttk.Button(button_frame, text='Drivers',
                                      command=self.driver_standings_window)
        race_results = ttk.Button(button_frame, text='Race Results', style='TButton', command=self.race_results_window)
        constructors = ttk.Button(button_frame, text='Constructors', style='TButton', command=self.constructors_window)
        circuits = ttk.Button(button_frame, text='Circuits', style='TButton', command=self.circuit_window)
        simulation_game = ttk.Button(button_frame, text='Simulation Game', style='TButton', command=self.simulation_window)
        # Place the buttons in the grid
        exiting.         grid(row=0, column=0, pady=2, sticky=[N, E, S, W])
        driver_standings.grid(row=0, column=1, pady=2, sticky=[N, E, S, W])
        race_results.    grid(row=0, column=2, pady=2, sticky=[N, E, S, W])
        constructors.    grid(row=1, column=1, pady=2, sticky=[N, E, S, W])
        circuits.        grid(row=1, column=2, pady=2, sticky=[N, E, S, W])
        simulation_game. grid(row=1, column=0, pady=2, sticky=[N, E, S, W])
        for i in range(2):
            button_frame.rowconfigure(i, weight=1)
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
        self.root.mainloop()


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

