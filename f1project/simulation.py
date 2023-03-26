import random

# Define constants
import ergast

NUM_LAPS = 11
TRACK_DISTANCE = 5.5


# Define classes
class Driver:
    def __init__(self, name):
        self.name = name
        self.lap_times = []

    def set_lap_time(self):
        self.lap_times.append(round(random.uniform(60, 75), 2))


class Car:
    def __init__(self, team_name, driver_name):
        self.team_name = team_name
        self.driver = Driver(driver_name)

    def simulate_laps(self):
        for lap in range(NUM_LAPS):
            self.driver.set_lap_time()


class Race:
    def __init__(self, cars):
        self.cars = cars

    def simulate(self):
        for car in self.cars:
            car.simulate_laps()

    def display_results(self, filename):
        with open(filename, "w") as f:
            f.write("Race Results:\n")
            f.write(
                "+--------+---------------------+---------------------+--------------------------------------------------------------------------------+---------------------+\n")
            f.write(
                "| Place  | Team                | Driver              | Lap Times                                                                      | Total Time          |\n")
            f.write(
                "+--------+---------------------+---------------------+--------------------------------------------------------------------------------+---------------------+\n")
            results = []
            for i, car in enumerate(self.cars):
                driver_time = sum(car.driver.lap_times)
                results.append((i + 1, car.team_name, car.driver.name, car.driver.lap_times, driver_time))
            results = sorted(results, key=lambda x: x[4])
            for i, result in enumerate(results):
                lap_times = '  '.join([f"{lap:.2f}" for lap in result[3]])
                f.write(f"| {i + 1:<6} | {result[1]:<19} | {result[2]:<19} | {lap_times:<78} | {result[4]:<19.2f} |\n")
                f.write(
                    "+--------+---------------------+---------------------+--------------------------------------------------------------------------------+---------------------+\n")

            # Display driver total time and positions
            f.write("\nDriver Standings:\n")
            f.write("+--------+---------------------+---------------------+---------------------+\n")
            f.write("| Place  | Driver              | Team                | Total Time          |\n")
            f.write("+--------+---------------------+---------------------+---------------------+\n")
            driver_results = []
            for car in self.cars:
                driver_time = sum(car.driver.lap_times)
                driver_results.append((car.driver.name, car.team_name, driver_time))
            driver_results = sorted(driver_results, key=lambda x: x[2])
            for i, driver_result in enumerate(driver_results):
                f.write(
                    f"| {i + 1:<6} | {driver_result[0]:<19} | {driver_result[1]:<19} | {driver_result[2]:<19.2f} |\n")
                f.write("+--------+---------------------+---------------------+---------------------+\n")


def get_cars(year, database):

    # Define cars for the race
    constructors = database.get_constructors_for_year(year)
    cars = []
    drivers = database.get_drivers_by_constructor(year, constructors)
    for d in drivers:
        cars.append(Car(d[0], d[1]))
    return cars

