import random
import math
import threading
import time
import numpy as np

class Glowworm:
    def __init__(self, natural_frequency, initial_phase=0.0):
        self.phase = random.uniform(0, 2 * math.pi)  # zyklisch im Bereich von 0 bis 2𝜋
        self.natural_frequency = natural_frequency  # ωi: Die natürliche Frequenz des Glühwürmchens i
        self.neighbors = []
        self.coupling_strength = 1.0  # K: Die Kopplungsstärke
        self.lock = threading.Lock()
        self.running = False  # Steuerung für den Thread

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def update_phase(self):
        with self.lock:  # Verhindert Race-Conditions
            # Speicher die alten Phasen der Nachbarn
            old_phases = [neighbor.phase for neighbor in self.neighbors]
            
            print(f"Aktuelle Phasen (alt): {old_phases}")

            # Berechne den Einfluss der Nachbarn auf die Phase (nur mit alten Phasenwerten)
            neighbor_influence = sum(math.sin(neighbor.phase - self.phase) for neighbor in self.neighbors)
            phase_change = self.natural_frequency + (self.coupling_strength / len(self.neighbors)) * neighbor_influence
            
            # Update die eigene Phase
            self.phase += phase_change
            self.phase = self.phase % (2 * math.pi)  # Halte die Phase im Bereich 0 bis 2*pi
            
            print(f"Neue Phase: {self.phase:.2f}")

    def start(self):
        """Startet den Thread für das Glühwürmchen."""
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        """Kontinuierliche Schleife zur Aktualisierung der Phase."""
        while self.running:
            self.update_phase()
            time.sleep(1)  # Frequenz der Aktualisierungen; kann je nach Bedarf angepasst werden

    def stop(self):
        """Beendet den Thread für das Glühwürmchen."""
        self.running = False
        self.thread.join()

    def __repr__(self):
        return f"Glowworm(Phase: {self.phase:.2f}, Frequency: {self.natural_frequency:.2f}, Neighbors: {len(self.neighbors)})"


class Torus:
    def __init__(self, rows, cols, coupling_strength):
        self.rows = rows
        self.cols = cols
        self.coupling_strength = coupling_strength
        self.grid = [[Glowworm(natural_frequency=random.uniform(0.5, 1.5)) for _ in range(cols)] for _ in range(rows)]
        self._set_neighbors()

        # Setze Kopplungsstärke für alle Glühwürmchen
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].coupling_strength = coupling_strength

    def _set_neighbors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                glowworm = self.grid[row][col]
                top = self.grid[(row - 1) % self.rows][col]
                bottom = self.grid[(row + 1) % self.rows][col]
                left = self.grid[row][(col - 1) % self.cols]
                right = self.grid[row][(col + 1) % self.cols]
                glowworm.add_neighbor(top)
                glowworm.add_neighbor(bottom)
                glowworm.add_neighbor(left)
                glowworm.add_neighbor(right)

    def start(self):
        # Startet alle Glühwürmchen-Threads
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].start()

    def stop(self):
        # Stoppt alle Glühwürmchen-Threads
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].stop()

    def degree_of_synchronization(self):
        """Berechnet den Synchronisationsgrad r basierend auf den aktuellen Phasen der Glühwürmchen."""
        N = self.rows * self.cols
        phases = [self.grid[row][col].phase for row in range(self.rows) for col in range(self.cols)]
        # Berechnung des komplexen Mittelwerts
        complex_sum = np.sum(np.exp(1j * np.array(phases)))
        r = abs(complex_sum) / N
        return r

    def __repr__(self):
        representation = ""
        for row in self.grid:
            representation += " | ".join(f"{worm.phase:.2f}" for worm in row) + "\n"
        return representation


# Testen der Torus-Struktur und des Multithreadings
if __name__ == "__main__":
    torus = Torus(rows=3, cols=3, coupling_strength=1.0)
    torus.start()

    try:
        for step in range(5):
            print(f"Aktueller Zustand des Torus nach Schritt {step + 1}:")
            print(torus)
            sync_degree = torus.degree_of_synchronization()
            print(f"Grad der Synchronisation (r): {sync_degree:.2f}")
            time.sleep(1)
    finally:
        torus.stop()
        print("Simulation beendet.")
