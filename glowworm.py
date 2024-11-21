# In glowworm.py
import random
import math
import threading
import time

import numpy as np

class Glowworm:
    def __init__(self, natural_frequency, initial_phase=0.0):
        self.phase = initial_phase #zyklisch im Bereich von 0 bis 2𝜋
        # self.phase = initial_phase #zyklisch im Bereich von 0 bis 2𝜋
        self.natural_frequency = natural_frequency #ωi: Die natürliche Frequenz des Glühwürmchens i
        self.neighbors = []
        self.coupling_strength = 1.0  # K: Die Kopplungsstärke, die angibt, wie stark ein Glühwürmchen auf seine Nachbarn reagiert
        self.lock = threading.Lock()
        self.running = False  # Steuerung für den Thread

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def update_phase(self):
        with self.lock:
            # Kopiere die aktuellen Phasen der Nachbarn (alte Werte)
            old_phases = [neighbor.phase for neighbor in self.neighbors]
            
            # Berechne den Einfluss der Nachbarn
            neighbor_influence = sum(math.sin(old_phase - self.phase) for old_phase in old_phases)
            
            # Berechne die Änderung der Phase
            phase_change = self.natural_frequency + (self.coupling_strength / len(self.neighbors)) * neighbor_influence
            print("self.natural_frequency",self.natural_frequency)
            print("phase_change", phase_change)
            self.phase += phase_change
            self.phase = self.phase % (2 * math.pi)  # Halte die Phase im Bereich 0 bis 2*pi

    def start(self):
        """Startet den Thread für das Glühwürmchen."""
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        """Kontinuierliche Schleife zur Aktualisierung der Phase."""
        while self.running:
            time.sleep(0.5)  # Frequenz der Aktualisierungen; kann je nach Bedarf angepasst werden
            self.update_phase()

    def stop(self):
        """Beendet den Thread für das Glühwürmchen."""
        self.running = False
        self.thread.join()

    

    def __repr__(self):
        return f"Glowworm(Phase: {self.phase:.2f}, Frequency: {self.natural_frequency:.2f}, Neighbors: {len(self.neighbors)})"
