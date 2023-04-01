import requests  # Imports requests module
import json  # Imports json module
import pickle  # Imports pickle module


class Ergast:
    """Class to encapsulate accessing the Ergast online database"""

    def __init__(self):
        """Create the instance, but don't populate the data tables yet"""
        self.driver_list = None
        self.constructor_list = None
        self.circuit_list = None
        self.year_list = None
        self.url = "http://ergast.com/api/f1/"

    def get_data(self):
        """Get the data tables from the online database"""
        self._get_driver_list()  # call the private method to retrieve driver list
        self._get_constructor_list()  # call the private method to retrieve constructor list
        self._get_circuit_list()  # call the private method to retrieve circuit list
        self._get_year_list()  # call the private method to retrieve year list

    def _get_driver_list(self):
        """Retrieve a list with one entry per driver"""
        table = requests.get(self.url + 'drivers.json?limit=900')  # retrieve JSON data of drivers
        table_content = json.loads(table.content)  # load JSON content
        driver_temp = table_content['MRData']['DriverTable']  # get the driver table
        self.driver_list = driver_temp['Drivers']  # set the driver list

    def _get_constructor_list(self):
        """Retrieve a list with one entry per constructor"""
        table = requests.get(self.url + 'constructors.json?limit=300')    # Get the JSON table with constructor data and limit the response to 300 entries
        table_content = json.loads(table.content)  # Load the content of the table into a Python object
        constructor_temp = table_content['MRData']['ConstructorTable']  # Extract the constructor data from the content
        self.constructor_list = constructor_temp['Constructors']  # Save the constructor data to the instance variable constructor_list

    def get_seasons_for_driver(self, driver_id):
        """Retrieve a list of seasons in which a driver competed"""
        table = requests.get(self.url + f'drivers/{driver_id}/seasons.json')  # Get the JSON table with the seasons in which the driver competed
        table_content = json.loads(table.content)  # Load the content of the table into a Python object
        season_table = table_content['MRData']['SeasonTable']['Seasons']  # Extract the season data from the content
        season_list = [s['season'] for s in season_table]  # Create a list of seasons by extracting the 'season' field from each entry in the season table
        return season_list  # Return the list of seasons

    def get_seasons_for_circuit(self, circuit_id):
        """Retrieve a list of seasons in which a circuit was used"""
        table = requests.get(f'{self.url}circuits/{circuit_id}/seasons.json')  # Get the JSON table with the seasons in which the circuit was used
        table_content = json.loads(table.content)  # Load the content of the table into a Python object
        season_table = table_content['MRData']['SeasonTable']['Seasons']  # Extract the season data from the content
        season_list = [s['season'] for s in season_table]  # Create a list of seasons by extracting the 'season' field from each entry in the season table
        return season_list  # Return the list of seasons

    def get_seasons_for_constructor(self, constructor_id):
        """Retrieve a list of seasons in which a constructor competed"""
        table = requests.get(
            f'{self.url}constructors/{constructor_id}/seasons.json')  # send GET request to get seasons for a constructor
        table_content = json.loads(table.content)  # parse JSON content from response
        season_table = table_content['MRData']['SeasonTable']['Seasons']  # get the list of seasons from the parsed JSON
        season_list = [s['season'] for s in
                       season_table]  # create a list of seasons by extracting the 'season' attribute from each item in season_table
        return season_list

    def get_races_for_season(self, year):
        """Retrieve a list of races that took place in a season"""
        table = requests.get(f'{self.url}{year}/circuits.json')  # send GET request to get races for a year
        table_content = json.loads(table.content)  # parse JSON content from response
        race_table = table_content['MRData']['CircuitTable']['Circuits']  # get the list of races from the parsed JSON
        race_list = [r['circuitName'] for r in
                     race_table]  # create a list of races by extracting the 'circuitName' attribute from each item in race_table
        return race_list

    def get_round_for_circuit_in_year(self, year, circuit_id):
        """Retrive the round number for a circuit in a given year"""
        round_no = 0  # initialize round_no to 0
        table = requests.get(f'{self.url}{year}.json')  # send GET request to get races for a year
        table_content = json.loads(table.content)  # parse JSON content from response
        race_table = table_content['MRData']['RaceTable']['Races']  # get the list of races from the parsed JSON
        for r in race_table:  # iterate over each race in the race_table
            if r['Circuit']['circuitId'] == circuit_id:  # if the circuitId of the race matches the circuit_id argument
                round_no = r['round']  # update round_no to the round number of the race
        return round_no

    def get_driver_results_for_season(self, driver_id, season):
        """Retrieve a list of (position, race name) results for a specific driver in a season"""
        table = requests.get(self.url + f'{season}/drivers/{driver_id}/results.json')  # send GET request to get results for a driver in a season
        table_content = json.loads(table.content)  # parse JSON content from response
        driver_race_results_table = table_content['MRData']['RaceTable']['Races']  # get the list of races from the parsed JSON
        driver_race_results_list = [(r['Results'][0]['position'], r['raceName'], r['Circuit']['circuitId']) for r in driver_race_results_table]  # create a list of driver results by extracting the 'position', 'raceName', and 'circuitId' attributes from each item in driver_race_results_table
        return driver_race_results_list

    def get_circuit_results_for_season(self, circuit_id, season):
        """Retrieve a list of (position, driver name, driverId) results for a specific circuit in a season"""
        table = requests.get(self.url + f'{season}/circuits/{circuit_id}/results.json')  # Get the race results for the given circuit and season
        table_content = json.loads(table.content)  # Load the content of the response as JSON
        circuit_race_results_table = table_content['MRData']['RaceTable']['Races'][0]['Results']  # Get the list of results from the first race of the season
        circuit_race_results_list = []  # Initialize an empty list to store the results
        for r in circuit_race_results_table:
            name = r['Driver']['givenName'] + ' ' + r['Driver']['familyName']  # Get the driver's full name
            circuit_race_results_list.append([r['position'], name, r['Driver']['driverId']])  # Add the driver's position, full name, and driver ID to the list of results
        return circuit_race_results_list  # Return the list of results

    def get_constructor_results_for_season(self, constructor_id, season):
        """Retrieve a list of (position, driver name, driverId) results for a specific circuit in a season"""
        table = requests.get(self.url + f'{season}/constructors/{constructor_id}/results.json')  # Get the race results for the given constructor and season
        table_content = json.loads(table.content)  # Load the content of the response as JSON
        race_table = table_content['MRData']['RaceTable']['Races']  # Get the list of races from the season
        constructor_race_results_list = []  # Initialize an empty list to store the results
        for r in race_table:
            d1 = r['Results'][0]['Driver']  # Get the first driver's information
            d1_name = f"{d1['givenName']} {d1['familyName']}"  # Get the first driver's full name
            d1_points = r['Results'][0]['points']  # Get the first driver's points
            d2 = r['Results'][1]['Driver']  # Get the second driver's information
            d2_name = f"{d2['givenName']} {d2['familyName']}"  # Get the second driver's full name
            d2_points = r['Results'][1]['points']  # Get the second driver's points
            constructor_race_results_list.append([r['raceName'], d1_name, d1_points, d2_name, d2_points, r['Circuit']['circuitId']])  # Add the race name, both drivers' full names, both drivers' points, and the circuit ID to the list of results
        return constructor_race_results_list  # Return the list of results

    def get_race_results(self, circuit_id, season):
        """Retrieve a list of (position, driver name, constructor, fastest lap, fastest lap speed, points, grid position, status, driverId)
        results for a specific race in a season"""
        table = requests.get(self.url + f'{season}/circuits/{circuit_id}/results.json?limit=500')  # Get the race results for the given circuit and season, with a maximum of 500 results
        try:
            table_content = json.loads(table.content)  # Load the content of the response as JSON
        except json.decoder.JSONDecodeError:
            print('JSON error: ',table.content)  # If there is an error decoding the JSON, print an error message and return None
        circuit_race_results_table = table_content['MRData']['RaceTable']['Races'][0]['Results']  # retrieve race results table for a specific circuit in a season
        circuit_race_results_list = []  # create an empty list to store the results for each driver
        for r in circuit_race_results_table:  # iterate through each race result
            name = r['Driver']['givenName'] + ' ' + r['Driver']['familyName']  # concatenate driver's first and last name
            if r.get('FastestLap'):  # check the drivers' fastest lap time, this will not be true if the race is pre 2004 as that is where fastest lap works from
                fastest_lap_speed = r['FastestLap']['AverageSpeed']['speed'] + ' ' + r['FastestLap']['AverageSpeed']['units']  # concatenate the speed and units of the fastest lap
                fastest_lap_time = r['FastestLap']['Time']['time']  # retrieve the time of the fastest lap
            else:
                fastest_lap_speed = 'n/a'  # set the fastest lap speed to 'n/a' if the driver didn't complete a lap or if its a pre 2004 race and no fastest lap is existent
                fastest_lap_time = 'n/a'  # set the fastest lap time to 'n/a' if the driver didn't complete a lap or if its a pre 2004 race and no fastest lap is existent
            circuit_race_results_list.append([r['position'],  # append the driver's position
                                              name,  # append the driver's name
                                              r['Constructor']['name'],  # append the name of the driver's constructor
                                              fastest_lap_time,  # append the time of the fastest lap
                                              fastest_lap_speed,  # append the speed and units of the fastest lap
                                              r['points'],  # append the number of points the driver received
                                              r['grid'],  # append the driver's starting grid position
                                              r['status'],  # append the driver's status (e.g. finished, retired)
                                              r['Driver']['driverId']])  # append the driver's ID
        return circuit_race_results_list  # return the list of race results for a circuit

    def _get_year_list(self):
        """Retrieve a list of years"""
        table = requests.get(f"{self.url}seasons.json?limit=100")  # retrieve a table of all the seasons
        standings = json.loads(table.content)  # parse the content of the table as a JSON object
        refined = standings['MRData']['SeasonTable']['Seasons']  # retrieve the list of seasons from the JSON object
        self.year_list = []  # create an empty list to store the years
        for data in refined:
            self.year_list.append(data['season'])  # append the value of the 'season' key to the years list

    def _get_circuit_list(self):
        """Retrieve a list with one entry per circuit"""
        table = requests.get(self.url + 'circuits.json?limit=100')  # retrieve a table of all the circuits
        table_content = json.loads(table.content)  # parse the content of the table as a JSON object
        circuit_temp = table_content['MRData']['CircuitTable']  # retrieve the circuit table from the JSON object
        self.circuit_list = circuit_temp['Circuits']  # retrieve the list of circuits from the circuit table object

    def save_to_file(self, filename):
        """Save the whole database to a local file"""
        # Use with block to close file if any exceptions happen
        with open(filename, 'wb') as f:  # Open a binary file for writing and use 'f' as a file object
            pickle.dump(self.driver_list, f)  # Write the driver_list to the file object 'f'
            pickle.dump(self.circuit_list, f)  # Write the circuit_list to the file object 'f'
            pickle.dump(self.year_list, f)  # Write the year_list to the file object 'f'
            pickle.dump(self.constructor_list, f)  # Write the constructor_list to the file object 'f'

    def load_from_file(self, filename):
        """Load the whole database from a local file"""
        # Use with block to close file if any exceptions happen
        with open(filename, 'rb') as f:  # Open a binary file for reading and use 'f' as a file object
            self.driver_list = pickle.load(f)  # Load the driver_list from the file object 'f'
            self.circuit_list = pickle.load(f)  # Load the circuit_list from the file object 'f'
            self.year_list = pickle.load(f)  # Load the year_list from the file object 'f'
            self.constructor_list = pickle.load(f)  # Load the constructor_list from the file object 'f'

    def get_driver_standings(self, driver_id):
        """Returns driver standings list for a driver"""
        table = requests.get(
            f"{self.url}drivers/{driver_id}/driverStandings.json")  # Request driver standings data for a specific driver from the API and store it in the 'table' variable
        standings = json.loads(
            table.content)  # Convert the contents of the 'table' variable to JSON format and store it in the 'standings' variable
        return standings['MRData'][
            'StandingsTable']  # Return the 'StandingsTable' key of the 'MRData' dictionary in the 'standings' variable

    def get_constructors_for_year(self, year):
        """Returns the constructors that raced in a specified year"""
        year = year  # Assign the 'year' parameter to the 'year' variable
        table = requests.get(f"{self.url}{year}/constructors.json")  # Request constructor data for a specific year from the API and store it in the 'table' variable
        standings = json.loads(table.content)  # Convert the contents of the 'table' variable to JSON format and store it in the 'standings' variable
        refined = standings['MRData']['ConstructorTable']['Constructors']  # Store the 'Constructors' list from the 'ConstructorTable' dictionary in the 'standings' variable in the 'refined' variable
        names = []  # Create an empty list called 'names'
        for data in refined:  # For each dictionary in the 'refined' list
            names.append(data['constructorId'])  # Append the value of the 'constructorId' key to the 'names' list
        return names  # Return the 'names' list

    def get_drivers_by_constructor(self, year, constructors):
        """Returns a list of drivers that raced for a constructor in a given year"""
        year = year  # Assign the input year to the year variable
        table = []  # Initialize an empty list to store results
        for c in constructors:  # Loop through each constructor in the input list
            templist = requests.get(f"{self.url}{year}/constructors/{c}/drivers.json")  # Send a request to the API to get the list of drivers for the given constructor and year
            team_year_drivers = json.loads(templist.content)  # Parse the JSON response and load the data into a Python dictionary
            refined = team_year_drivers['MRData']['DriverTable']['Drivers']  # Extract the relevant data from the dictionary
            for data in refined:  # Loop through each driver in the list of drivers for the given constructor and year
                table.append([c, data['givenName'] + ' ' + data['familyName']])  # Append the constructor name and driver name to the results list
        return table  # Return the list of drivers that raced for the given constructors in the given year

    def get_list_of_lap_times(self, year, driver_id, circuit_id):
        """Retrieve a list of lap times for a driver in a given race"""
        round_no = self.get_round_for_circuit_in_year(year, circuit_id)  # Get the round number of the race for the given year and circuit
        table = requests.get(f"{self.url}{year}/{round_no}/drivers/{driver_id}/laps.json?limit=150")  # Send a request to the API to get the lap times for the given driver in the given race
        standings = json.loads(table.content)  # Parse the JSON response and load the data into a Python dictionary
        refined = standings['MRData']['RaceTable']['Races'][0]['Laps']  # Extract the relevant data from the dictionary
        lap_list = []  # Initialize an empty list to store lap time data
        for data in refined:  # Loop through each lap in the race
            lap_list.append(data['Timings'][0])  # Append the lap time to the lap time list
        times = [d['time'] for d in lap_list]  # Extract just the lap times from the list of lap time data
        return times  # Return the list of lap times for the given driver in the given race
