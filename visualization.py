import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class EColiVisualizer:
    def __init__(self, simulation):
        self.simulation = simulation

        # Set larger font size globally
        plt.rcParams.update({'font.size': 14})

        # Create figure and subplot
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 10))
        plt.subplots_adjust(bottom=0.25)  # Increase bottom margin for stats

        # Initialize plots
        self.pop_line, = self.ax1.plot([], [], 'b-', linewidth=2, label='Population')
        self.food_line, = self.ax2.plot([], [], 'g-', linewidth=2, label='Food')
        self.air_line, = self.ax2.plot([], [], 'r-', linewidth=2, label='Air')

        # Configure axes with larger fonts
        self.ax1.set_title('E. coli Population Growth Simulation', fontsize=16)
        self.ax1.set_ylabel('Population', fontsize=14)
        self.ax1.set_ylim(0, self.simulation.max_population * 1.1)
        self.ax1.tick_params(axis='both', which='major', labelsize=12)
        self.ax1.grid(True)
        self.ax1.legend(loc='upper left', fontsize=12)

        self.ax2.set_xlabel('Time (minutes)', fontsize=14)
        self.ax2.set_ylabel('Resource Quantity', fontsize=14)
        self.ax2.set_ylim(0, max(self.simulation.max_food, self.simulation.max_air) * 1.1)
        self.ax2.tick_params(axis='both', which='major', labelsize=12)
        self.ax2.grid(True)
        self.ax2.legend(loc='upper left', fontsize=12)

        # Create a text area at the bottom for stats instead of on the plot
        self.stats_ax = plt.axes([0.15, 0.05, 0.7, 0.1])  # [left, bottom, width, height]
        self.stats_ax.axis('off')  # Hide the axes
        self.status_text = self.stats_ax.text(0.0, 0.5, '', fontsize=14,
                                            va='center', ha='left')

    def update(self, frame):
        self.simulation.step()

        # Update plots
        time_data = np.array(self.simulation.time_history) / 60  # convert to minutes

        self.pop_line.set_data(time_data, self.simulation.population_history)
        self.food_line.set_data(time_data, self.simulation.food_history)
        self.air_line.set_data(time_data, self.simulation.air_history)

        # Adjust x-axis limits to show recent history
        if time_data[-1] > 2:
            self.ax1.set_xlim(max(0, time_data[-1] - 10), time_data[-1] + 0.5)
            self.ax2.set_xlim(max(0, time_data[-1] - 10), time_data[-1] + 0.5)
        else:
            self.ax1.set_xlim(0, 2)
            self.ax2.set_xlim(0, 2)

        # Update status text
        status = self.simulation.get_status()
        self.status_text.set_text(f"Population: {status['population']:.0f}   "
                                  f"Growth Rate: {status['growth_rate']:.2f}%/min   "
                                  f"Death Rate: {status['death_rate']:.2f}%/min   "
                                  f"Food: {status['food']:.0f}   "
                                  f"Air: {status['air']:.0f}")

        return self.pop_line, self.food_line, self.air_line, self.status_text

    def run(self):
        # Run the visualization
        ani = animation.FuncAnimation(
            self.fig, self.update, interval=100, blit=True, save_count=100)
        plt.show()
