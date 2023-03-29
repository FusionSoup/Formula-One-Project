import requests
import json
import pickle


class Ergast:
    """Class to encapsulate accessing the Ergast online database"""
    def __init__(self):
        """Create the instance, but don't populate the data tables yet"""
        self.driver_list = None
        self.circuit_list = None
        self.year_list = None
        self.url = "http://ergast.com/api/f1/"

    def get_data(self):
        """Get the data tables from the online database"""
        self._get_driver_list()
        self._get_circuit_list()
        self._get_year_list()

    def _get_driver_list(self):
        """Retrieve a list with one entry per driver"""
        table = requests.get(self.url + 'drivers.json?limit=900')
        table_content = json.loads(table.content)
        driver_temp = table_content['MRData']['DriverTable']
        self.driver_list = driver_temp['Drivers']

    def get_seasons_for_driver(self, driver_id):
        """Retrieve a list of seasons in which a driver competed"""
        # http://ergast.com/api/f1/drivers/alonso/constructors/renault/seasons
        table = requests.get(self.url + f'drivers/{driver_id}/seasons.json')
        table_content = json.loads(table.content)

        season_table = table_content['MRData']['SeasonTable']['Seasons']
        # Equivalent to
        # season_list = []
        # for s in season_table:
        #     season_list.append(s['season'])
        season_list = [s['season'] for s in season_table]
        return season_list

    def get_seasons_for_circuit(self, circuit_id):
        """Retrieve a list of seasons in which a circuit was used"""
        table = requests.get(f'{self.url}circuits/{circuit_id}/seasons.json')
        table_content = json.loads(table.content)
        season_table = table_content['MRData']['SeasonTable']['Seasons']
        season_list = [s['season'] for s in season_table]
        return season_list

    def get_races_for_season(self, year):
        """Retrieve a list of races that took place in a season"""
        table = requests.get(f'{self.url}{year}/circuits.json')
        table_content = json.loads(table.content)
        race_table = table_content['MRData']['CircuitTable']['Circuits']
        race_list = [r['circuitName'] for r in race_table]
        return race_list

    def get_round_for_circuit_in_year(self, year, circuit_id):
        round_no = 0
        table = requests.get(f'{self.url}{year}.json')
        table_content = json.loads(table.content)
        race_table = table_content['MRData']['RaceTable']['Races']
        for r in race_table:
            if r['Circuit']['circuitId'] == circuit_id:
                round_no = r['round']
        return round_no

    def get_driver_results_for_season(self, driver_id, season):
        """Retrieve a list of (position, race name) results for a specific driver in a season"""
        # http://ergast.com/api/f1/2008/drivers/alonso/results
        table = requests.get(self.url + f'{season}/drivers/{driver_id}/results.json')
        table_content = json.loads(table.content)
        driver_race_results_table = table_content['MRData']['RaceTable']['Races']
        driver_race_results_list = [(r['Results'][0]['position'], r['raceName'], r['Circuit']['circuitId']) for r in driver_race_results_table]
        return driver_race_results_list

    def get_circuit_results_for_season(self, circuit_id, season):
        """Retrieve a list of (position, driver name, driverId) results for a specific circuit in a season"""
        table = requests.get(self.url + f'{season}/circuits/{circuit_id}/results.json')
        table_content = json.loads(table.content)
        circuit_race_results_table = table_content['MRData']['RaceTable']['Races'][0]['Results']
        circuit_race_results_list = []
        for r in circuit_race_results_table:
            name = r['Driver']['givenName'] + ' ' + r['Driver']['familyName']
            circuit_race_results_list.append([r['position'], name, r['Driver']['driverId']])
        return circuit_race_results_list

    def get_race_results(self, circuit_id, season):
        """Retrieve a list of (position, driver name, constructor, fastest lap, fastest lap speed, points, grid position, status, driverId)
         results for a specific race in a season"""
        table = requests.get(self.url + f'{season}/circuits/{circuit_id}/results.json?limit=500')
        try:
            table_content = json.loads(table.content)
        except json.decoder.JSONDecodeError:
            print('JSON error: ', table.content)
        circuit_race_results_table = table_content['MRData']['RaceTable']['Races'][0]['Results']
        circuit_race_results_list = []
        for r in circuit_race_results_table:
            name = r['Driver']['givenName'] + ' ' + r['Driver']['familyName']
            if r.get('FastestLap'):
                fastest_lap_speed = r['FastestLap']['AverageSpeed']['speed'] + ' ' + r['FastestLap']['AverageSpeed']['units']
                fastest_lap_time = r['FastestLap']['Time']['time']
            else:
                fastest_lap_speed = 'n/a'
                fastest_lap_time = 'n/a'
            circuit_race_results_list.append([r['position'],
                                              name,
                                              r['Constructor']['name'],
                                              fastest_lap_time,
                                              fastest_lap_speed,
                                              r['points'],
                                              r['grid'],
                                              r['status'],
                                              r['Driver']['driverId']])
        return circuit_race_results_list

    def _get_year_list(self):
        """Retrieve a list of years"""
        table = requests.get(f"{self.url}seasons.json?limit=100")
        standings = json.loads(table.content)
        refined = standings['MRData']['SeasonTable']['Seasons']
        self.year_list = []
        for data in refined:
            self.year_list.append(data['season'])  # append the value of the 'season' key to the years list

    def _get_circuit_list(self):
        """Retrieve a list with one entry per circuit"""
        table = requests.get(self.url + 'circuits.json?limit=100')
        table_content = json.loads(table.content)
        circuit_temp = table_content['MRData']['CircuitTable']
        self.circuit_list = circuit_temp['Circuits']

    def save_to_file(self, filename):
        """Save the whole database to a local file"""
        # Use with block to close file if any exceptions happen
        with open(filename, 'wb') as f:
            pickle.dump(self.driver_list, f)
            pickle.dump(self.circuit_list, f)
            pickle.dump(self.year_list, f)

    def load_from_file(self, filename):
        """Load the whole database from a local file"""
        # Use with block to close file if any exceptions happen
        with open(filename, 'rb') as f:
            self.driver_list = pickle.load(f)
            self.circuit_list = pickle.load(f)
            self.year_list = pickle.load(f)

    def get_driver_standings(self, driver_id):
        table = requests.get(f"{self.url}drivers/{driver_id}/driverStandings.json")
        standings = json.loads(table.content)
        return standings['MRData']['StandingsTable']

    def get_constructors_for_year(self, year):
        year = year
        table = requests.get(f"{self.url}{year}/constructors.json")
        standings = json.loads(table.content)
        refined = standings['MRData']['ConstructorTable']['Constructors']
        names = []
        for data in refined:
            names.append(data['constructorId'])  # append the value of the 'name' key to the names list
        return names

    def get_drivers_by_constructor(self, year, constructors):
        year = year
        table = []
        for c in constructors:
            templist = requests.get(f"{self.url}{year}/constructors/{c}/drivers.json")
            team_year_drivers = json.loads(templist.content)
            refined = team_year_drivers['MRData']['DriverTable']['Drivers']
            for data in refined:
                table.append([c, data['givenName'] +' '+ data['familyName']])
        return table

    def get_list_of_lap_times(self, year, driver_id, circuit_id):
        """Retrieve a list of lap times for a driver in a given race"""
        round_no = self.get_round_for_circuit_in_year(year, circuit_id)
        table = requests.get(f"{self.url}{year}/{round_no}/drivers/{driver_id}/laps.json?limit=150")
        standings = json.loads(table.content)
        refined = standings['MRData']['RaceTable']['Races'][0]['Laps']
        lap_list = []
        for data in refined:
            lap_list.append(data['Timings'][0])  # append the value of the 'season' key to the years list
        times = [d['time'] for d in lap_list]
        return times
