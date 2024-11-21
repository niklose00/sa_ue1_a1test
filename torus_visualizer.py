import tkinter as tk
from torus import Torus
import time

class TorusVisualizer:
    def __init__(self, rows, cols, coupling_strength):
        self.root = tk.Tk()
        self.root.title("Glowworm Torus Synchronization")
        
        # Parameter für die Visualisierung
        self.cell_size = 50  # Größe jedes Rechtecks
        self.rows = rows
        self.cols = cols
        self.torus = Torus(rows, cols, coupling_strength)

        # Canvas zum Zeichnen der Glühwürmchen
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        # Rechtecke für die Glühwürmchen anlegen
        self.rectangles = [[self.canvas.create_rectangle(
            x * self.cell_size, y * self.cell_size,
            (x + 1) * self.cell_size, (y + 1) * self.cell_size,
            fill="black") for x in range(self.cols)] for y in range(self.rows)]

    def phase_to_color(self, phase):
        """Konvertiert die Phase in eine Farbe: aus (schwarz) und an (gelb)."""
        brightness = int((phase / (2 * 3.1415)) * 255)  # Normalisiere Phase auf [0, 255]
        # Schwarz für "aus" und Gelb für "an"
        color = f'#{brightness:02x}{brightness:02x}00'  # Von Schwarz nach Gelb
        return color



    def update_gui(self):
        """Aktualisiert die Farben der Rechtecke basierend auf den Phasen der Glühwürmchen."""
        for row in range(self.rows):
            for col in range(self.cols):
                glowworm = self.torus.grid[row][col]
                color = self.phase_to_color(glowworm.phase)
                self.canvas.itemconfig(self.rectangles[row][col], fill=color)
        
        # Nächste Aktualisierung planen
        self.root.after(100, self.update_gui)

    def start_simulation(self):
        """Startet die Simulation und die GUI."""
        self.torus.start()
        self.update_gui()
        self.root.mainloop()

    def stop_simulation(self):
        """Stoppt die Simulation und beendet die GUI."""
        self.torus.stop()
        self.root.quit()


# Testen der Visualisierung
if __name__ == "__main__":
    visualizer = TorusVisualizer(rows=3, cols=3, coupling_strength=2.0)
    try:
        visualizer.start_simulation()
    except KeyboardInterrupt:
        visualizer.stop_simulation()
