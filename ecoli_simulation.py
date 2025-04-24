import numpy as np
import time

class EColiSimulation:
    def __init__(self, initial_population=100, food_quantity=1000, air_quantity=1000,
                 max_population=10000, max_food=500, max_air=500):

        self.population = initial_population
        self.food_quantity = food_quantity
        self.air_quantity = air_quantity
        self.max_population = max_population
        self.max_food = max_food
        self.max_air = max_air

        # History tracking
        self.population_history = [initial_population]
        self.food_history = [food_quantity]
        self.air_history = [air_quantity]
        self.time_history = [0]
        self.start_time = time.time()

    def calculate_growth_rate(self):
        base_rate = 0.034  # per min
        food_factor = self.food_quantity / (100 + self.food_quantity)
        air_factor = self.air_quantity / (100 + self.air_quantity)
        capacity_factor = 1 - (self.population / self.max_population)
        return base_rate * food_factor * air_factor * max(0, capacity_factor)

    def calculate_death_rate(self):
        base_death_rate = 0.005  # Natural death rate

        food_scarcity = max(0, 1 - (self.food_quantity / 50))

        air_scarcity = max(0, 1 - (self.air_quantity / 30))

        death_rate = base_death_rate + 0.05 * (food_scarcity**2 + air_scarcity**2)

        return death_rate

    def step(self, dt=1):
        growth_rate = self.calculate_growth_rate()
        death_rate = self.calculate_death_rate()

        # Calculate population change considering both growth and death
        new_cells = self.population * np.exp(growth_rate * dt) - self.population
        dead_cells = self.population * (1 - np.exp(-death_rate * dt))

        # Update population
        self.population += new_cells - dead_cells

        # Consume resources
        self.food_quantity -= new_cells * 0.1  # Each new cell consumes 0.1 food units
        self.air_quantity -= new_cells * 0.05  # Each new cell consumes 0.05 air units

        # Ensure values stay within valid ranges
        self.population = max(0, min(self.population, self.max_population))
        self.food_quantity = max(0, self.food_quantity)
        self.air_quantity = max(0, self.air_quantity)

        # Update history
        current_time = time.time() - self.start_time
        self.population_history.append(self.population)
        self.food_history.append(self.food_quantity)
        self.air_history.append(self.air_quantity)
        self.time_history.append(current_time)

        return self.population, self.food_quantity, self.air_quantity

    def add_food(self, amount):
        self.food_quantity = min(self.food_quantity + amount, self.max_food)

    def add_air(self, amount):
        self.air_quantity = min(self.air_quantity + amount, self.max_air)

    def get_status(self):
        return {
            "population": self.population,
            "food": self.food_quantity,
            "air": self.air_quantity,
            "growth_rate": self.calculate_growth_rate() * 100,  # percentage per minute
            "death_rate": self.calculate_death_rate() * 100  # percentage per minute
        }
