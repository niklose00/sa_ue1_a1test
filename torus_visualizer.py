import tkinter as tk
from torus import Torus
import time
import math
import threading

class TorusVisualizer:
    def __init__(self, rows, cols, coupling_strength):
        self.root = tk.Tk()
        self.root.title("Glowworm Torus Synchronization")
        
        # Parameter für die Visualisierung
        self.cell_size = 20  # Größe jedes Rechtecks
        self.rows = rows
        self.cols = cols
        self.coupling_strength = coupling_strength
        self.torus = Torus(rows, cols, coupling_strength)

        # Canvas zum Zeichnen der Glühwürmchen
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        # Rechtecke für die Glühwürmchen anlegen
        self.rectangles = [[self.canvas.create_rectangle(
            x * self.cell_size, y * self.cell_size,
            (x + 1) * self.cell_size, (y + 1) * self.cell_size,
            fill="black") for x in range(self.cols)] for y in range(self.rows)]
        
        # Label für die Anzeige des Synchronisationsgrads
        self.sync_label = tk.Label(self.root, text="Grad der Synchronisation: 0.00", font=('Arial', 12))
        self.sync_label.pack()

    def phase_to_color(self, phase):
        normalized_phase = (phase / (2 * math.pi)) % 1
        if abs(normalized_phase - 0.5) < 0.2:  # Toleranz von 0.1 für visuelle Synchronisation
            return "yellow"
        return "black"

    def update_gui(self):
        """Aktualisiert die Farben der Rechtecke basierend auf den Phasen der Glühwürmchen."""
        for row in range(self.rows):
            for col in range(self.cols):
                glowworm = self.torus.grid[row][col]
                color = self.phase_to_color(glowworm.phase)
                self.canvas.itemconfig(self.rectangles[row][col], fill=color)
        
        # Berechnung und Anzeige des Synchronisationsgrads
        sync_degree = self.torus.degree_of_synchronization()
        self.sync_label.config(text=f"Grad der Synchronisation: {sync_degree:.2f}")
        
        # Nächste Aktualisierung planen
        if sync_degree < 1.0:  # Fortfahren, bis Synchronisationsgrad 1 erreicht wird
            self.root.after(100, self.run_simulation_step)

    def run_simulation_step(self):
        """Führt einen Simulationsschritt aus und aktualisiert die GUI."""
        self.torus.update_phases()
        self.update_gui()

    def start_simulation(self):
        """Startet die Simulation und die GUI."""
        # Erhöhe die Kopplungsstärke, um eine Synchronisation zu forcieren
        self.torus.coupling_strength = 1.0  # Starker Kopplungsfaktor für schnellere Synchronisation
        for row in range(self.rows):
            for col in range(self.cols):
                self.torus.grid[row][col].coupling_strength = 1.0

        self.torus.start()
        self.run_simulation_step()
        self.root.mainloop()

    def stop_simulation(self):
        """Stoppt die Simulation und beendet die GUI."""
        self.torus.stop()
        self.root.quit()


# Testen der Visualisierung
if __name__ == "__main__":
    visualizer = TorusVisualizer(rows=15, cols=15, coupling_strength=1.0)
    try:
        visualizer.start_simulation()
    except KeyboardInterrupt:
        visualizer.stop_simulation()
