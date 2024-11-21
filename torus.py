# In torus.py
import time

import numpy as np
from glowworm import Glowworm
import random

class Torus:
    def __init__(self, rows, cols, coupling_strength):
        self.rows = rows
        self.cols = cols
        self.coupling_strength = coupling_strength
        self.grid = [[Glowworm() for _ in range(cols)] for _ in range(rows)]
        self._set_neighbors()

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
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].start()

    def stop(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].stop()

    def update_phases(self):
        # Aktualisiere die Phasen für alle Glühwürmchen
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].update_phase()

    def degree_of_synchronization(self):
        N = self.rows * self.cols
        phases = [self.grid[row][col].phase for row in range(self.rows) for col in range(self.cols)]
        complex_sum = np.sum(np.exp(1j * np.array(phases)))
        r = abs(complex_sum) / N
        return r

    def __repr__(self):
        representation = ""
        for row in self.grid:
            representation += " | ".join(f"{worm.phase:.2f}" for worm in row) + "\n"
        return representation


if __name__ == "__main__":
    torus = Torus(rows=10, cols=10, coupling_strength=1.0)
    torus.start()

    try:
        for step in range(500):
            print(f"Aktueller Zustand des Torus nach Schritt {step + 1}:")
            print(torus)
            sync_degree = torus.degree_of_synchronization()
            print(f"Grad der Synchronisation (r): {sync_degree:.2f}")
            torus.update_phases()  # Wende die neuen Phasen an
            time.sleep(0.5)
    finally:
        torus.stop()
        print("Simulation beendet.")
