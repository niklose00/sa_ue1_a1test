# In glowworm.py
import random
import math
import threading
import time

import numpy as np

class Glowworm:
    def __init__(self):
        self.phase = random.uniform(0, 2*math.pi)
        self.natural_frequency = random.uniform(0.5, 1)
        self.coupling_strength = 5
        self.neighbors = []
        self.lock = threading.Lock()
        self.running = False
        self.next_phase = self.phase  # Neue Variable für die nächste Phase

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def calculate_next_phase(self):
        with self.lock:
            # Berechne den Einfluss der Nachbarn
            neighbor_influence = sum(math.sin(neighbor.phase - self.phase) for neighbor in self.neighbors)
            # Berechne die Änderung der Phase
            phase_change = self.natural_frequency + (self.coupling_strength / len(self.neighbors)) * neighbor_influence
            self.next_phase = (self.phase + phase_change) % (2 * math.pi)

    def update_phase(self):
        with self.lock:
            self.phase = self.next_phase

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while self.running:
            time.sleep(0.5)
            self.calculate_next_phase()  # Berechne die nächste Phase

    def stop(self):
        self.running = False
        self.thread.join()

    def __repr__(self):
        return f"Glowworm(Phase: {self.phase:.2f}, Frequency: {self.natural_frequency:.2f}, Neighbors: {len(self.neighbors)})"
