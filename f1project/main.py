import json  # import the JSON library for handling data
import wikipediaapi  # import the wikipedia API for searching for information
from tkinter import *  # import the tkinter library for creating a GUI
from tkinter import ttk  # import ttk for creating themed widgets
from ergast import Ergast  # import the Ergast library for retrieving Formula 1 data
from tk_html_widgets import HTMLScrolledText  # import the tk_html_widgets for displaying HTML content
from requests.exceptions import ConnectionError  # import the ConnectionError exception for handling connection errors
from PIL import ImageTk  # import the ImageTk module for displaying images in tkinter
import PIL  # import PIL for image manipulation
from simulation import *  # import the simulation module for running simulations
import matplotlib.pyplot as plt  # import the matplotlib library for creating plots
import math  # import math for mathematical operations

class F1Gui:
    def __init__(self, _root, _database):
        self.root = _root  # assign the root window to self.root
        self.database = _database  # assign the database to self.database
        self.frame = ttk.Frame(self.root, padding="5")  # create a themed frame with padding of 5
        self.frame.grid(column=0, row=0, sticky=[N, E, S, W])  # grid the frame to column 0, row 0 and set sticky to all directions
        self.root.columnconfigure(0, weight=1)  # set the weight of column 0 to 1
        self.root.rowconfigure(0, weight=1)  # set the weight of row 0 to 1
        self.dsw = None  # initialize the driver search widget to None
        self.d_frame = None  # initialize the driver frame to None
        self.ds_frame = None  # initialize the driver stats frame to None
        self.driver_key = None  # initialize the driver key to None
        self.s_frame = None  # initialize the standings frame to None
        self.csw = None  # initialize the circuit search widget to None
        self.csw_frame = None  # initialize the circuit search frame to None
        self.c_frame = None  # initialize the circuit frame to None
        self.circuit_key = None  # initialize the circuit key to None
        self.ssw = None  # initialize the season search widget to None
        self.ssw_frame = None  # initialize the season search frame to None
        self.rrw = None  # initialize the race result widget to None
        self.rrw_frame = None  # initialize the race result frame to None
        self.year = None  # initialize the year to None
        self.cw = None  # initialize the constructor widget to None
        self.cw_frame = None  # initialize the constructor frame to None
        self.ct_frame = None  # initialize the constructor stats frame to None
        self.constructor_key = None  # initialize the constructor key to None

    def driver_standings_selection(self, event):
        """Add widgets to screen once a driver has been selected"""
        selection = event.widget.curselection()  # get selected driver
        if len(selection) != 1:  # if not exactly 1 driver selected, return
            return

        # Clear d_frame
        for s in self.d_frame.grid_slaves():
            s.destroy()

        # Get info for the selected driver
        driver = self.database.driver_list[selection[0]]  # get driver data from the database
        self.driver_key = driver['driverId']  # set driver key for later use
        standings_table = self.database.get_driver_standings(self.driver_key)  # get driver standings from the database

        # Create driver standings frame
        self.ds_frame = ttk.Frame(self.d_frame)  # create frame to hold driver standings
        self.ds_frame.grid(row=0, rowspan=2, column=1, sticky=[N, E, S, W])  # set position of frame
        Label(self.ds_frame, text='Year').grid(row=0, column=0)  # add 'Year' label
        Label(self.ds_frame, text='Position').grid(row=0, column=1)  # add 'Position' label
        Label(self.ds_frame, text='Points').grid(row=0, column=2)  # add 'Points' label
        Label(self.ds_frame, text='Wins').grid(row=0, column=3)  # add 'Wins' label
        Label(self.ds_frame, text='Constructor').grid(row=0, column=4)  # add 'Constructor' label
        for i in range(len(standings_table['StandingsLists'])):  # for each year in the driver standings table
            sl = standings_table['StandingsLists'][i]  # get the standings list for that year
            Label(self.ds_frame, text=sl['season']).grid(row=i + 1, column=0)  # add year label
            Label(self.ds_frame, text=sl['DriverStandings'][0]['position']).grid(row=i + 1,
                                                                                 column=1)  # add position label
            Label(self.ds_frame, text=sl['DriverStandings'][0]['points']).grid(row=i + 1, column=2)  # add points label
            Label(self.ds_frame, text=sl['DriverStandings'][0]['wins']).grid(row=i + 1, column=3)  # add wins label
            Label(self.ds_frame, text=sl['DriverStandings'][0]['Constructors'][0]['name']).grid(row=i + 1,
                                                                                                column=4)  # add constructor label

        # Create driver summary text
        dst = HTMLScrolledText(self.d_frame, width=70, height=15, padx=10, pady=1)  # create text widget
        dst.set_html(self.get_wikipedia_summary(driver['url'].split('/')[-1]))  # get driver summary from wikipedia
        dst.configure(state='disabled')  # make text widget uneditable
        dst.grid(row=1, column=0, rowspan=2, sticky=[N, E, S, W])  # set position of text widget

        # Load the image
        driver_name = driver['givenName'] + driver['familyName']  # get driver name
        try:
            im = PIL.Image.open(
                f'C:\\Work\\Formula-One-Project\\f1project\\drivers\\{driver_name}.jpg')  # open driver image file
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
        for s in self.s_frame.grid_slaves():  # iterate through all widgets in s_frame
            if s.grid_info()['row'] > 0:  # if the widget's row is greater than 0 (i.e. not the header row)
                s.destroy()  # destroy the widget
        results = self.database.get_driver_results_for_season(self.driver_key,
                                                              selection)  # get the driver's results for the selected season
        for i in range(len(results)):  # iterate through each race result
            for j in range(
                    len(results[i]) - 1):  # iterate through each column in the race result (excluding the last column)
                label = ttk.Label(self.s_frame, text=results[i][j])  # create a label for the current cell
                label.grid(column=j, row=i + 1)  # place the label in the correct row and column
                # Clicking on this row takes the user to that race
                label.bind('<Button-1>',
                           lambda evt, year=selection, circuit=results[i][-1]: self.circuit_click(year,
                                                                                                  circuit))  # bind a function to the label that will take the user to the selected race when clicked

    def race_click(self, year, circuit_id):
        self.race_results_window(selected_year=year)  # open the race results window for the selected year

    def circuit_click(self, year, circuit_id):
        self.circuit_window(selected_circuit=circuit_id)  # open the circuit window for the selected circuit

    def circuit_selection(self, event):
        selection = event.widget.curselection()  # get the selected circuit from the event widget
        if len(selection) != 1:  # if more than one circuit is selected
            return  # do nothing
        for slave in self.csw_frame.grid_slaves():  # iterate through all widgets in csw_frame
            slave.destroy()  # destroy the widget
        circuit = self.database.circuit_list[selection[0]]  # get the circuit info for the selected circuit
        circuit_info = HTMLScrolledText(self.csw_frame, width=70, height=15, padx=10,
                                        pady=1)  # create a scrolled text widget to display circuit info
        circuit_info.set_html(self.get_wikipedia_summary(circuit['url'].split('/')[
                                                             -1]))  # set the HTML content of the widget to the Wikipedia summary for the selected circuit
        circuit_info.configure(state='disabled')  # disable editing of the widget
        circuit_info.grid(row=1, column=0, rowspan=2,
                          sticky=[N, E, S, W])  # place the widget in the correct row and column, spanning two rows

        # Create circuit season frame
        self.c_frame = ttk.Frame(self.csw_frame)  # create a new frame to display the circuit's seasons
        self.c_frame.grid(row=0, column=0, sticky=[N, E, S, W])  # place the frame in the top-left corner of csw_frame
        self.circuit_key = circuit['circuitId']  # set the circuit key for use in other functions
        seasons_list = self.database.get_seasons_for_circuit(
            self.circuit_key)  # get the seasons in which the circuit was used
        seasons_list.reverse()  # reverse the list to display the most recent seasons first
        selected_season = StringVar()  # create a variable to store the selected season
        if len(seasons_list) > 0:  # if there are seasons to display
            seasons_menu = ttk.OptionMenu(self.csw_frame, selected_season, seasons_list[0], *seasons_list,
                                          command=self.circuit_season_selection)
            seasons_menu.grid(row=0, column=0, columnspan=4)
            selected_season.set(seasons_list[0])

    def circuit_season_selection(self, selection):
        # Destroy all s_frame rows except the first one
        for s in self.c_frame.grid_slaves():
            if s.grid_info()['row'] > 0:
                s.destroy()
        # Get the results for the selected circuit and season
        results = self.database.get_circuit_results_for_season(self.circuit_key, selection)
        # Display the results in the circuit frame
        for i in range(len(results)):
            for j in range(2):
                # Create a label for each result and add it to the circuit frame
                label = ttk.Label(self.c_frame, text=results[i][j], name=results[i][-1] + str(j))
                label.grid(column=j, row=i + 1)
                # Clicking on this row takes the user to the driver standings for the selected driver and season
                label.bind('<Button-1>',
                           lambda evt, year=selection, driver=results[i][2]: self.circuit_driver_click(year, driver))

    def circuit_driver_click(self, year, driver_id):
        # Open the driver standings window for the selected driver and season
        self.driver_standings_window(selected_driver=driver_id)

    def get_wikipedia_summary(self, page):
        try:
            # Create a new Wikipedia API object
            wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.HTML)
            # Get the summary text of the given Wikipedia page
            wiki = wiki_wiki.page(page).summary
        except Exception:
            # If there is an error or the page is not found, return a specific message
            wiki = 'Wikipedia offline'
        # Return the summary text of the Wikipedia page
        return wiki

    def driver_standings_window_destroy(self, event):
        # Set the driver standings window to None, destroying it
        self.dsw = None

    def driver_standings_window(self, selected_driver=None):
        if self.dsw:
            # If the driver standings window exists, raise it to the top
            self.dsw.tkraise()
        else:
            # Create a new driver standings window
            self.dsw = Toplevel()
            # Set the title of the window
            self.dsw.title('Drivers')
            # Set the dimensions of the window
            self.dsw.geometry('1700x900')
            # Bind the destroy event to the driver_standings_window_destroy method
            self.dsw.bind('<Destroy>', self.driver_standings_window_destroy)
            # Create a listbox to display the list of drivers
            driver_listbox = Listbox(self.dsw, width=30)
            # Bind the ListboxSelect event to the driver_standings_selection method
            driver_listbox.bind('<<ListboxSelect>>', self.driver_standings_selection)
            # Create a scrollbar for the listbox
            my_scroll = Scrollbar(self.dsw, command=driver_listbox.yview)
            # Set the scroll command of the scrollbar to the listbox's yview method
            driver_listbox.config(yscrollcommand=my_scroll.set)
            # Pack the scrollbar on the left side of the window and fill the y-axis
            my_scroll.pack(side=LEFT, fill=Y)
            # Pack the listbox on the left side of the window and fill the y-axis
            driver_listbox.pack(side=LEFT, fill=Y)
            # Create a new frame for displaying driver standings
            self.d_frame = ttk.Frame(self.dsw)
            # Pack the frame on the right side of the window and fill both the x and y axes
            self.d_frame.pack(side='right', fill='both')
            # Configure the rows of the frame to be of equal weight
            for i in range(3):
                self.d_frame.rowconfigure(i, weight=1)
            # Configure the columns of the frame to be of equal weight
            for j in range(2):
                self.d_frame.columnconfigure(j, weight=1)
            # Insert the list of drivers into the listbox
            for d in database.driver_list:
                driver_listbox.insert('end', d['givenName'] + ' ' + d['familyName'])
            # If a driver is selected, select the corresponding item in the listbox and generate the ListboxSelect event
            for i in range(len(self.database.driver_list)):
                if selected_driver == self.database.driver_list[i]['driverId']:
                    driver_listbox.select_set([i])
                    driver_listbox.event_generate('<<ListboxSelect>>')

    def circuit_window_destroy(self, event):
        # Set the circuit window to None, destroying it
        self.csw = None

    def circuit_window(self, selected_circuit=None):
        if self.csw:  # if the circuit window is already open
            self.csw.tkraise()  # bring it to the front
        else:
            self.csw = Toplevel()  # create a new circuit window
            self.csw.title('circuit information')
            self.csw.geometry('1000x600')
            self.csw.bind('<Destroy>', self.circuit_window_destroy)  # bind the destroy event to the function
            circuit_listbox = Listbox(self.csw, width=30)
            circuit_listbox.bind('<<ListboxSelect>>',
                                 self.circuit_selection)  # bind the selection event to the function
            my_scroll2 = Scrollbar(self.csw, command=circuit_listbox.yview)
            circuit_listbox.config(yscrollcommand=my_scroll2.set)
            my_scroll2.pack(side=LEFT, fill=Y)
            circuit_listbox.pack(side=LEFT, fill=Y)
            self.csw_frame = ttk.Frame(self.csw)
            self.csw_frame.pack(side='top', fill=NONE, expand=True)
            for c in self.database.circuit_list:  # populate the listbox with circuits
                circuit_listbox.insert('end', c['circuitName'] + ', ' + c['Location']['country'])
            for i in range(len(self.database.circuit_list)):  # select the circuit if it was passed as an argument
                if selected_circuit == self.database.circuit_list[i]['circuitId']:
                    circuit_listbox.select_set([i])
                    circuit_listbox.event_generate('<<ListboxSelect>>')

    def simulation_window_destroy(self, event):
        self.ssw = None

    def simulation_window(self):
        if self.ssw:  # if the simulation window is already open
            self.ssw.tkraise()  # bring it to the front
        else:
            self.ssw = Toplevel()  # create a new simulation window
            self.ssw.title('Simulation Game')
            self.ssw.geometry('1700x1000')
            self.ssw.bind('<Destroy>', self.simulation_window_destroy)  # bind the destroy event to the function
        years_listbox = Listbox(self.ssw, width=30)
        years_listbox.bind('<<ListboxSelect>>', self.simulation_run)  # bind the selection event to the function
        scroller = Scrollbar(self.ssw, command=years_listbox.yview)
        years_listbox.config(yscrollcommand=scroller.set)
        scroller.pack(side=LEFT, fill=Y)
        years_listbox.pack(side=LEFT, fill=Y)
        self.ssw_frame = ttk.LabelFrame(self.ssw, text='Simulation')
        self.ssw_frame.pack(side=RIGHT, fill='both')
        years = self.database.year_list
        for c in years:  # populate the listbox with years
            years_listbox.insert(END, c)

    def simulation_run(self, event):
        # Get selected item from listbox
        selection = event.widget.curselection()
        # If no item or more than one item selected, exit function
        if len(selection) != 1:
            return
        # Clear ssw_frame
        for s in self.ssw_frame.grid_slaves():
            s.destroy()
        # Get cars for selected year and create race
        cars = get_cars(self.database.year_list[selection[0]], self.database)
        race = Race(cars)
        # Simulate the race and display the results
        race.simulate()
        race.display_results('racesimulationgame')
        # Add a Text widget to display the contents of the text file
        text_widget = Text(self.ssw_frame, width=1000, height=60)
        text_widget.columnconfigure(0, weight=1)
        text_widget.rowconfigure(0, weight=1)
        text_widget.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=[N, E, S, W])

        # Open the text file and read its contents into the Text widget
        with open('racesimulationgame', 'r') as f:
            contents = f.read()
            text_widget.insert(END, contents)

    def race_results_window(self, selected_year=None):
        # If the window is already open, bring it to the front
        if self.rrw:
            self.rrw.tkraise()
        # Otherwise, create a new window
        else:
            self.rrw = Toplevel()
            self.rrw.title('race results')
            self.rrw.geometry('1000x600')
            self.rrw.bind('<Destroy>', self.race_results_window_destroy)
            # Create a listbox to display available years
            years_listbox = Listbox(self.rrw, width=30)
            years_listbox.bind('<<ListboxSelect>>', self.year_selection)
            scroller = Scrollbar(self.rrw, command=years_listbox.yview)
            years_listbox.config(yscrollcommand=scroller.set)
            scroller.pack(side=LEFT, fill=Y)
            years_listbox.pack(side=LEFT, fill=Y)
            # Create a frame to hold race results
            self.rrw_frame = ttk.Frame(self.rrw)
            self.rrw_frame.pack(side='top', fill=NONE, expand=True)
            years = self.database.year_list
            # Populate listbox with available years
            for c in years:
                years_listbox.insert(END, c)
            for i in range(len(self.database.year_list)):
                # If a year is selected, highlight it in the listbox
                if selected_year == self.database.year_list[i]:
                    years_listbox.select_set([i])
                    years_listbox.event_generate('<<ListboxSelect>>')

    def year_selection(self, event):
        # Get the selected index
        selection = event.widget.curselection()
        # If nothing is selected, return
        if len(selection) != 1:
            return
        # Destroy previous widgets in the frame
        for slave in self.rrw_frame.grid_slaves():
            slave.destroy()
        # Set the selected year and get the circuits for that year
        self.year = self.database.year_list[selection[0]]
        circuits_list = self.database.get_races_for_season(self.year)
        # Set the initial circuit to the first circuit in the list
        selected_circuit = StringVar()
        if len(circuits_list) > 0:
            selected_circuit.set(circuits_list[0])
            # Create the circuits menu
            circuits_menu = ttk.OptionMenu(self.rrw_frame, selected_circuit, circuits_list[0], *circuits_list,
                                           command=self.race_results_selection)
            # Display the circuits menu
            circuits_menu.grid(row=0, column=0, columnspan=4)

    def race_results_selection(self, selection):
        # Destroy previous widgets in the frame
        for s in self.rrw_frame.grid_slaves():
            if s.grid_info()['row'] > 0:
                s.destroy()
        circuit_id = ''
        # Find the circuit id for the selected circuit name
        for c in self.database.circuit_list:
            if c['circuitName'] == selection:
                circuit_id = c['circuitId']
                break
        # Create the header labels for the race results table
        ttk.Label(self.rrw_frame, text='Position').grid(column=0, row=1)
        ttk.Label(self.rrw_frame, text='Driver').grid(column=1, row=1)
        ttk.Label(self.rrw_frame, text='Constructor').grid(column=2, row=1)
        ttk.Label(self.rrw_frame, text='Fastest lap').grid(column=3, row=1)
        ttk.Label(self.rrw_frame, text='FL Avg Speed').grid(column=4, row=1)
        ttk.Label(self.rrw_frame, text='Points').grid(column=5, row=1)
        ttk.Label(self.rrw_frame, text='Grid').grid(column=6, row=1)
        ttk.Label(self.rrw_frame, text='Status').grid(column=7, row=1)
        # Get the race results for the selected circuit and year
        results = self.database.get_race_results(circuit_id, self.year)
        # Create a label for each result and add it to the frame
        for i in range(len(results)):
            for j in range(len(results[i]) - 1):
                label = ttk.Label(self.rrw_frame, text=results[i][j])
                label.grid(column=j, row=i + 2)
                # Bind a click event to the driver name to display their details
                if j == 1:
                    label.bind('<Button-1>',
                               lambda evt, driver=results[i][-1]: self.race_driver_click(evt, driver))
                # Bind a click event to the fastest lap time to display the lap times plot
                if j == 3:
                    label.bind('<Button-1>',
                               lambda evt, driver_id=results[i][-1], driver_name=results[i][1], circuit_id=circuit_id,
                                      circuit_name=selection, year=self.year:
                               self.plot_lap_times(driver_id, driver_name, circuit_id, circuit_name, year))

    def race_driver_click(self, evt, driver_id):
        # Calls the driver_standings_window method with the selected driver's ID
        self.driver_standings_window(selected_driver=driver_id)

    def race_results_window_destroy(self, event):
        # Sets the rrw attribute to None, indicating that the race results window has been destroyed
        self.rrw = None

    @staticmethod
    def convert_to_float(lap_time_str):
        # Splits a lap time string into minutes, seconds, and milliseconds and returns the time in seconds
        minutes, seconds = lap_time_str.split(":")
        seconds, millis = seconds.split(".")
        return float(minutes) * 60 + float(seconds) + float(millis) / 1000

    def plot_lap_times(self, driver_id, driver_name, circuit_id, circuit_name, year):
        """ Plots a list of lap times on a graph using Matplotlib."""
        # Retrieves a list of lap times for a specific driver and circuit in a given year
        lap_time_list = database.get_list_of_lap_times(year, driver_id, circuit_id)

        # Convert lap time list to seconds
        for i in range(len(lap_time_list)):
            lap_time_list[i] = self.convert_to_float(lap_time_list[i])

        # Get the maximum and minimum lap times
        max_lap_time = max(lap_time_list)
        min_lap_time = min(lap_time_list)

        # Set x values as indices of the lap_time_list
        x_values = range(len(lap_time_list))

        # Create a new figure and axis
        fig, ax = plt.subplots()

        # Plot the lap times as a line graph
        ax.plot(x_values, lap_time_list)

        # Set the y-tick values to be 5-second intervals from min to max lap time
        first_y_tick = int(5 * math.floor(min_lap_time / 5))
        last_y_tick = int(5 * math.ceil(max_lap_time / 5))
        ax.set_yticks(range(first_y_tick, last_y_tick, 5))

        # Set the axis labels and title
        ax.set_xlabel('Lap number')
        ax.set_ylabel('Lap time (seconds)')
        ax.set_title(f'{driver_name}, {circuit_name}, {year}')

        # Display the plot
        plt.show()

    def constructors_window(self):
        if self.cw:  # if the window already exists
            self.cw.tkraise()  # bring the existing window to the top
        else:  # if the window does not exist
            self.cw = Toplevel()  # create a new window
            self.cw.title('Constructor information')  # set the title of the new window
            self.cw.geometry('1000x600')  # set the size of the new window
            self.cw.bind('<Destroy>',
                         self.constructors_window_destroy)  # bind a callback function to the window's Destroy event
            constructors_listbox = Listbox(self.cw, width=30)  # create a listbox widget
            constructors_listbox.bind('<<ListboxSelect>>',
                                      self.constructors_selection)  # bind a callback function to the widget's ListboxSelect event
            my_scroll2 = Scrollbar(self.cw, command=constructors_listbox.yview)  # create a scrollbar widget
            constructors_listbox.config(
                yscrollcommand=my_scroll2.set)  # set the listbox widget's yscrollcommand to the scrollbar widget's set method
            my_scroll2.pack(side=LEFT,
                            fill=Y)  # pack the scrollbar widget on the left side of the window, filling the Y axis
            constructors_listbox.pack(side=LEFT,
                                      fill=Y)  # pack the listbox widget on the left side of the window, filling the Y axis
            self.cw_frame = ttk.Frame(self.cw)  # create a new frame widget
            self.cw_frame.pack(side='top', fill=NONE,
                               expand=True)  # pack the frame widget on the top side of the window, filling none and expanding
            for c in self.database.constructor_list:  # loop through each constructor in the database's constructor list
                constructors_listbox.insert('end',
                                            f"{c['name']} ({c['nationality']})")  # insert the constructor's name and nationality into the listbox widget

    def constructors_window_destroy(self, event):
        self.cw = None  # set the window variable to None

    def constructors_selection(self, event):
        selection = event.widget.curselection()  # get the current selection in the widget that triggered the event
        if len(selection) != 1:  # if there are no or more than one selection
            return  # exit the function
        for slave in self.cw_frame.grid_slaves():  # loop through each widget in the frame widget
            slave.destroy()  # destroy the widget
        constructor = self.database.constructor_list[
            selection[0]]  # get the selected constructor from the database's constructor list
        constructor_info = HTMLScrolledText(self.cw_frame, width=70, height=15, padx=10, pady=1)  # create a HTMLScrolledText widget
        constructor_info.set_html(self.get_wikipedia_summary(constructor['url'].split('/')[-1]))  # set the widget's HTML content by getting a summary of the constructor from Wikipedia
        constructor_info.configure(state='disabled')  # disable the editing of the widget
        constructor_info.grid(row=1, column=0, rowspan=2, sticky=[N, E, S, W])  # grid the widget to the frame widget, spanning 2 rows and setting the sticky properties

        # Create circuit season frame
        self.ct_frame = ttk.Frame(self.cw_frame)  # create a new frame widget
        self.ct_frame.grid(row=0, column=0, sticky=[N, E, S, W])  # grid the frame widget to the frame widget, setting the sticky properties
        self.constructor_key = constructor['constructorId']  # set the constructor key

        seasons_list = self.database.get_seasons_for_constructor(self.constructor_key) # get a list of seasons for the selected constructor

        # Reverse the list of seasons so that the most recent is first
        seasons_list.reverse()

        # Create a variable to store the user's selected season
        selected_season = StringVar()

        # If there are seasons in the list
        if len(seasons_list) > 0:
            # Create an OptionMenu widget to allow the user to select a season
            seasons_menu = ttk.OptionMenu(self.ct_frame, selected_season, seasons_list[0], *seasons_list,
                                          command=self.constructor_season_selection)
            seasons_menu.grid(row=0, column=0, columnspan=5)

            # Set the initial value of the OptionMenu to the first season in the list
            selected_season.set(seasons_list[0])

    def constructor_season_selection(self, selection):
        for s in self.ct_frame.grid_slaves():
            if s.grid_info()['row'] > 0:
                s.destroy()  # destroy any previous data
        results = self.database.get_constructor_results_for_season(self.constructor_key, selection)
        for i in range(len(results)):
            for j in range(5):
                label = ttk.Label(self.ct_frame, text=results[i][j])  # create a label with the race information
                label.grid(column=j, row=i + 1)  # place the label in the grid
                # Clicking on this row takes the user to that race
                label.bind('<Button-1>',
                           lambda evt, year=selection, circuit=results[i][5]: self.race_click(year, circuit))  # bind a function to the label

    def main_window(self):
        """Create the main menu"""
        self.root.title('Formula One')  # Set the title of the window
        self.root.geometry('850x250')  # Set the size of the window
        button_frame = ttk.LabelFrame(self.frame, text="Main menu")  # Create a frame for the buttons
        button_frame.grid(row=0, column=0, sticky=[N, E, S, W])  # Place the frame in the grid
        self.frame.columnconfigure(0, weight=1)  # Configure the columns to resize with the window
        self.frame.rowconfigure(0, weight=1)  # Configure the rows to resize with the window

        # Create the main menu buttons
        style = ttk.Style()  # Create a style object
        style.configure('TButton', padding=5, width=40)  # Configure the style of the buttons
        exiting = ttk.Button(button_frame, text='Exit', style='TButton',
                             command=root.destroy)  # Create a button that closes the window
        driver_standings = ttk.Button(button_frame, text='Drivers',
                                      command=self.driver_standings_window)  # Create a button that opens the driver standings window
        race_results = ttk.Button(button_frame, text='Race Results', style='TButton',
                                  command=self.race_results_window)  # Create a button that opens the race results window
        constructors = ttk.Button(button_frame, text='Constructors', style='TButton',
                                  command=self.constructors_window)  # Create a button that opens the constructors window
        circuits = ttk.Button(button_frame, text='Circuits', style='TButton',
                              command=self.circuit_window)  # Create a button that opens the circuits window
        simulation_game = ttk.Button(button_frame, text='Simulation Game', style='TButton',
                                     command=self.simulation_window)  # Create a button that opens the simulation game window
        # Place the buttons in the grid
        exiting.grid(row=0, column=0, pady=2, sticky=[N, E, S, W])
        driver_standings.grid(row=0, column=1, pady=2, sticky=[N, E, S, W])
        race_results.grid(row=0, column=2, pady=2, sticky=[N, E, S, W])
        constructors.grid(row=1, column=1, pady=2, sticky=[N, E, S, W])
        circuits.grid(row=1, column=2, pady=2, sticky=[N, E, S, W])
        simulation_game.grid(row=1, column=0, pady=2, sticky=[N, E, S, W])
        for i in range(2):
            button_frame.rowconfigure(i, weight=1)  # Configure the rows to resize with the window
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)  # Configure the columns to resize with the window
        self.root.mainloop()  # Start the event loop


# Define three functions to save, load, and get data from the web for a database
def save_database(db, filename):
    db.save_to_file(filename)

def load_database(db, filename):
    db.load_from_file(filename)

def get_database_from_web(db):
    db.get_data()

if __name__ == '__main__':
    # Create an Ergast object as a database
    database = Ergast()
    try:
        # Try to get the data from the web and save it to a file
        get_database_from_web(database)
        save_database(database, 'database.bin')
    except (json.decoder.JSONDecodeError, ConnectionRefusedError, ConnectionError):
        # If getting the data from the web failed, load it from a file
        load_database(database, 'database.bin')

    # Create a Tk object and an F1Gui object with the database
    root = Tk()
    f1Gui = F1Gui(root, database)
    # Call the main_window() function of F1Gui to display the main menu
    f1Gui.main_window()


