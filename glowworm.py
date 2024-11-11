import random
import math
import numpy as np
import threading
import time

class Glowworm:
    def __init__(self, natural_frequency, initial_phase=0.0):
        """
        Initialisiert ein Glühwürmchen mit einer natürlichen Frequenz und einer anfänglichen Phase.
        :param natural_frequency: Die natürliche Frequenz des Glühwürmchens.
        :param initial_phase: Die anfängliche Phase des Glühwürmchens (Standardwert 0).
        """
        self.phase = initial_phase  # Aktuelle Phase des Glühwürmchens
        self.natural_frequency = natural_frequency  # Natürliche Frequenz des Glühwürmchens (wi)
        self.neighbors = []  # Liste der benachbarten Glühwürmchen in der Torus-Struktur
        

    def add_neighbor(self, neighbor):
        """
        Fügt ein benachbartes Glühwürmchen hinzu.
        :param neighbor: Ein anderes Glühwürmchen-Objekt.
        """
        self.neighbors.append(neighbor)

    def update_phase(self, coupling_strength):
        # Berechnung der Einflüsse der Nachbarn
        neighbor_influence = sum(math.sin(neighbor.phase - self.phase) for neighbor in self.neighbors)
        
        # Phasenänderung gemäß dem Kuramoto-Modell
        phase_change = self.natural_frequency + (coupling_strength / len(self.neighbors)) * neighbor_influence
        
        # Aktualisierung der Phase
        self.phase += phase_change

        # Optionale Normalisierung der Phase (auf einen Bereich von 0 bis 2*pi)
        self.phase = self.phase % (2 * math.pi)

    def __repr__(self):
        """
        Gibt eine String-Repräsentation des Glühwürmchens zurück, um den Zustand zu testen.
        """
        return f"Glowworm (Phase: {self.phase:.2f}, Frequency: {self.natural_frequency:.2f}, Neighbors: {len(self.neighbors)})"


