import threading
import tkinter as tk
import numpy as np
import time

# Parameters for Kuramoto Model
K = 1.0  # Coupling constant
dt = 0.05  # Time step

# Torus size
GRID_SIZE = 10

# Define the Firefly class
class Firefly:
    def __init__(self, x, y, phase, omega, canvas, rect_id):
        self.x = x
        self.y = y
        self.phase = phase
        self.omega = omega
        self.canvas = canvas
        self.rect_id = rect_id

    def update_phase(self, neighbors):
        # Update phase based on neighbors using Kuramoto model
        coupling_sum = sum(np.sin(neighbor.phase - self.phase) for neighbor in neighbors)
        self.phase += dt * (self.omega + (K / len(neighbors)) * coupling_sum)
        self.phase %= 2 * np.pi

    def update_display(self):
        # Update color of the firefly rectangle based on its phase
        brightness = int((np.sin(self.phase) + 1) * 127.5)  # Map phase to brightness value (0-255)
        color = f"#{brightness:02x}{brightness:02x}00"  # Yellowish color gradient
        self.canvas.itemconfig(self.rect_id, fill=color)

# Thread function for each firefly
def firefly_thread(firefly, fireflies, grid_size, sync_rates):
    while True:
        # Get neighbors in the torus structure
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = (firefly.x + dx) % grid_size, (firefly.y + dy) % grid_size
            neighbors.append(fireflies[nx][ny])

        # Update phase and display
        firefly.update_phase(neighbors)
        firefly.update_display()

        # Update synchronization rate
        with sync_rates['lock']:
            sync_rates['phases'].append(firefly.phase)

        # Print phase to console
        print(f"Firefly at ({firefly.x}, {firefly.y}) phase: {firefly.phase:.2f}")
        
        time.sleep(dt)

# Function to calculate synchronization rate
def calculate_sync_rate(phases):
    mean_phase = np.mean(phases)
    order_parameter = np.abs(np.sum(np.exp(1j * np.array(phases))) / len(phases))
    return order_parameter

# Update synchronization rate display
def update_sync_rate_display(root, sync_label, sync_rates):
    while True:
        time.sleep(1)
        with sync_rates['lock']:
            if sync_rates['phases']:
                sync_rate = calculate_sync_rate(sync_rates['phases'])
                sync_label.config(text=f"Synchronization Rate: {sync_rate:.2f}")
                sync_rates['phases'].clear()

# Main function
def main():
    # Initialize Tkinter window
    root = tk.Tk()
    root.title("Firefly Synchronization Simulation")
    canvas = tk.Canvas(root, width=500, height=500, bg="black")
    canvas.pack()

    sync_label = tk.Label(root, text="Synchronization Rate: 0.00", fg="white", bg="black")
    sync_label.pack()

    # Initialize fireflies in a torus structure
    rect_size = 500 // GRID_SIZE
    fireflies = []
    for x in range(GRID_SIZE):
        row = []
        for y in range(GRID_SIZE):
            phase = np.random.uniform(0, 2 * np.pi)
            omega = np.random.uniform(0.9, 1.1)  # Natural frequency, slightly varied for each firefly
            rect_id = canvas.create_rectangle(x * rect_size, y * rect_size, (x + 1) * rect_size, (y + 1) * rect_size, fill="yellow")
            firefly = Firefly(x, y, phase, omega, canvas, rect_id)
            row.append(firefly)
        fireflies.append(row)

    # Synchronization rate tracking
    sync_rates = {'phases': [], 'lock': threading.Lock()}

    # Create and start a thread for each firefly
    threads = []
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            t = threading.Thread(target=firefly_thread, args=(fireflies[x][y], fireflies, GRID_SIZE, sync_rates))
            t.daemon = True  # Set as a daemon thread to end with main program
            t.start()
            threads.append(t)

    # Create and start a thread to update synchronization rate display
    sync_thread = threading.Thread(target=update_sync_rate_display, args=(root, sync_label, sync_rates))
    sync_thread.daemon = True
    sync_thread.start()

    # Run the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
