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
    def __init__(self, team_name, driver1_name, driver2_name):
        self.team_name = team_name
        self.driver1 = Driver(driver1_name)
        self.driver2 = Driver(driver2_name)

    def simulate_laps(self):
        for lap in range(NUM_LAPS):
            self.driver1.set_lap_time()
            self.driver2.set_lap_time()


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
                driver1_time = sum(car.driver1.lap_times)
                driver2_time = sum(car.driver2.lap_times)
                total_time = driver1_time + driver2_time
                results.append((i + 1, car.team_name, car.driver1.name, car.driver1.lap_times, driver1_time))
                results.append((i + 1, car.team_name, car.driver2.name, car.driver2.lap_times, driver2_time))
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
                driver1_time = sum(car.driver1.lap_times)
                driver2_time = sum(car.driver2.lap_times)
                driver_results.append((car.driver1.name, car.team_name, driver1_time))
                driver_results.append((car.driver2.name, car.team_name, driver2_time))
            driver_results = sorted(driver_results, key=lambda x: x[2])
            for i, driver_result in enumerate(driver_results):
                f.write(
                    f"| {i + 1:<6} | {driver_result[0]:<19} | {driver_result[1]:<19} | {driver_result[2]:<19.2f} |\n")
                f.write("+--------+---------------------+---------------------+---------------------+\n")


    # Define cars for the race
my_instance = ergast.Ergast()  # create an instance of MyClass
constructor = my_instance.get_list_of_cars_for_year('2018')
#print(constructor)
car1 = Car(constructor[0], "Lewis Hamilton", "Valtteri Bottas")
car2 = Car(constructor[1], "Max Verstappen", "Sergio Perez")
car3 = Car(constructor[2], "Charles Leclerc", "Carlos Sainz")
car4 = Car(constructor[3], "Lando Norris", "Daniel Ricciardo")
car5 = Car(constructor[4], "Lewis Hamilton", "Valtteri Bottas")
car6 = Car(constructor[5], "Max Verstappen", "Sergio Perez")
car7 = Car(constructor[6], "Charles Leclerc", "Carlos Sainz")
car8 = Car(constructor[7], "Lando Norris", "Daniel Ricciardo")
car9 = Car(constructor[8], "Lewis Hamilton", "Valtteri Bottas")
car10 = Car(constructor[9], "Max Verstappen", "Sergio Perez")


cars = [car1, car2, car3, car4, car5, car6, car7, car8, car9, car10]

race = Race(cars)

# Run the simulation and display the results
#race.simulate()
#race.display_results('racesimulationgame')