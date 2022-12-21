import requests
import json
import pickle


class Ergast:
    """Class to encapsulate accessing the Ergast online database"""
    def __init__(self):
        """Create the instance, but don't populate the data tables yet"""
        self.driver_list = None
        self.circuit_list = None

    def get_data(self):
        """Get the data tables from the online database"""
        self._get_driver_list()
        self._get_circuit_list()

    def _get_driver_list(self):
        """Retrieve a list with one entry per driver"""
        table = requests.get('http://ergast.com/api/f1/drivers.json?limit=900')
        table_content = json.loads(table.content)
        driver_temp = table_content['MRData']['DriverTable']
        self.driver_list = driver_temp['Drivers']

    def _get_circuit_list(self):
        """Retrieve a list with one entry per circuit"""
        table = requests.get('http://ergast.com/api/f1/circuits.json?limit=100')
        table_content = json.loads(table.content)
        circuit_temp = table_content['MRData']['CircuitTable']
        self.circuit_list = circuit_temp['Circuits']

    def save_to_file(self, filename):
        """Save the whole database to a local file"""
        # Use with block to close file if any exceptions happen
        with open(filename, 'wb') as f:
            pickle.dump(self.driver_list, f)
            pickle.dump(self.circuit_list, f)

    def load_from_file(self, filename):
        """Load the whole database from a local file"""
        # Use with block to close file if any exceptions happen
        with open(filename, 'rb') as f:
            self.driver_list = pickle.load(f)
            self.circuit_list = pickle.load(f)
