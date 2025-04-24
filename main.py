from ecoli_simulation import EColiSimulation
from visualization import EColiVisualizer

def main():
    simulation = EColiSimulation(
        initial_population=1000,
        food_quantity=1000,
        air_quantity=1000,
        max_population=10000,
        max_food=5000,
        max_air=5000
    )

    # Create and run visualizer
    visualizer = EColiVisualizer(simulation)
    visualizer.run()

if __name__ == "__main__":
    main()
